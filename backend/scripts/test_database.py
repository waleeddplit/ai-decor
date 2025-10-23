"""
Test database connections and operations
Verifies Supabase, FAISS, and local storage are working
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
from PIL import Image, ImageDraw

from db.supabase_client import get_supabase_client
from db.faiss_client import get_faiss_client
from utils.file_storage import get_file_storage


def create_test_image(size=(400, 400), color=(100, 150, 200)) -> Image.Image:
    """Create a simple test image"""
    img = Image.new('RGB', size, color=color)
    draw = ImageDraw.Draw(img)
    draw.text((size[0]//2, size[1]//2), "Test Image", fill=(255, 255, 255), anchor="mm")
    return img


async def test_supabase():
    """Test Supabase connection and operations"""
    print("=" * 60)
    print("Testing Supabase Connection")
    print("=" * 60)
    
    try:
        supabase = get_supabase_client()
        print("✓ Supabase client initialized")
        
        # Test: Get user profile (may return None if no data)
        print("\nTest: Fetching user profile...")
        profile = await supabase.get_user_profile("test_user_id")
        if profile:
            print(f"✓ Found profile: {profile.get('name', 'No name')}")
        else:
            print("ℹ No profile found (expected if database is empty)")
        
        # Test: Get artworks
        print("\nTest: Fetching artworks...")
        artworks = await supabase.get_artworks(limit=5)
        print(f"✓ Found {len(artworks)} artworks")
        
        if artworks:
            print(f"  Sample: {artworks[0].get('title', 'Unknown title')}")
        
        print("\n✓ Supabase tests passed")
        return True
        
    except Exception as e:
        print(f"\n❌ Supabase test failed: {e}")
        print("   Make sure SUPABASE_URL and SUPABASE_KEY are set in .env")
        return False


def test_faiss():
    """Test FAISS vector database"""
    print("\n" + "=" * 60)
    print("Testing FAISS Vector Database")
    print("=" * 60)
    
    try:
        faiss = get_faiss_client()
        print(f"✓ FAISS client initialized")
        print(f"  Current vectors: {faiss.get_total_vectors()}")
        print(f"  Dimension: {faiss.dimension}")
        
        # Test: Add vectors
        print("\nTest: Adding test vectors...")
        test_vectors = np.random.randn(3, 512).astype(np.float32)
        test_metadata = [
            {"id": "test_vec_1", "title": "Test 1"},
            {"id": "test_vec_2", "title": "Test 2"},
            {"id": "test_vec_3", "title": "Test 3"},
        ]
        
        before_count = faiss.get_total_vectors()
        faiss.add_vectors(test_vectors, test_metadata)
        after_count = faiss.get_total_vectors()
        
        print(f"✓ Added {after_count - before_count} vectors")
        print(f"  Total vectors: {after_count}")
        
        # Test: Search
        print("\nTest: Searching vectors...")
        query_vector = np.random.randn(512).astype(np.float32)
        distances, results = faiss.search(query_vector, k=5)
        
        print(f"✓ Search returned {len(results)} results")
        for i, (dist, meta) in enumerate(zip(distances, results), 1):
            print(f"  {i}. {meta.get('title', 'Unknown')} (distance: {dist:.4f})")
        
        # Test: Save index
        print("\nTest: Saving index...")
        faiss.save_index()
        print(f"✓ Index saved to {faiss.index_path}")
        
        print("\n✓ FAISS tests passed")
        return True
        
    except Exception as e:
        print(f"\n❌ FAISS test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_local_storage():
    """Test local file storage"""
    print("\n" + "=" * 60)
    print("Testing Local File Storage")
    print("=" * 60)
    
    try:
        storage = get_file_storage()
        print(f"✓ Storage initialized at {storage.base_path}")
        
        # Test: Save image
        print("\nTest: Saving test image...")
        test_image = create_test_image()
        image_url, thumbnail_url = storage.save_artwork(test_image, artwork_id="test_artwork")
        
        print(f"✓ Image saved")
        print(f"  URL: {image_url}")
        print(f"  Thumbnail: {thumbnail_url}")
        
        # Test: Get storage stats
        print("\nTest: Getting storage stats...")
        stats = storage.get_storage_stats()
        print(f"✓ Storage stats:")
        print(f"  Total size: {stats['total_size_mb']} MB")
        print(f"  Artworks: {stats['artworks']['count']} files")
        print(f"  Thumbnails: {stats['thumbnails']['count']} files")
        
        # Test: Get image path
        print("\nTest: Retrieving image path...")
        file_path = storage.get_image_path(image_url)
        if file_path and file_path.exists():
            print(f"✓ Image found at: {file_path}")
        else:
            print(f"⚠ Image not found")
        
        print("\n✓ Local storage tests passed")
        return True
        
    except Exception as e:
        print(f"\n❌ Local storage test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def run_all_tests():
    """Run all database tests"""
    print("\n🧪 Art.Decor.AI Database Tests")
    print("=" * 60)
    print()
    
    results = {
        "Supabase": await test_supabase(),
        "FAISS": test_faiss(),
        "Local Storage": test_local_storage()
    }
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for name, passed in results.items():
        status = "✓ PASS" if passed else "❌ FAIL"
        print(f"{name:20} {status}")
    
    all_passed = all(results.values())
    
    print()
    if all_passed:
        print("✨ All tests passed! Database is ready.")
    else:
        print("⚠ Some tests failed. Check configuration above.")
    print()
    
    return all_passed


if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)

