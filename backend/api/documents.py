"""FastAPI endpoints for document management."""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import aiosqlite
import os
import shutil
import logging
from typing import List

from backend.config import settings
from backend.database import get_db
from backend.models.schemas import DocumentUploadResponse, DocumentInfo, DocumentListResponse
from backend.services.document_processor import DocumentProcessor
from backend.services.embedding_service import EmbeddingService
from backend.services.vector_store import VectorStore
from backend.repositories import document_repo, audit_repo

logger = logging.getLogger(__name__)
router = APIRouter()

# Instantiate services
doc_processor = DocumentProcessor(chunk_size=settings.CHUNK_SIZE, chunk_overlap=settings.CHUNK_OVERLAP)
embedding_service = EmbeddingService(model_name=settings.EMBEDDING_MODEL)
vector_store = VectorStore(
    index_path=settings.FAISS_INDEX_PATH,
    metadata_db_path=settings.FAISS_METADATA_DB,
    embedding_dim=settings.EMBEDDING_DIM
)

@router.post("/documents/upload", response_model=List[DocumentUploadResponse])
async def upload_documents(files: List[UploadFile] = File(...), db: aiosqlite.Connection = Depends(get_db)):
    """Upload, process, chunk, embed and index multiple files."""
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    results = []
    
    for upload_file in files:
        filename = upload_file.filename
        file_ext = os.path.splitext(filename)[1].lower().strip('.')
        
        # Save file to upload directory
        file_path = os.path.join(settings.UPLOAD_DIR, filename)
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(upload_file.file, buffer)
            
            # Save document initially to DB to get its ID
            doc_id = await document_repo.save_document(
                db=db,
                filename=filename,
                file_type=file_ext,
                file_path=file_path,
                chunk_count=0
            )
            
            # Process & chunk file
            chunks = doc_processor.process_file(file_path, file_ext)
            chunk_count = len(chunks)
            
            if chunk_count > 0:
                # Generate embeddings
                chunk_texts = [c['text'] for c in chunks]
                embeddings = embedding_service.encode(chunk_texts)
                
                # Add to FAISS Vector Store
                vector_store.add_documents(
                    chunks=chunks,
                    embeddings=embeddings,
                    document_id=doc_id,
                    source_file=filename
                )
                
                # Update DB record with completed status and correct chunk count
                await document_repo.update_document_status(
                    db=db,
                    doc_id=doc_id,
                    status="processed",
                    chunk_count=chunk_count
                )
                
                # Save interactions in case they are customer conversations
                interaction_text = "\n\n".join(chunk_texts)
                await document_repo.save_interaction(
                    db=db,
                    document_id=doc_id,
                    content=interaction_text,
                    interaction_type="upload"
                )
            else:
                await document_repo.update_document_status(
                    db=db,
                    doc_id=doc_id,
                    status="failed_processing",
                    chunk_count=0
                )
                logger.warning(f"No chunks extracted from document: {filename}")
            
            await audit_repo.log_action(
                db=db,
                action="document_upload",
                entity_type="document",
                entity_id=str(doc_id),
                details=f"Uploaded and processed file {filename} with {chunk_count} chunks"
            )
            
            results.append(DocumentUploadResponse(
                doc_id=doc_id,
                filename=filename,
                file_type=file_ext,
                chunk_count=chunk_count,
                status="processed" if chunk_count > 0 else "failed_processing"
            ))
            
        except Exception as e:
            logger.error(f"Error handling file upload {filename}: {e}")
            results.append(DocumentUploadResponse(
                doc_id=-1,
                filename=filename,
                file_type=file_ext,
                chunk_count=0,
                status=f"error: {str(e)}"
            ))
            
    return results

@router.get("/documents", response_model=DocumentListResponse)
async def list_uploaded_documents(db: aiosqlite.Connection = Depends(get_db)):
    """List all uploaded documents."""
    try:
        docs = await document_repo.list_documents(db)
        # Parse output into Pydantic model structure
        doc_infos = []
        for doc in docs:
            doc_infos.append(DocumentInfo(
                id=doc['id'],
                filename=doc['filename'],
                file_type=doc['file_type'],
                upload_time=doc['upload_time'],
                status=doc['status'],
                chunk_count=doc['chunk_count']
            ))
        return DocumentListResponse(documents=doc_infos, total=len(doc_infos))
    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/documents/{doc_id}")
async def delete_uploaded_document(doc_id: int, db: aiosqlite.Connection = Depends(get_db)):
    """Delete a document, its database entries, vectors, and local file."""
    try:
        doc = await document_repo.get_document(db, doc_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Delete from FAISS Vector Store
        vector_store.delete_document(document_id=doc_id)
        
        # Delete database entries
        await document_repo.delete_document(db, doc_id)
        
        # Delete local file if it exists
        if os.path.exists(doc['file_path']):
            os.remove(doc['file_path'])
            
        await audit_repo.log_action(
            db=db,
            action="document_delete",
            entity_type="document",
            entity_id=str(doc_id),
            details=f"Deleted file {doc['filename']}"
        )
        
        return {"status": "success", "message": f"Deleted document {doc_id}"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting document {doc_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
