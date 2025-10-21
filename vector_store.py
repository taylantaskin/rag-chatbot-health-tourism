import os
from typing import List, Dict
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from pdf_processor import PDFProcessor


class VectorStore:
    """
    Create and manage vector database using Chroma
    """

    def __init__(self, collection_name: str = "health_tourism_docs"):
        """
        Initialize vector store

        Args:
            collection_name: Name of the Chroma collection
        """
        self.collection_name = collection_name

        # Initialize embedding model
        print("Loading embedding model...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✓ Embedding model loaded")

        # Initialize Chroma client
        self.client = chromadb.PersistentClient(path="./chroma_db")

        # Get or create collection
        try:
            self.collection = self.client.get_collection(name=self.collection_name)
            print(f"✓ Loaded existing collection: {self.collection_name}")
        except:
            self.collection = self.client.create_collection(name=self.collection_name)
            print(f"✓ Created new collection: {self.collection_name}")

    def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Create embeddings for a list of texts

        Args:
            texts: List of text strings

        Returns:
            List of embedding vectors
        """
        embeddings = self.embedding_model.encode(texts, show_progress_bar=True)
        return embeddings.tolist()

    def add_documents(self, chunks: List[Dict[str, str]]) -> None:
        """
        Add document chunks to the vector store

        Args:
            chunks: List of document chunks with metadata
        """
        print(f"\nAdding {len(chunks)} documents to vector store...")

        # Prepare data
        texts = [chunk['text'] for chunk in chunks]
        metadatas = [{'source': chunk['source'], 'chunk_id': str(chunk['chunk_id'])}
                     for chunk in chunks]
        ids = [f"{chunk['source']}_{chunk['chunk_id']}" for chunk in chunks]

        # Create embeddings
        print("Creating embeddings...")
        embeddings = self.create_embeddings(texts)

        # Add to collection
        print("Storing in Chroma database...")
        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )

        print(f"✓ Successfully added {len(chunks)} documents")

    def search(self, query: str, n_results: int = 3) -> Dict:
        """
        Search for similar documents

        Args:
            query: Search query
            n_results: Number of results to return

        Returns:
            Dictionary containing search results
        """
        # Create query embedding
        query_embedding = self.embedding_model.encode([query]).tolist()

        # Search
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )

        return results

    def get_collection_stats(self) -> None:
        """
        Print statistics about the collection
        """
        count = self.collection.count()
        print("\n" + "=" * 50)
        print("VECTOR STORE STATISTICS")
        print("=" * 50)
        print(f"Collection name: {self.collection_name}")
        print(f"Total documents: {count}")
        print("=" * 50)


def build_vector_database():
    """
    Main function to build the vector database
    """
    print("=" * 50)
    print("BUILDING VECTOR DATABASE")
    print("=" * 50)

    # Step 1: Process PDFs
    print("\nStep 1: Processing PDFs...")
    processor = PDFProcessor()
    chunks = processor.process_all_pdfs()

    if not chunks:
        print("Error: No chunks created from PDFs")
        return None

    # Step 2: Create vector store
    print("\nStep 2: Creating vector store...")
    vector_store = VectorStore()

    # Step 3: Add documents
    vector_store.add_documents(chunks)

    # Step 4: Show stats
    vector_store.get_collection_stats()

    return vector_store


def test_search(vector_store: VectorStore):
    """
    Test the search functionality
    """
    print("\n" + "=" * 50)
    print("TESTING SEARCH FUNCTIONALITY")
    print("=" * 50)

    test_queries = [
        "What are the benefits of health tourism in Turkey?",
        "Medical tourism services",
        "Thermal tourism in Turkey"
    ]

    for query in test_queries:
        print(f"\nQuery: '{query}'")
        print("-" * 50)

        results = vector_store.search(query, n_results=2)

        for i, (doc, metadata) in enumerate(zip(results['documents'][0],
                                                results['metadatas'][0])):
            print(f"\nResult {i + 1}:")
            print(f"Source: {metadata['source']}")
            print(f"Content: {doc[:200]}...")


# Main execution
if __name__ == "__main__":
    # Build database
    vector_store = build_vector_database()

    # Test search
    if vector_store:
        test_search(vector_store)

        print("\n" + "=" * 50)
        print("✓ Vector database created successfully!")
        print("=" * 50)