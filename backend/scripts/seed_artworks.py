"""
Artwork seeding script
Populates database with sample artwork data and generates embeddings
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
from datetime import datetime

from db.supabase_client import get_supabase_client
from db.faiss_client import get_faiss_client
from utils.file_storage import get_file_storage


# Sample artwork data
SAMPLE_ARTWORKS = [
    {
        "title": "Abstract Geometric Canvas",
        "artist": "Modern Art Studio",
        "description": "Clean lines and neutral tones create a minimalist aesthetic perfect for contemporary spaces.",
        "price": 249.00,
        "style": "Modern",
        "tags": ["Abstract", "Geometric", "Minimalist", "Neutral"],
        "dimensions": "24x36 inches",
        "medium": "Canvas Print",
        "image_source": "https://images.unsplash.com/photo-1541961017774-22349e4a1262?w=800&h=800&fit=crop"
    },
    {
        "title": "Botanical Line Art Print",
        "artist": "Nature Studio",
        "description": "Organic shapes and muted green tones bring natural warmth while maintaining clean aesthetics.",
        "price": 129.00,
        "style": "Botanical",
        "tags": ["Botanical", "Minimalist", "Line Art", "Nature"],
        "dimensions": "18x24 inches",
        "medium": "Framed Print",
        "image_source": "https://images.unsplash.com/photo-1513519245088-0e12902e35ca?w=800&h=800&fit=crop"
    },
    {
        "title": "Sunset Watercolor",
        "artist": "Color Waves",
        "description": "Warm sunset hues add a cozy atmosphere, working beautifully with natural lighting.",
        "price": 189.00,
        "style": "Abstract",
        "tags": ["Watercolor", "Warm Tones", "Abstract", "Sunset"],
        "dimensions": "20x30 inches",
        "medium": "Watercolor Print",
        "image_source": "https://images.unsplash.com/photo-1578926375605-eaf7559b0220?w=800&h=800&fit=crop"
    },
    {
        "title": "Scandinavian Mountains",
        "artist": "Nordic Design Co.",
        "description": "Minimalist mountain landscape in muted earth tones, perfect for modern interiors.",
        "price": 179.00,
        "style": "Scandinavian",
        "tags": ["Mountains", "Minimalist", "Nature", "Earth Tones"],
        "dimensions": "24x36 inches",
        "medium": "Canvas Print",
        "image_source": "https://images.unsplash.com/photo-1464618663641-bbdd760ae84a?w=800&h=800&fit=crop"
    },
    {
        "title": "Mid-Century Modern Shapes",
        "artist": "Retro Revival",
        "description": "Vibrant geometric shapes inspired by 1960s design, adding playful energy to any room.",
        "price": 159.00,
        "style": "Mid-Century Modern",
        "tags": ["Geometric", "Colorful", "Retro", "Playful"],
        "dimensions": "20x20 inches",
        "medium": "Canvas Print",
        "image_source": "https://images.unsplash.com/photo-1549887534-1541e9326642?w=800&h=800&fit=crop"
    },
    {
        "title": "Minimalist Line Portrait",
        "artist": "Simple Lines Studio",
        "description": "Single continuous line forming an elegant portrait, embodying minimalist sophistication.",
        "price": 99.00,
        "style": "Minimalist",
        "tags": ["Line Art", "Portrait", "Black and White", "Simple"],
        "dimensions": "16x20 inches",
        "medium": "Framed Print",
        "image_source": "https://images.unsplash.com/photo-1547826039-bfc35e0f1ea8?w=800&h=800&fit=crop"
    },
    {
        "title": "Tropical Palm Leaves",
        "artist": "Jungle Vibes",
        "description": "Lush green palm leaves bringing tropical energy and natural vibrancy indoors.",
        "price": 139.00,
        "style": "Tropical",
        "tags": ["Botanical", "Green", "Tropical", "Nature"],
        "dimensions": "24x32 inches",
        "medium": "Canvas Print",
        "image_source": "https://images.unsplash.com/photo-1509114397022-ed747cca3f65?w=800&h=800&fit=crop"
    },
    {
        "title": "Abstract Blue Waves",
        "artist": "Ocean Art Collective",
        "description": "Flowing blue waves creating a calming, meditative atmosphere with coastal vibes.",
        "price": 199.00,
        "style": "Abstract",
        "tags": ["Abstract", "Blue", "Waves", "Coastal"],
        "dimensions": "30x40 inches",
        "medium": "Canvas Print",
        "image_source": "https://images.unsplash.com/photo-1549887534-1541e9326642?w=800&h=800&fit=crop"
    },
    {
        "title": "Bohemian Mandala",
        "artist": "Boho Art House",
        "description": "Intricate mandala patterns with warm earthy tones for a bohemian aesthetic.",
        "price": 149.00,
        "style": "Bohemian",
        "tags": ["Mandala", "Bohemian", "Pattern", "Earth Tones"],
        "dimensions": "24x24 inches",
        "medium": "Canvas Print",
        "image_source": "https://images.unsplash.com/photo-1513569771920-c9e1d31714af?w=800&h=800&fit=crop"
    },
    {
        "title": "Black and White Architecture",
        "artist": "Urban Lens",
        "description": "Striking architectural photography showcasing geometric patterns and bold contrast.",
        "price": 219.00,
        "style": "Contemporary",
        "tags": ["Photography", "Architecture", "Black and White", "Modern"],
        "dimensions": "24x36 inches",
        "medium": "Framed Print",
        "image_source": "https://images.unsplash.com/photo-1487958449943-2429e8be8625?w=800&h=800&fit=crop"
    }
]


def create_placeholder_image(title: str, artist: str, size=(800, 800)) -> Image.Image:
    """Create a placeholder image with artwork info"""
    img = Image.new('RGB', size, color=(240, 240, 245))
    draw = ImageDraw.Draw(img)
    
    # Add text
    text_y = size[1] // 2 - 50
    draw.text((size[0]//2, text_y), title, fill=(100, 100, 100), anchor="mm")
    draw.text((size[0]//2, text_y + 40), f"by {artist}", fill=(150, 150, 150), anchor="mm")
    
    return img


def download_image(url: str, fallback_title: str, fallback_artist: str) -> Image.Image:
    """Download image from URL or create placeholder"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
    except Exception as e:
        print(f"  ⚠ Could not download image: {e}")
    
    # Create placeholder
    return create_placeholder_image(fallback_title, fallback_artist)


