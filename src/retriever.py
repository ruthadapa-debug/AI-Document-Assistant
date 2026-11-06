from pathlib import Path

import faiss
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer


# Load the embedding model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
_model = None


def get_embedding_model():
    """Load the embedding model only when needed."""
    global _model

    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)

    return _model


def extract_text(pdf_path):
    """Extract text from every page of a PDF."""
    reader = PdfReader(str(pdf_path))
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if text.strip():
            pages.append(f"[Page {page_number}]\n{text}")

    if not pages:
        raise ValueError(
            "No readable text was found in this PDF. "
            "If it is a scanned PDF, OCR may be required."
        )

    return "\n\n".join(pages)


def split_text(text, chunk_size=800, overlap=150):
    """Split extracted text into smaller, overlapping chunks."""
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks


def build_retriever(pdf_path):
    """
    Build a searchable FAISS index for a PDF.

    Returns:
        index: FAISS vector index
        chunks: list of text chunks
    """
    text = extract_text(pdf_path)
    chunks = split_text(text)

    if not chunks:
        raise ValueError("Could not create text chunks from this PDF.")

    model = get_embedding_model()

    embeddings = model.encode(
        chunks,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )

    embeddings = np.asarray(embeddings, dtype="float32")

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    return index, chunks


def retrieve_documents(index, question, chunks, top_k=4):
    """Find the text chunks most relevant to the user's question."""
    if index is None or not chunks:
        return "Please upload a PDF first."

    model = get_embedding_model()

    question_embedding = model.encode(
        [question],
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    question_embedding = np.asarray(
        question_embedding, dtype="float32"
    )

    number_to_find = min(top_k, len(chunks))
    scores, indices = index.search(question_embedding, number_to_find)

    relevant_chunks = []

    for score, chunk_index in zip(scores[0], indices[0]):
        if chunk_index >= 0:
            relevant_chunks.append(
                f"Relevance score: {score:.3f}\n{chunks[chunk_index]}"
            )

    return "\n\n---\n\n".join(relevant_chunks)