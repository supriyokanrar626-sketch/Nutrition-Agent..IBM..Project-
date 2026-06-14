"""
RAG Knowledge Base — Nutrition Agent
Uses ChromaDB + Sentence Transformers for local vector search.
Falls back to keyword search if ChromaDB not available.
"""

import os
import re
from config import CHROMA_PERSIST_DIR, COLLECTION_NAME

NUTRITION_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "nutrition_data.txt")


def load_nutrition_chunks():
    """Load and split nutrition data into chunks."""
    try:
        with open(NUTRITION_DATA_PATH, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        return []

    # Split by section headers or double newlines
    chunks = []
    sections = re.split(r'\n===.*?===\n', text)
    headers = re.findall(r'=== (.*?) ===', text)

    for i, section in enumerate(sections):
        if section.strip():
            paragraphs = [p.strip() for p in section.split('\n') if p.strip()]
            header = headers[i - 1] if i > 0 and i - 1 < len(headers) else "General"
            # Group every 5 lines into a chunk
            for j in range(0, len(paragraphs), 5):
                chunk_text = f"[{header}] " + " ".join(paragraphs[j:j+5])
                if len(chunk_text) > 50:
                    chunks.append(chunk_text)
    return chunks


class NutritionKnowledgeBase:
    """
    RAG knowledge base using ChromaDB + sentence-transformers.
    Falls back to simple keyword search if dependencies unavailable.
    """

    def __init__(self):
        self.chunks = load_nutrition_chunks()
        self.use_vector = False
        self.collection = None
        self._init_vector_store()

    def _init_vector_store(self):
        """Try to initialize ChromaDB vector store."""
        try:
            import chromadb
            from chromadb.utils import embedding_functions
            from sentence_transformers import SentenceTransformer

            client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)

            # Use sentence-transformers embedding
            ef = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2"
            )

            self.collection = client.get_or_create_collection(
                name=COLLECTION_NAME,
                embedding_function=ef
            )

            # Add chunks if collection is empty
            if self.collection.count() == 0 and self.chunks:
                print("📚 Building nutrition knowledge base...")
                ids = [f"chunk_{i}" for i in range(len(self.chunks))]
                self.collection.add(documents=self.chunks, ids=ids)
                print(f"✅ Added {len(self.chunks)} knowledge chunks.")

            self.use_vector = True
            print("✅ Vector store initialized successfully.")

        except Exception as e:
            print(f"⚠️ Vector store unavailable ({e}). Using keyword search.")
            self.use_vector = False

    def retrieve(self, query: str, top_k: int = 5) -> list[str]:
        """Retrieve most relevant nutrition info for a query."""
        if self.use_vector and self.collection:
            return self._vector_retrieve(query, top_k)
        else:
            return self._keyword_retrieve(query, top_k)

    def _vector_retrieve(self, query: str, top_k: int) -> list[str]:
        """Semantic vector retrieval."""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=min(top_k, self.collection.count())
            )
            return results["documents"][0] if results["documents"] else []
        except Exception as e:
            print(f"Vector retrieve error: {e}")
            return self._keyword_retrieve(query, top_k)

    def _keyword_retrieve(self, query: str, top_k: int) -> list[str]:
        """Simple keyword-based fallback retrieval."""
        query_words = set(query.lower().split())
        scored = []
        for chunk in self.chunks:
            chunk_lower = chunk.lower()
            score = sum(1 for w in query_words if w in chunk_lower)
            if score > 0:
                scored.append((score, chunk))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [c for _, c in scored[:top_k]]

    def get_context(self, query: str, top_k: int = 4) -> str:
        """Return formatted context string for LLM prompt."""
        chunks = self.retrieve(query, top_k)
        if not chunks:
            return "No specific nutritional data found. Use general nutrition knowledge."
        return "\n\n".join(chunks)


# Singleton instance
_kb_instance = None

def get_knowledge_base() -> NutritionKnowledgeBase:
    global _kb_instance
    if _kb_instance is None:
        _kb_instance = NutritionKnowledgeBase()
    return _kb_instance
