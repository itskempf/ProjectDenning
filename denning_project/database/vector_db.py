"""
Manages the ChromaDB vector database for Project Denning.
"""
import chromadb
import yaml
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class VectorDB:
    """Handles storage and retrieval of vector embeddings."""

    def __init__(self, config_path='config.yaml'):
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            db_path = config.get('vector_db_path', './database/vector_db')
            
            self.client = chromadb.PersistentClient(path=db_path)
            self.collection = self.client.get_or_create_collection(name="uk_law_collection")
            logging.info(f"VectorDB initialized. Collection 'uk_law_collection' has {self.collection.count()} documents.")
        except Exception as e:
            logging.error(f"Failed to initialize VectorDB: {e}")
            raise

    def add_documents(self, chunks: list[str]):
        if not chunks:
            logging.warning("No chunks provided to add to the database.")
            return
        try:
            self.collection.add(
                documents=chunks,
                ids=[f"id_{i}" for i in range(self.collection.count(), self.collection.count() + len(chunks))]
            )
            logging.info(f"Added {len(chunks)} new documents to the collection.")
        except Exception as e:
            logging.error(f"Failed to add documents to ChromaDB: {e}")
            raise

    def query(self, search_text: str, n_results: int = 5) -> list[str]:
        try:
            results = self.collection.query(query_texts=[search_text], n_results=n_results)
            return results['documents'][0] if results['documents'] else []
        except Exception as e:
            logging.error(f"Failed to query ChromaDB: {e}")
            return []