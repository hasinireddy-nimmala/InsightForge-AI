"""Document processing for PDF, DOCX, TXT, CSV with chunking."""
import csv
import io
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Processes documents into chunked text segments for embedding."""

    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def process_file(self, file_path: str, file_type: str) -> list[dict]:
        """Process a file and return chunked text segments.

        Args:
            file_path: Path to the file to process.
            file_type: File extension (e.g., 'pdf', 'docx', 'txt', 'csv').

        Returns:
            List of dicts with keys: text, page_number, chunk_index, start_char, end_char.
        """
        file_type = file_type.lower().strip('.')
        try:
            if file_type == 'pdf':
                return self._process_pdf(file_path)
            elif file_type == 'docx':
                text = self._extract_docx(file_path)
                return self._chunk_text(text, page_number=0)
            elif file_type == 'txt':
                text = self._extract_txt(file_path)
                return self._chunk_text(text, page_number=0)
            elif file_type == 'csv':
                text = self._extract_csv(file_path)
                return self._chunk_text(text, page_number=0)
            else:
                logger.warning(f"Unsupported file type: {file_type}. Attempting as plain text.")
                text = self._extract_txt(file_path)
                return self._chunk_text(text, page_number=0)
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")
            return []

    def _process_pdf(self, file_path: str) -> list[dict]:
        """Extract and chunk text from a PDF file, page by page."""
        try:
            from PyPDF2 import PdfReader
        except ImportError:
            logger.error("PyPDF2 is not installed. Cannot process PDF files.")
            return []

        chunks = []
        try:
            reader = PdfReader(file_path)
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                if text and text.strip():
                    page_chunks = self._chunk_text(text, page_number=page_num + 1)
                    chunks.extend(page_chunks)
        except Exception as e:
            logger.error(f"Error extracting PDF {file_path}: {e}")

        # Re-index chunk indices across all pages
        for i, chunk in enumerate(chunks):
            chunk['chunk_index'] = i

        return chunks

    def _extract_pdf(self, file_path: str) -> list[tuple[str, int]]:
        """Extract text from PDF as list of (text, page_number) tuples."""
        try:
            from PyPDF2 import PdfReader
        except ImportError:
            logger.error("PyPDF2 is not installed. Cannot process PDF files.")
            return []

        results = []
        try:
            reader = PdfReader(file_path)
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                if text and text.strip():
                    results.append((text, page_num + 1))
        except Exception as e:
            logger.error(f"Error extracting PDF {file_path}: {e}")
        return results

    def _extract_docx(self, file_path: str) -> str:
        """Extract text from a DOCX file."""
        try:
            import docx2txt
        except ImportError:
            logger.error("docx2txt is not installed. Cannot process DOCX files.")
            return ""

        try:
            text = docx2txt.process(file_path)
            return text if text else ""
        except Exception as e:
            logger.error(f"Error extracting DOCX {file_path}: {e}")
            return ""

    def _extract_txt(self, file_path: str) -> str:
        """Extract text from a plain text file."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading TXT file {file_path}: {e}")
            return ""

    def _extract_csv(self, file_path: str) -> str:
        """Extract text from a CSV file by concatenating all rows."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                reader = csv.reader(f)
                rows = []
                for row in reader:
                    rows.append(', '.join(row))
                return '\n'.join(rows)
        except Exception as e:
            logger.error(f"Error reading CSV file {file_path}: {e}")
            return ""

    def _chunk_text(self, text: str, page_number: int = 0) -> list[dict]:
        """Split text into chunks with overlap, tracking character positions.

        Args:
            text: The text to chunk.
            page_number: The page number this text came from.

        Returns:
            List of dicts with keys: text, page_number, chunk_index, start_char, end_char.
        """
        if not text or not text.strip():
            return []

        chunks = []
        start = 0
        chunk_index = 0
        text_len = len(text)

        while start < text_len:
            end = min(start + self.chunk_size, text_len)
            chunk_text = text[start:end]

            if chunk_text.strip():
                chunks.append({
                    'text': chunk_text.strip(),
                    'page_number': page_number,
                    'chunk_index': chunk_index,
                    'start_char': start,
                    'end_char': end
                })
                chunk_index += 1

            # Move forward by chunk_size - overlap
            if end >= text_len:
                break
            start += self.chunk_size - self.chunk_overlap

        return chunks
