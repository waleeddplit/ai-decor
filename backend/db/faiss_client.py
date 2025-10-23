"""
FAISS vector database client for similarity search
"""

import os
import pickle
from typing import List, Tuple, Optional
import numpy as np
import faiss
from dotenv import load_dotenv

load_dotenv()


class FAISSClient:
    """FAISS vector database for artwork embeddings"""

    def __init__(self, index_path: Optional[str] = None):
        self.index_path = index_path or os.getenv(
            "FAISS_INDEX_PATH", "./data/artwork_vectors.index"
        )
        self.metadata_path = self.index_path.replace(".index", "_metadata.pkl")

        self.index: Optional[faiss.Index] = None
        self.metadata: List[dict] = []
        self.dimension = 512  # CLIP embedding dimension

        # Load index if exists
        if os.path.exists(self.index_path):
            self.load_index()
        else:
            print(f"FAISS index not found at {self.index_path}. Creating new index...")
            self.create_index()

    def create_index(self, dimension: int = 512):
        """Create a new FAISS index"""
        self.dimension = dimension
        # Using IndexFlatL2 for exact search (can be changed to IndexIVFFlat for larger datasets)
        self.index = faiss.IndexFlatL2(dimension)
        print(f"Created new FAISS index with dimension {dimension}")

    def save_index(self):
        """Save FAISS index and metadata to disk"""
        try:
            os.makedirs(os.path.dirname(self.index_path), exist_ok=True)

            # Save FAISS index
            faiss.write_index(self.index, self.index_path)

            # Save metadata
            with open(self.metadata_path, "wb") as f:
                pickle.dump(self.metadata, f)

            print(f"Saved FAISS index to {self.index_path}")
        except Exception as e:
            print(f"Error saving FAISS index: {e}")
            raise

    def load_index(self):
        """Load FAISS index and metadata from disk"""
        try:
            self.index = faiss.read_index(self.index_path)

            # Load metadata
            if os.path.exists(self.metadata_path):
                with open(self.metadata_path, "rb") as f:
                    self.metadata = pickle.load(f)

            print(
                f"Loaded FAISS index from {self.index_path} with {self.index.ntotal} vectors"
            )
        except Exception as e:
            print(f"Error loading FAISS index: {e}")
            raise

    def add_vectors(
        self, vectors: np.ndarray, metadata: List[dict]
    ) -> List[int]:
        """
        Add vectors to the index with associated metadata

        Args:
            vectors: numpy array of shape (n, dimension)
            metadata: list of metadata dicts for each vector

        Returns:
            List of IDs for the added vectors
        """
        if self.index is None:
            self.create_index()

        # Ensure vectors are float32
        vectors = vectors.astype(np.float32)

        # Normalize vectors for cosine similarity (optional)
        faiss.normalize_L2(vectors)

        # Get starting ID
        start_id = self.index.ntotal

        # Add to index
        self.index.add(vectors)

        # Add metadata
        self.metadata.extend(metadata)

        # Return IDs
        ids = list(range(start_id, self.index.ntotal))
        print(f"Added {len(vectors)} vectors to FAISS index")

        return ids

    def search(
        self, query_vector: np.ndarray, k: int = 10
    ) -> Tuple[List[float], List[dict]]:
        """
        Search for k nearest neighbors

        Args:
            query_vector: numpy array of shape (dimension,) or (1, dimension)
            k: number of nearest neighbors to return

        Returns:
            Tuple of (distances, metadata) for k nearest neighbors
        """
        if self.index is None or self.index.ntotal == 0:
            print("FAISS index is empty")
            return [], []

        # Ensure query vector is 2D and float32
        if query_vector.ndim == 1:
            query_vector = query_vector.reshape(1, -1)
        query_vector = query_vector.astype(np.float32)

        # Normalize for cosine similarity
        faiss.normalize_L2(query_vector)

        # Search
        distances, indices = self.index.search(query_vector, min(k, self.index.ntotal))

        # Get metadata for results
        results_metadata = []
        results_distances = []

        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.metadata):
                results_distances.append(float(dist))
                results_metadata.append(self.metadata[idx])

        return results_distances, results_metadata

    def search_by_style(
        self, style_embedding: np.ndarray, filters: Optional[dict] = None, k: int = 20
    ) -> Tuple[List[float], List[dict]]:
        """
        Search for artworks matching a style embedding with optional filters

        Args:
            style_embedding: Style vector from room analysis
            filters: Dict of filters (e.g., {"price_range": [0, 500]})
            k: Number of results to return

        Returns:
            Tuple of (scores, metadata)
        """
        # Get more results than needed for filtering
        search_k = k * 3 if filters else k
        distances, results = self.search(style_embedding, k=search_k)

        # Apply filters if provided
        if filters:
            filtered_distances = []
            filtered_results = []

            for dist, meta in zip(distances, results):
                # Example filter: price range
                if "price_range" in filters:
                    price = meta.get("price", 0)
                    min_price, max_price = filters["price_range"]
                    if not (min_price <= price <= max_price):
                        continue

                # Example filter: style match
                if "style" in filters:
                    if meta.get("style") != filters["style"]:
                        continue

                filtered_distances.append(dist)
                filtered_results.append(meta)

                if len(filtered_results) >= k:
                    break

            return filtered_distances[:k], filtered_results[:k]

        return distances[:k], results[:k]

    def get_total_vectors(self) -> int:
        """Get total number of vectors in index"""
        return self.index.ntotal if self.index else 0


# Singleton instance
_faiss_client: Optional[FAISSClient] = None


def get_faiss_client() -> FAISSClient:
    """Get or create FAISS client singleton"""
    global _faiss_client
    if _faiss_client is None:
        _faiss_client = FAISSClient()
    return _faiss_client