def generate_mock_embedding(text: str, dimension: int = 512) -> np.ndarray:
    """
    Generate a mock embedding based on text
    In production, this would use CLIP model
    """
    # Use text hash as seed for reproducibility
    seed = abs(hash(text)) % (2**32)
    np.random.seed(seed)
    
    # Generate random embedding
    embedding = np.random.randn(dimension).astype(np.float32)
    
    # Normalize
    embedding = embedding / np.linalg.norm(embedding)
    
    return embedding


async def seed_artworks():
    """Main seeding function"""
    print("🎨 Starting artwork seeding...")
    print(f"   Artworks to seed: {len(SAMPLE_ARTWORKS)}")
    print()
    
    # Initialize clients (skip Supabase for now)
    supabase = None
    try:
        supabase = get_supabase_client()
        print("✓ Supabase client initialized")
    except Exception as e:
        print(f"⚠ Supabase not available (skipping database): {e}")
        print("  → Will only populate FAISS for recommendations")
    
    try:
        faiss = get_faiss_client()
        print(f"✓ FAISS client initialized ({faiss.get_total_vectors()} existing vectors)")
    except Exception as e:
        print(f"❌ Could not initialize FAISS: {e}")
        return
    
    try:
        storage = get_file_storage()
        print(f"✓ Local storage initialized")
    except Exception as e:
        print(f"❌ Could not initialize storage: {e}")
        return
    
    print()
    
    # Process each artwork
    embeddings_list = []
    metadata_list = []
    
    for idx, artwork_data in enumerate(SAMPLE_ARTWORKS, 1):
        print(f"[{idx}/{len(SAMPLE_ARTWORKS)}] Processing: {artwork_data['title']}")
        
        try:
            # Download or create image
            print(f"  → Downloading image...")
            image = download_image(
                artwork_data['image_source'],
                artwork_data['title'],
                artwork_data['artist']
            )
            
            # Save to local storage
            print(f"  → Saving to local storage...")
            image_url, thumbnail_url = storage.save_artwork(image)
            
            # Generate embedding
            print(f"  → Generating embedding...")
            text_for_embedding = f"{artwork_data['title']} {artwork_data['artist']} {artwork_data['style']} {' '.join(artwork_data['tags'])}"
            embedding = generate_mock_embedding(text_for_embedding)
            
            # Generate artwork ID
            artwork_id = f"artwork_{idx}"
            
            # Try to insert into Supabase (if available)
            if supabase:
                try:
                    print(f"  → Inserting into Supabase...")
                    artwork_record = {
                        "title": artwork_data["title"],
                        "artist": artwork_data["artist"],
                        "description": artwork_data["description"],
                        "price": artwork_data["price"],
                        "image_url": image_url,
                        "thumbnail_url": thumbnail_url,
                        "style": artwork_data["style"],
                        "tags": artwork_data["tags"],
                        "dimensions": artwork_data["dimensions"],
                        "medium": artwork_data["medium"],
                        "embedding": embedding.tolist(),
                        "is_available": True
                    }
                    # Note: This would use: supabase.client.table("artworks").insert()
                    # Skipping for now since tables don't exist
                    print(f"  ⚠ Skipping Supabase (tables not created)")
                except Exception as e:
                    print(f"  ⚠ Supabase insert failed: {e}")
            
            # Collect for FAISS (this is what we need!)
            embeddings_list.append(embedding)
            metadata_list.append({
                "id": artwork_id,
                "title": artwork_data["title"],
                "artist": artwork_data["artist"],
                "style": artwork_data["style"],
                "price": artwork_data["price"],
                "image_url": image_url,
                "thumbnail_url": thumbnail_url,
                "tags": artwork_data["tags"],
                "dimensions": artwork_data["dimensions"],
                "medium": artwork_data["medium"]
            })
            
            print(f"  ✓ Successfully processed")
            print()
            
        except Exception as e:
            print(f"  ❌ Error processing artwork: {e}")
            print()
            continue
    
    # Add embeddings to FAISS
    if embeddings_list:
        print(f"📊 Adding {len(embeddings_list)} embeddings to FAISS...")
        try:
            embeddings_array = np.array(embeddings_list)
            faiss.add_vectors(embeddings_array, metadata_list)
            faiss.save_index()
            print(f"✓ FAISS index updated ({faiss.get_total_vectors()} total vectors)")
        except Exception as e:
            print(f"❌ Error adding to FAISS: {e}")
    
    # Print summary
    print()
    print("=" * 60)
    print("✨ Seeding Complete!")
    print("=" * 60)
    print(f"Artworks processed: {len(embeddings_list)}/{len(SAMPLE_ARTWORKS)}")
    print(f"FAISS vectors: {faiss.get_total_vectors()}")
    
    # Storage stats
    stats = storage.get_storage_stats()
    print(f"Storage used: {stats['total_size_mb']} MB")
    print(f"  - Artworks: {stats['artworks']['count']} files ({stats['artworks']['size_mb']} MB)")
    print(f"  - Thumbnails: {stats['thumbnails']['count']} files ({stats['thumbnails']['size_mb']} MB)")
    print()


if __name__ == "__main__":
    asyncio.run(seed_artworks())

