"""
Vector Store using ChromaDB for RAG (Retrieval Augmented Generation)
"""
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class VectorStore:
    """ChromaDB-based vector store for code and documentation embeddings"""
    
    def __init__(self):
        """Initialize ChromaDB client"""
        try:
            self.client = chromadb.Client(Settings(
                chroma_db_impl="duckdb+parquet",
                persist_directory=settings.chroma_persist_directory
            ))
            
            # Create or get default collections
            self.code_collection = self.client.get_or_create_collection(
                name="code_snippets",
                metadata={"description": "Code snippets and examples"}
            )
            
            self.docs_collection = self.client.get_or_create_collection(
                name="documentation",
                metadata={"description": "Project documentation and context"}
            )
            
            logger.info("✅ ChromaDB vector store initialized")
            self.enabled = True
            
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {str(e)}")
            self.enabled = False
    
    def add_code(
        self,
        code: str,
        metadata: Dict[str, Any],
        doc_id: Optional[str] = None
    ):
        """Add code snippet to vector store"""
        if not self.enabled:
            return
        
        try:
            import hashlib
            if not doc_id:
                doc_id = hashlib.md5(code.encode()).hexdigest()
            
            self.code_collection.add(
                documents=[code],
                metadatas=[metadata],
                ids=[doc_id]
            )
            logger.debug(f"Added code to vector store: {doc_id}")
            
        except Exception as e:
            logger.error(f"Error adding code to vector store: {str(e)}")
    
    def search_code(
        self,
        query: str,
        n_results: int = 5,
        filter_metadata: Optional[Dict] = None
    ) -> List[Dict[str, Any]]:
        """Search for similar code snippets"""
        if not self.enabled:
            return []
        
        try:
            results = self.code_collection.query(
                query_texts=[query],
                n_results=n_results,
                where=filter_metadata
            )
            
            matches = []
            if results['documents'] and results['documents'][0]:
                for i in range(len(results['documents'][0])):
                    matches.append({
                        "code": results['documents'][0][i],
                        "metadata": results['metadatas'][0][i],
                        "distance": results['distances'][0][i] if 'distances' in results else None
                    })
            
            logger.debug(f"Found {len(matches)} code matches for query")
            return matches
            
        except Exception as e:
            logger.error(f"Error searching code: {str(e)}")
            return []
    
    def get_stats(self) -> Dict[str, Any]:
        """Get vector store statistics"""
        if not self.enabled:
            return {"enabled": False}
        
        try:
            return {
                "enabled": True,
                "code_count": self.code_collection.count(),
                "docs_count": self.docs_collection.count(),
                "persist_directory": settings.chroma_persist_directory
            }
        except Exception as e:
            return {"enabled": True, "error": str(e)}


# Global vector store instance
vector_store = VectorStore()
