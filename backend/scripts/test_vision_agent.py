"""
Test the VisionMatchAgent with real images
"""

import os
import sys
import json
from pathlib import Path
from PIL import Image
import requests
from io import BytesIO
import time
import asyncio

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.vision_match_agent import VisionMatchAgent

async def test_vision_agent():
    """Test VisionMatchAgent with various room images"""
    print("=" * 60)
    print("🧪 Testing VisionMatchAgent")
    print("=" * 60)
    
    # Initialize agent
    print("\n1️⃣  Initializing VisionMatchAgent...")
    try:
        agent = VisionMatchAgent(use_dinov2=False)  # Use CLIP
        print("✅ Agent initialized successfully with CLIP")
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        return
    
    # Test images (using public URLs)
    test_images = [
        {
            "name": "Modern Living Room",
            "url": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800",
            "description": "Modern minimalist living room with white walls and contemporary furniture"
        },
        {
            "name": "Cozy Bedroom",
            "url": "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=800",
            "description": "Cozy bedroom with warm lighting and comfortable bedding"
        },
        {
            "name": "Kitchen Interior",
            "url": "https://images.unsplash.com/photo-1556912173-46c336c7fd55?w=800",
            "description": "Contemporary kitchen with wooden cabinets"
        }
    ]
    
    results = []
    
    for idx, test_case in enumerate(test_images, 1):
        print(f"\n{idx}️⃣  Testing: {test_case['name']}")
        print(f"   URL: {test_case['url']}")
        print(f"   Description: {test_case['description']}")
        
        try:
            # Download image
            print("   📥 Downloading image...")
            response = requests.get(test_case['url'], timeout=10)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
            
            # Resize if too large (for faster processing)
            max_size = 1024
            if max(image.size) > max_size:
                ratio = max_size / max(image.size)
                new_size = tuple(int(dim * ratio) for dim in image.size)
                image = image.resize(new_size, Image.Resampling.LANCZOS)
            
            print(f"   📐 Image size: {image.size}")
            
            # Analyze room
            print("   🔍 Analyzing room...")
            start_time = time.time()
            analysis = await agent.analyze_room(image, test_case['description'])
            processing_time = time.time() - start_time
            
            # Display results
            print(f"   ⏱️  Processing time: {processing_time:.2f}s")
            print(f"\n   📊 Analysis Results:")
            print(f"      Style: {analysis.get('style', 'Unknown')}")
            print(f"      Confidence: {analysis.get('confidence_score', 0):.2%}")
            print(f"      Detected Objects: {len(analysis.get('detected_objects', []))}")
            
            # Color palette
            palette = analysis.get('palette', [])
            print(f"      Color Palette ({len(palette)} colors):")
            for color in palette[:3]:  # Show top 3
                print(f"         - {color['name']}: {color['hex']} ({color['percentage']:.1f}%)")
            
            # Lighting
            lighting = analysis.get('lighting', {})
            print(f"      Lighting:")
            print(f"         - Type: {lighting.get('type', 'Unknown')}")
            brightness = lighting.get('brightness', 0)
            if isinstance(brightness, (int, float)):
                print(f"         - Brightness: {brightness:.2f}")
            else:
                print(f"         - Brightness: {brightness}")
            temperature = lighting.get('temperature', 'Unknown')
            print(f"         - Temperature: {temperature}")
            
            # Style vector
            style_vector = analysis.get('style_vector', [])
            if style_vector:
                print(f"      Style Vector: {len(style_vector)} dimensions")
            
            print(f"   ✅ Test passed!")
            
            results.append({
                "test": test_case['name'],
                "success": True,
                "processing_time": processing_time,
                "analysis": analysis
            })
            
        except Exception as e:
            print(f"   ❌ Test failed: {e}")
            results.append({
                "test": test_case['name'],
                "success": False,
                "error": str(e)
            })
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    successful = sum(1 for r in results if r['success'])
    total = len(results)
    
    print(f"Total Tests: {total}")
    print(f"Passed: {successful}")
    print(f"Failed: {total - successful}")
    print(f"Success Rate: {successful/total*100:.1f}%")
    
    if successful > 0:
        avg_time = sum(r['processing_time'] for r in results if r['success']) / successful
        print(f"Average Processing Time: {avg_time:.2f}s")
    
    # Save detailed results
    results_path = Path(__file__).parent.parent / "test_results_vision.json"
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n💾 Detailed results saved to: {results_path}")
    
    if successful == total:
        print("\n🎉 All tests passed!")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
    
    print()

async def test_with_dinov2():
    """Test with DINOv2 instead of CLIP"""
    print("=" * 60)
    print("🧪 Testing VisionMatchAgent with DINOv2")
    print("=" * 60)
    
    try:
        agent = VisionMatchAgent(use_dinov2=True)
        print("✅ Agent initialized successfully with DINOv2")
        
        # Quick test
        print("\n🔍 Quick test with sample image...")
        url = "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800"
        response = requests.get(url, timeout=10)
        image = Image.open(BytesIO(response.content))
        
        analysis = await agent.analyze_room(image, "Test room")
        
        style_vector = analysis.get('style_vector', [])
        print(f"✅ DINOv2 test passed! Style vector: {len(style_vector)} dimensions")
        
    except Exception as e:
        print(f"⚠️  DINOv2 test skipped: {e}")
        print("   (This is OK - CLIP is the default and primary model)")

async def main():
    """Main async function"""
    # Test with CLIP (default)
    await test_vision_agent()
    
    # Test with DINOv2 (optional)
    print("\n")
    await test_with_dinov2()

if __name__ == "__main__":
    asyncio.run(main())

