"""Upload Center Page - handles document ingestion and indexing."""
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from frontend.utils.styling import get_custom_css
from frontend.utils.api_client import APIClient

st.set_page_config(page_title="Upload Center - InsightForge AI", page_icon="📤", layout="wide")
st.markdown(f"<style>{get_custom_css()}</style>", unsafe_allow_html=True)

# Sidebar indicator
api_client = APIClient()
health = api_client.health_check()
backend_online = health.get("status") != "offline"

with st.sidebar:
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 style="margin: 0; color: #06b6d4; font-weight: 800; font-size: 1.6rem;">🔮 InsightForge AI</h2>
        </div>
        """, 
        unsafe_allow_html=True
    )
    if backend_online:
        st.markdown('<div class="status-indicator status-online" style="width: 100%; justify-content: center; margin-bottom: 1.5rem;"><span class="status-dot online"></span><span>SYSTEM ONLINE</span></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-indicator status-offline" style="width: 100%; justify-content: center; margin-bottom: 1.5rem;"><span class="status-dot offline"></span><span>SYSTEM OFFLINE (DEMO)</span></div>', unsafe_allow_html=True)

st.markdown("<h1 class='gradient-text'>Upload Center</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8; font-size: 1rem;'>Upload customer documents (meeting notes, support tickets, CRM exports) to build the local enterprise knowledge base.</p>", unsafe_allow_html=True)
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

# Setup columns for upload and database list
col_upload, col_list = st.columns([1, 1])

with col_upload:
    st.markdown("<h3 class='section-title'><span class='icon'>📤</span> Ingest New Documents</h3>", unsafe_allow_html=True)
    
    with st.container(border=True):
        uploaded_files = st.file_uploader(
            "Select customer meeting notes, call logs, emails, or support tickets",
            type=["pdf", "docx", "txt", "csv"],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            st.info(f"{len(uploaded_files)} file(s) ready for ingestion.")
            if st.button("🚀 Process & Index Knowledge Chunks", type="primary", use_container_width=True):
                if backend_online:
                    with st.spinner("Chunking, embedding, and indexing in FAISS Vector Store..."):
                        response = api_client.upload_documents(uploaded_files)
                        if response:
                            st.success("All files ingested successfully and synced with SQLite metadata.")
                            for r in response:
                                st.markdown(f"- **{r.get('filename')}**: Extracted and indexed **{r.get('chunk_count')}** semantic chunks.")
                        else:
                            st.error("Failed to process files. Please verify backend logs.")
                else:
                    st.success("Demo Mode: Simulated processing of files completed successfully. FAISS would save index.")

with col_list:
    st.markdown("<h3 class='section-title'><span class='icon'>📁</span> Document Library</h3>", unsafe_allow_html=True)
    
    # Load documents list
    docs = []
    if backend_online:
        docs_res = api_client.list_documents()
        docs = docs_res.get("documents", [])
    else:
        # Mock demo documents
        docs = [
            {"id": 1, "filename": "sample_meeting_notes.txt", "file_type": "txt", "upload_time": "2026-06-27 12:00:00", "status": "processed", "chunk_count": 8},
            {"id": 2, "filename": "sample_crm_export.csv", "file_type": "csv", "upload_time": "2026-06-27 12:05:00", "status": "processed", "chunk_count": 31},
            {"id": 3, "filename": "sample_support_tickets.txt", "file_type": "txt", "upload_time": "2026-06-27 12:10:00", "status": "processed", "chunk_count": 14}
        ]
        
    if docs:
        st.markdown(f"Total documents indexed: **{len(docs)}**")
        
        # Display as a table/list
        for doc in docs:
            doc_id = doc.get("id")
            filename = doc.get("filename")
            chunks = doc.get("chunk_count")
            file_type = doc.get("file_type", "").upper()
            upload_time = doc.get("upload_time", "")
            
            with st.container(border=True):
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.markdown(f"📄 **{filename}**  `{file_type}`")
                    st.markdown(f"<span style='color: #64748b; font-size: 0.8rem;'>Chunks: {chunks} | Ingested: {upload_time}</span>", unsafe_allow_html=True)
                with c2:
                    if st.button("🗑️ Delete", key=f"del_{doc_id}", use_container_width=True):
                        if backend_online:
                            if api_client.delete_document(doc_id):
                                st.success("Deleted document and cleaned vectors!")
                                st.rerun()
                            else:
                                st.error("Failed to delete document.")
                        else:
                            st.success("Demo Mode: Deleted document.")
                            st.rerun()
    else:
        st.warning("No documents indexed. Upload files to proceed.")
