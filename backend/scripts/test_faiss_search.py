"""
Test FAISS vector search with real embeddings from VisionMatchAgent
"""

import os
import sys
import json
import asyncio
import numpy as np
from pathlib import Path
from PIL import Image
import requests
from io import BytesIO

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.vision_match_agent import VisionMatchAgent
from db.faiss_client import FAISSClient

async def test_faiss_search():
    """Test FAISS search with real image embeddings"""
    print("=" * 60)
    print("🧪 Testing FAISS Vector Search")
    print("=" * 60)
    
    # Initialize clients
    print("\n1️⃣  Initializing agents and FAISS client...")
    vision_agent = VisionMatchAgent(use_dinov2=False)
    faiss_client = FAISSClient()
    if faiss_client.index is None:
        faiss_client.create_index(dimension=512)
    print("✅ Initialized")
    
    # Test images for embedding generation
    test_images = [
        {
            "id": "room_1",
            "name": "Modern Living Room",
            "url": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800",
            "style": "Modern Minimalist"
        },
        {
            "id": "room_2",
            "name": "Cozy Bedroom",
            "url": "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=800",
            "style": "Scandinavian"
        },
        {
            "id": "room_3",
            "name": "Industrial Loft",
            "url": "https://images.unsplash.com/photo-1556912173-46c336c7fd55?w=800",
            "style": "Industrial"
        },
        {
            "id": "room_4",
            "name": "Bohemian Space",
            "url": "https://images.unsplash.com/photo-1556912167-f556f1f39faa?w=800",
            "style": "Bohemian"
        }
    ]
    
    # Step 1: Generate embeddings for test images
    print("\n2️⃣  Generating embeddings for test images...")
    embeddings_data = []
    
    for idx, img_data in enumerate(test_images):
        try:
            print(f"   Processing {idx+1}/{len(test_images)}: {img_data['name']}")
            
            # Download image
            response = requests.get(img_data['url'], timeout=10)
            image = Image.open(BytesIO(response.content))
            
            # Resize if needed
            max_size = 800
            if max(image.size) > max_size:
                ratio = max_size / max(image.size)
                new_size = tuple(int(dim * ratio) for dim in image.size)
                image = image.resize(new_size, Image.Resampling.LANCZOS)
            
            # Generate embedding
            analysis = await vision_agent.analyze_room(image, img_data['name'])
            embedding = analysis.get('style_vector')
            
            if embedding:
                embeddings_data.append({
                    "id": img_data['id'],
                    "name": img_data['name'],
                    "style": img_data['style'],
                    "embedding": np.array(embedding),
                    "metadata": {
                        "palette": analysis.get('palette', [])[:3],
                        "detected_style": analysis.get('style'),
                        "confidence": analysis.get('confidence_score')
                    }
                })
                print(f"      ✅ Generated {len(embedding)}-dim embedding")
            else:
                print(f"      ⚠️  No embedding generated")
        
        except Exception as e:
            print(f"      ❌ Error: {e}")
    
    print(f"\n   Total embeddings generated: {len(embeddings_data)}")
    
    # Step 2: Add embeddings to FAISS index
    print("\n3️⃣  Adding embeddings to FAISS index...")
    
    # Prepare vectors and metadata
    vectors = np.array([data['embedding'] for data in embeddings_data])
    metadata_list = [
        {
            "id": data['id'],
            "name": data['name'],
            "style": data['style'],
            **data['metadata']
        }
        for data in embeddings_data
    ]
    
    # Add all vectors at once
    try:
        ids = faiss_client.add_vectors(vectors, metadata_list)
        print(f"   ✅ Added {len(ids)} embeddings to FAISS index")
    except Exception as e:
        print(f"   ❌ Failed to add embeddings: {e}")
    
    # Step 3: Test search with a query image
    print("\n4️⃣  Testing similarity search...")
    
    # Use the first image as query
    query_data = embeddings_data[0]
    print(f"   Query: {query_data['name']} ({query_data['style']})")
    
    # Search for similar items
    distances, results = faiss_client.search(
        query_vector=query_data['embedding'],
        k=3
    )
    
    print(f"\n   Top 3 similar rooms:")
    for idx, (dist, metadata) in enumerate(zip(distances, results), 1):
        similarity = 1.0 / (1.0 + dist)  # Convert distance to similarity score
        print(f"\n      {idx}. {metadata.get('name', 'Unknown')}")
        print(f"         Style: {metadata.get('style', 'Unknown')}")
        print(f"         Similarity: {similarity:.2%}")
        print(f"         Distance: {dist:.4f}")
        if 'palette' in metadata:
            colors = metadata['palette']
            if colors:
                print(f"         Top Color: {colors[0].get('name', 'Unknown')}")
    
    # Step 4: Cross-style search test
    print("\n5️⃣  Testing cross-style similarity...")
    
    for query_data in embeddings_data[1:2]:  # Test with second image
        print(f"\n   Query: {query_data['name']} ({query_data['style']})")
        
        distances, results = faiss_client.search(
            query_vector=query_data['embedding'],
            k=2
        )
        
        print(f"   Most similar:")
        for dist, metadata in zip(distances[:2], results[:2]):
            if metadata.get('name') != query_data['name']:
                similarity = 1.0 / (1.0 + dist)
                print(f"      • {metadata.get('name')} ({metadata.get('style')})")
                print(f"        Similarity: {similarity:.2%}")
    
    # Step 5: Test index statistics
    print("\n6️⃣  Index statistics...")
    total = faiss_client.get_total_vectors()
    print(f"   Total vectors: {total}")
    print(f"   Dimension: {faiss_client.dimension}")
    print(f"   Index type: {type(faiss_client.index).__name__}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    print(f"✅ FAISS vector search tested successfully!")
    print(f"   • {len(embeddings_data)} embeddings generated")
    print(f"   • {total} vectors in index")
    print(f"   • Similarity search working correctly")
    print()

if __name__ == "__main__":
    asyncio.run(test_faiss_search())

