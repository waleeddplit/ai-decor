"""
Initialize FAISS vector database
Creates the index structure and adds initial test vectors
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
from db.faiss_client import get_faiss_client


def init_faiss_index():
    """Initialize FAISS index with proper structure"""
    print("📊 Initializing FAISS vector database...")
    print()
    
    try:
        # Get FAISS client
        faiss = get_faiss_client()
        
        current_vectors = faiss.get_total_vectors()
        print(f"Current vectors in index: {current_vectors}")
        
        if current_vectors == 0:
            print("Creating new index with test vectors...")
            
            # Create a few test vectors
            test_vectors = np.random.randn(5, 512).astype(np.float32)
            test_metadata = [
                {"id": "test_1", "title": "Test Artwork 1", "style": "Modern"},
                {"id": "test_2", "title": "Test Artwork 2", "style": "Abstract"},
                {"id": "test_3", "title": "Test Artwork 3", "style": "Minimalist"},
                {"id": "test_4", "title": "Test Artwork 4", "style": "Botanical"},
                {"id": "test_5", "title": "Test Artwork 5", "style": "Contemporary"},
            ]
            
            # Add to index
            faiss.add_vectors(test_vectors, test_metadata)
            
            # Save index
            faiss.save_index()
            
            print(f"✓ Created index with {faiss.get_total_vectors()} test vectors")
        else:
            print("✓ Index already initialized")
        
        # Test search
        print()
        print("Testing vector search...")
        query_vector = np.random.randn(512).astype(np.float32)
        distances, results = faiss.search(query_vector, k=3)
        
        print(f"✓ Search returned {len(results)} results")
        for i, (dist, meta) in enumerate(zip(distances, results), 1):
            print(f"  {i}. {meta.get('title', 'Unknown')} (distance: {dist:.4f})")
        
        print()
        print("=" * 60)
        print("✨ FAISS Initialization Complete!")
        print("=" * 60)
        print(f"Total vectors: {faiss.get_total_vectors()}")
        print(f"Index dimension: {faiss.dimension}")
        print(f"Index path: {faiss.index_path}")
        print()
        
    except Exception as e:
        print(f"❌ Error initializing FAISS: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    init_faiss_index()

