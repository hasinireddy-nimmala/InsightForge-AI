"""Context Retrieval Agent - performs similarity search using FAISS."""
import logging
from datetime import datetime, timezone
from backend.agents.state import AgentState
from backend.services.embedding_service import EmbeddingService
from backend.services.vector_store import VectorStore
from backend.config import settings

logger = logging.getLogger(__name__)

embedding_service = EmbeddingService(model_name=settings.EMBEDDING_MODEL)
vector_store = VectorStore(
    index_path=settings.FAISS_INDEX_PATH,
    metadata_db_path=settings.FAISS_METADATA_DB,
    embedding_dim=settings.EMBEDDING_DIM
)

async def context_retrieval_agent(state: AgentState) -> dict:
    """Retrieve relevant context from the FAISS vector store."""
    start = datetime.now(timezone.utc)
    logger.info("Context Retrieval Agent: Searching knowledge store")
    
    query = state.get('input_text', '')
    if not query:
        # Fallback to general terms or empty search
        query = "Acme onboarding churn support tickets"
        
    try:
        # Encode query
        query_vector = embedding_service.encode([query])[0]
        
        # Search vector store
        results = vector_store.search(query_vector, top_k=settings.TOP_K)
        
        # Format results
        retrieved_chunks = []
        source_docs = set()
        for r in results:
            retrieved_chunks.append({
                'text': r['chunk_text'],
                'page': r['page_number'],
                'source': r['source_file'],
                'score': r['score']
            })
            if r['source_file']:
                source_docs.add(r['source_file'])
                
        context_package = {
            'retrieved_chunks': retrieved_chunks,
            'source_documents': list(source_docs),
            'total_results': len(retrieved_chunks)
        }
        
        end = datetime.now(timezone.utc)
        duration = (end - start).total_seconds() * 1000
        
        return {
            'context': context_package,
            'agent_timeline': [{
                'agent_name': 'Context Retrieval Agent',
                'status': 'completed',
                'start_time': start.isoformat(),
                'end_time': end.isoformat(),
                'execution_time_ms': duration,
                'output_summary': f"Retrieved {len(retrieved_chunks)} relevant chunks from {len(source_docs)} source files"
            }]
        }
    except Exception as e:
        end = datetime.now(timezone.utc)
        logger.error(f"Context retrieval error: {e}")
        return {
            'context': {'retrieved_chunks': [], 'source_documents': [], 'total_results': 0},
            'error': str(e),
            'agent_timeline': [{
                'agent_name': 'Context Retrieval Agent',
                'status': 'error',
                'start_time': start.isoformat(),
                'end_time': end.isoformat(),
                'execution_time_ms': (end - start).total_seconds() * 1000,
                'output_summary': f'Error: {str(e)[:100]}'
            }]
        }
