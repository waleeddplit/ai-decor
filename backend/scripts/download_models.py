"""
Download and test AI models for Art.Decor.AI
This script downloads YOLOv8, CLIP, and optionally DINOv2 models
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def download_yolo():
    """Download YOLOv8 model"""
    print("📦 Downloading YOLOv8 model...")
    try:
        from ultralytics import YOLO
        
        # Download YOLOv8n (nano) model - fast and lightweight
        model = YOLO('yolov8n.pt')
        print("✅ YOLOv8 nano model downloaded successfully")
        
        # Test the model
        print("🧪 Testing YOLOv8 model...")
        results = model.predict(source='https://ultralytics.com/images/bus.jpg', save=False)
        print(f"✅ YOLOv8 test successful! Detected {len(results[0].boxes)} objects")
        
        # Store model path
        model_path = os.path.join(Path.home(), '.cache', 'ultralytics', 'yolov8n.pt')
        print(f"📁 Model saved at: {model_path}")
        
        return model_path
    except Exception as e:
        print(f"❌ Error downloading YOLOv8: {e}")
        return None

def download_clip():
    """Download CLIP model"""
    print("\n📦 Downloading CLIP model...")
    try:
        from transformers import CLIPModel, CLIPProcessor
        
        model_name = "openai/clip-vit-base-patch32"
        print(f"   Loading {model_name}...")
        
        # Download model and processor
        processor = CLIPProcessor.from_pretrained(model_name)
        model = CLIPModel.from_pretrained(model_name)
        
        print("✅ CLIP model downloaded successfully")
        
        # Test the model
        print("🧪 Testing CLIP model...")
        from PIL import Image
        import requests
        from io import BytesIO
        
        # Load test image
        response = requests.get('https://ultralytics.com/images/bus.jpg')
        image = Image.open(BytesIO(response.content))
        
        # Process image
        inputs = processor(images=image, return_tensors="pt", padding=True)
        image_features = model.get_image_features(**inputs)
        
        print(f"✅ CLIP test successful! Generated embedding of shape: {image_features.shape}")
        
        return model_name
    except Exception as e:
        print(f"❌ Error downloading CLIP: {e}")
        return None

def download_dinov2():
    """Download DINOv2 model (optional)"""
    print("\n📦 Downloading DINOv2 model (optional)...")
    try:
        from transformers import AutoImageProcessor, AutoModel
        
        model_name = "facebook/dinov2-base"
        print(f"   Loading {model_name}...")
        
        # Download model and processor
        processor = AutoImageProcessor.from_pretrained(model_name)
        model = AutoModel.from_pretrained(model_name)
        
        print("✅ DINOv2 model downloaded successfully")
        
        # Test the model
        print("🧪 Testing DINOv2 model...")
        from PIL import Image
        import requests
        from io import BytesIO
        
        # Load test image
        response = requests.get('https://ultralytics.com/images/bus.jpg')
        image = Image.open(BytesIO(response.content))
        
        # Process image
        inputs = processor(images=image, return_tensors="pt")
        outputs = model(**inputs)
        
        print(f"✅ DINOv2 test successful! Generated embedding of shape: {outputs.last_hidden_state.shape}")
        
        return model_name
    except Exception as e:
        print(f"⚠️  DINOv2 download skipped: {e}")
        print("   (DINOv2 is optional - CLIP will be used as fallback)")
        return None

def create_env_file(yolo_path):
    """Create .env file with model configurations"""
    print("\n📝 Creating .env file...")
    
    env_path = Path(__file__).parent.parent / '.env'
    
    # Read existing .env if it exists
    existing_vars = {}
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    existing_vars[key] = value
    
    # Update with model paths
    env_content = []
    env_content.append("# Art.Decor.AI Configuration")
    env_content.append("")
    
    # Database (preserve if exists)
    env_content.append("# Database Configuration")
    env_content.append(f"SUPABASE_URL={existing_vars.get('SUPABASE_URL', 'your_supabase_url')}")
    env_content.append(f"SUPABASE_KEY={existing_vars.get('SUPABASE_KEY', 'your_supabase_key')}")
    env_content.append("")
    
    # AI Models
    env_content.append("# AI Model Configuration")
    if yolo_path:
        env_content.append(f"YOLO_MODEL_PATH={yolo_path}")
    env_content.append("CLIP_MODEL_NAME=openai/clip-vit-base-patch32")
    env_content.append("DINOV2_MODEL_NAME=facebook/dinov2-base")
    env_content.append("USE_DINOV2=false  # Set to true to use DINOv2 instead of CLIP")
    env_content.append("")
    
    # API Keys (preserve if exists)
    env_content.append("# External API Keys")
    env_content.append(f"TAVILY_API_KEY={existing_vars.get('TAVILY_API_KEY', 'your_tavily_api_key')}")
    env_content.append(f"GOOGLE_MAPS_API_KEY={existing_vars.get('GOOGLE_MAPS_API_KEY', 'your_google_maps_api_key')}")
    env_content.append("")
    
    # Server Configuration
    env_content.append("# Server Configuration")
    env_content.append(f"HOST={existing_vars.get('HOST', '0.0.0.0')}")
    env_content.append(f"PORT={existing_vars.get('PORT', '8000')}")
    env_content.append(f"BASE_URL={existing_vars.get('BASE_URL', 'http://localhost:8000')}")
    
    # Write to file
    with open(env_path, 'w') as f:
        f.write('\n'.join(env_content))
    
    print(f"✅ .env file created at: {env_path}")
    print("   ⚠️  Remember to add your actual API keys!")

def main():
    """Main function to download all models"""
    print("=" * 60)
    print("🤖 Art.Decor.AI - Model Download Script")
    print("=" * 60)
    
    # Download models
    yolo_path = download_yolo()
    clip_model = download_clip()
    dinov2_model = download_dinov2()
    
    # Create .env file
    if yolo_path or clip_model:
        create_env_file(yolo_path)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Download Summary")
    print("=" * 60)
    print(f"YOLOv8:  {'✅ Success' if yolo_path else '❌ Failed'}")
    print(f"CLIP:    {'✅ Success' if clip_model else '❌ Failed'}")
    print(f"DINOv2:  {'✅ Success' if dinov2_model else '⚠️  Skipped (optional)'}")
    print("=" * 60)
    
    if yolo_path and clip_model:
        print("\n🎉 All required models downloaded successfully!")
        print("   You can now run the backend server with: uvicorn main:app --reload")
    else:
        print("\n⚠️  Some models failed to download. Please check the errors above.")
    
    print()

if __name__ == "__main__":
    main()

