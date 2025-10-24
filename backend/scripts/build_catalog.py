#!/usr/bin/env python3
"""
Build Local Catalog from Unsplash
Fetches 50 diverse artworks and saves to data/local_catalog.json
"""

import asyncio
import httpx
import json
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()


async def fetch_unsplash_catalog():
    """Fetch 50 diverse artworks from Unsplash for local catalog"""
    
    access_key = os.getenv('UNSPLASH_ACCESS_KEY')
    if not access_key:
        print('❌ UNSPLASH_ACCESS_KEY not found in .env')
        return []
    
    print('🎨 Fetching artwork from Unsplash...')
    print('📊 Using 10 API requests to get 50 artworks (5 per request)')
    print('')
    
    # Different art styles to get diversity (10 queries × 5 results = 50 artworks)
    queries = [
        'abstract art',
        'minimalist poster',
        'geometric art',
        'nature landscape',
        'contemporary art',
        'modern architecture',
        'floral botanical',
        'ocean waves',
        'mountain landscape',
        'urban photography'
    ]
    
    catalog = []
    client = httpx.AsyncClient(timeout=30.0)
    
    try:
        for i, query in enumerate(queries, 1):
            print(f'  [{i}/10] Fetching: {query}...')
            
            url = 'https://api.unsplash.com/search/photos'
            headers = {'Authorization': f'Client-ID {access_key}'}
            params = {
                'query': query + ' wall art',
                'per_page': 5,
                'orientation': 'landscape'
            }
            
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            for photo in data.get('results', []):
                title = photo.get('alt_description') or photo.get('description') or f'{query.title()} Artwork'
                # Clean up title
                if len(title) > 80:
                    title = title[:77] + '...'
                
                catalog.append({
                    'id': f'local_catalog_{photo["id"]}',
                    'title': title.title(),
                    'artist': photo.get('user', {}).get('name', 'Unsplash Artist'),
                    'price': 'FREE Download',
                    'category': query.replace(' ', '_'),
                    'image_url': photo.get('urls', {}).get('regular'),
                    'thumbnail_url': photo.get('urls', {}).get('small'),
                    'download_url': photo.get('links', {}).get('download'),
                    'attribution': f'Photo by {photo.get("user", {}).get("name", "Unknown")} on Unsplash',
                    'attribution_url': photo.get('links', {}).get('html'),
                    'description': f'High-quality {query} - Free to download. Print on demand available.',
                    'tags': query.split() + [tag.get('title', '') for tag in photo.get('tags', [])[:3]],
                    'colors': [photo.get('color', '#CCCCCC')],
                    'width': photo.get('width', 3000),
                    'height': photo.get('height', 2000),
                    'source': 'Local Catalog',
                    'print_services': [
                        {'name': 'Printful', 'url': 'https://www.printful.com/', 'price_from': '$25'},
                        {'name': 'Printify', 'url': 'https://printify.com/', 'price_from': '$20'},
                        {'name': 'Redbubble', 'url': 'https://www.redbubble.com/', 'price_from': '$15'}
                    ]
                })
            
            # Avoid rate limiting
            await asyncio.sleep(0.5)
    
    except Exception as e:
        print(f'❌ Error: {e}')
        import traceback
        traceback.print_exc()
    finally:
        await client.aclose()
    
    print('')
    print(f'✅ Fetched {len(catalog)} artworks')
    return catalog


async def main():
    """Main function"""
    catalog = await fetch_unsplash_catalog()
    
    if catalog:
        # Save to JSON file
        output_dir = Path(__file__).parent.parent / 'data'
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / 'local_catalog.json'
        
        with open(output_file, 'w') as f:
            json.dump(catalog, f, indent=2)
        
        print(f'💾 Saved to: {output_file}')
        print(f'📊 Total artworks: {len(catalog)}')
        print(f'📂 Categories: {len(set(item["category"] for item in catalog))}')
        
        # Show sample
        print('')
        print('📸 Sample artworks:')
        for item in catalog[:3]:
            print(f'  • {item["title"]} by {item["artist"]}')
        
        print('')
        print('✅ Local catalog built successfully!')
        return True
    else:
        print('❌ Failed to fetch catalog')
        return False


if __name__ == '__main__':
    success = asyncio.run(main())
    sys.exit(0 if success else 1)

