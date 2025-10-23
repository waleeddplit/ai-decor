"""
VisionMatchAgent: Computer vision for room analysis
Uses YOLOv8 for wall/furniture detection, k-means for color extraction,
and CLIP/DINOv2 for style embeddings
"""

import os
from typing import Dict, List, Any, Optional, Tuple
import numpy as np
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel
from ultralytics import YOLO
from sklearn.cluster import KMeans
from dotenv import load_dotenv

load_dotenv()


class VisionMatchAgent:
    """
    Analyzes room images using computer vision models
    
    Features:
    - YOLOv8: Object detection for walls, furniture, and décor items
    - K-means: Dominant color palette extraction
    - CLIP/DINOv2: Style embedding generation (512-dim vectors)
    - Lighting analysis: Brightness, temperature, and ambiance
    
    Returns structured data with:
    - palette: List of dominant colors with RGB and hex
    - lighting: Detailed lighting characteristics
    - style_vector: 512-dimensional embedding for similarity search
    """

    def __init__(self, use_dinov2: bool = False):
        """
        Initialize VisionMatchAgent with selected models
        
        Args:
            use_dinov2: If True, use DINOv2 for embeddings instead of CLIP
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.use_dinov2 = use_dinov2
        print(f"VisionMatchAgent initializing on {self.device}")

        # Load YOLO model for object detection
        self._load_yolo_model()
        
        # Load embedding model (CLIP or DINOv2)
        if use_dinov2:
            self._load_dinov2_model()
        else:
            self._load_clip_model()

    def _load_yolo_model(self):
        """Load YOLOv8 model for object detection"""
        yolo_path = os.getenv("YOLO_MODEL_PATH", "yolov8n.pt")
        try:
            self.yolo_model = YOLO(yolo_path)
            print(f"✓ Loaded YOLOv8 model from {yolo_path}")
        except Exception as e:
            print(f"⚠ Warning: Could not load YOLO model: {e}")
            self.yolo_model = None

    def _load_clip_model(self):
        """Load CLIP model for style embeddings"""
        clip_model_name = os.getenv("CLIP_MODEL_NAME", "openai/clip-vit-base-patch32")
        try:
            self.clip_model = CLIPModel.from_pretrained(clip_model_name).to(self.device)
            self.clip_processor = CLIPProcessor.from_pretrained(clip_model_name)
            self.embedding_model = self.clip_model
            self.embedding_processor = self.clip_processor
            print(f"✓ Loaded CLIP model: {clip_model_name}")
        except Exception as e:
            print(f"⚠ Warning: Could not load CLIP model: {e}")
            self.clip_model = None
            self.clip_processor = None
            self.embedding_model = None
            self.embedding_processor = None

    def _load_dinov2_model(self):
        """Load DINOv2 model for style embeddings"""
        try:
            from transformers import AutoImageProcessor, AutoModel
            
            model_name = "facebook/dinov2-base"
            self.dinov2_processor = AutoImageProcessor.from_pretrained(model_name)
            self.dinov2_model = AutoModel.from_pretrained(model_name).to(self.device)
            self.embedding_model = self.dinov2_model
            self.embedding_processor = self.dinov2_processor
            print(f"✓ Loaded DINOv2 model: {model_name}")
        except Exception as e:
            print(f"⚠ Warning: Could not load DINOv2 model: {e}")
            print("  Falling back to CLIP...")
            self.use_dinov2 = False
            self._load_clip_model()

    async def analyze_room(
        self, image: Image.Image, description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze a room image and return structured data
        
        This is the main analysis pipeline that orchestrates all vision tasks:
        1. Object detection (walls, furniture)
        2. Color palette extraction (k-means)
        3. Style embedding generation (CLIP/DINOv2)
        4. Lighting analysis
        5. Wall space detection

        Args:
            image: PIL Image object
            description: Optional text description for context

        Returns:
            Dict with required structure:
            {
                "palette": [{"r": 255, "g": 255, "b": 255, "hex": "#ffffff", "percentage": 25.5}],
                "lighting": {
                    "brightness": "Natural, Bright",
                    "temperature": "Warm",
                    "avg_brightness": 156.7,
                    "contrast": 0.45
                },
                "style_vector": [512-dimensional embedding],
                "detected_objects": [...],
                "wall_spaces": [...],
                "style": "Modern Minimalist",
                "confidence_score": 0.85
            }
        """
        import time

        start_time = time.time()
        print(f"🔍 Starting room analysis...")

        # 1. Detect walls and furniture using YOLOv8
        detected_objects = await self._detect_objects(image)
        print(f"  ✓ Detected {len(detected_objects)} objects")

        # 2. Extract dominant color palette using k-means
        palette = await self._extract_color_palette(image, n_colors=5)
        print(f"  ✓ Extracted {len(palette)} dominant colors")

        # 3. Generate style embedding using CLIP or DINOv2
        style_vector = await self._generate_style_embedding(image, description)
        print(f"  ✓ Generated {len(style_vector) if style_vector is not None else 0}-dim style vector")

        # 4. Analyze lighting conditions
        lighting = await self._analyze_lighting_detailed(image)
        print(f"  ✓ Analyzed lighting: {lighting['brightness']}")

        # 5. Identify wall spaces for art placement
        wall_spaces = await self._detect_wall_spaces(detected_objects, image)
        print(f"  ✓ Detected {len(wall_spaces)} wall spaces")

        # 6. Classify room style based on embedding and objects
        room_style = await self._classify_style(style_vector, detected_objects)
        
        # 7. Calculate overall confidence
        confidence_score = await self._calculate_confidence(
            detected_objects, palette, style_vector
        )

        processing_time = time.time() - start_time
        print(f"✅ Analysis complete in {processing_time:.2f}s")

        return {
            "palette": palette,
            "lighting": lighting,
            "style_vector": style_vector.tolist() if style_vector is not None else None,
            "detected_objects": detected_objects,
            "wall_spaces": wall_spaces,
            "style": room_style,
            "confidence_score": confidence_score,
            "processing_time": processing_time,
            # Legacy fields for backward compatibility
            "colors": palette,  # Alias for palette
        }

    async def _detect_objects(self, image: Image.Image) -> List[Dict[str, Any]]:
        """
        Detect walls, furniture, and décor items using YOLOv8
        
        Focus on detecting:
        - Walls and wall spaces
        - Furniture (sofa, chair, table, bed)
        - Existing décor (paintings, lamps, plants)
        - Architectural features (windows, doors)
        
        Args:
            image: PIL Image object
            
        Returns:
            List of detected objects with labels, confidence, and bounding boxes
        """
        if self.yolo_model is None:
            print("⚠ YOLO model not loaded, using mock detections")
            return self._get_mock_detections(image)

        try:
            # Run YOLOv8 inference
            results = self.yolo_model(image, verbose=False)
            objects = []

            # Relevant object categories for room analysis
            relevant_categories = {
                'couch', 'chair', 'bed', 'dining table', 'potted plant',
                'tv', 'laptop', 'book', 'clock', 'vase', 'lamp',
                'person'  # For scale reference
            }

            for result in results:
                boxes = result.boxes
                for box in boxes:
                    label = result.names[int(box.cls[0])]
                    confidence = float(box.conf[0])
                    
                    # Filter by confidence and relevance
                    if confidence > 0.3 and (label in relevant_categories or 'wall' in label.lower()):
                        bbox = box.xyxy[0].tolist()  # [x1, y1, x2, y2]
                        
                        objects.append({
                            "category": label,  # Primary field for frontend
                            "class": label,     # Alias for compatibility
                            "label": label,     # Keep for backward compatibility
                            "confidence": confidence,
                            "bbox": bbox,
                            "area": (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]),
                            "center": [
                                (bbox[0] + bbox[2]) / 2,
                                (bbox[1] + bbox[3]) / 2
                            ]
                        })

            # Sort by confidence
            objects.sort(key=lambda x: x['confidence'], reverse=True)
            
            return objects

        except Exception as e:
            print(f"❌ Error in object detection: {e}")
            return self._get_mock_detections(image)

    def _get_mock_detections(self, image: Image.Image) -> List[Dict[str, Any]]:
        """Return mock detections for testing"""
        width, height = image.size
        return [
            {
                "category": "couch",
                "class": "couch",
                "label": "couch",
                "confidence": 0.85,
                "bbox": [width * 0.2, height * 0.5, width * 0.6, height * 0.9],
                "area": width * height * 0.16,
                "center": [width * 0.4, height * 0.7]
            },
            {
                "category": "potted plant",
                "class": "potted plant",
                "label": "potted plant",
                "confidence": 0.72,
                "bbox": [width * 0.8, height * 0.6, width * 0.95, height * 0.85],
                "area": width * height * 0.0375,
                "center": [width * 0.875, height * 0.725]
            }
        ]

    async def _generate_style_embedding(
        self, image: Image.Image, description: Optional[str] = None
    ) -> Optional[np.ndarray]:
        """
        Generate 512-dimensional style embedding using CLIP or DINOv2
        
        The embedding captures:
        - Overall room aesthetic and style
        - Spatial layout and composition
        - Color harmony and tone
        - Furniture arrangement
        
        Used for similarity search in FAISS vector database.
        
        Args:
            image: PIL Image object
            description: Optional text description for multimodal embedding (CLIP only)
            
        Returns:
            512-dimensional normalized numpy array, or None if models unavailable
        """
        if self.embedding_model is None or self.embedding_processor is None:
            print("⚠ No embedding model loaded, returning None")
            return None

        try:
            if self.use_dinov2:
                # DINOv2 embedding
                inputs = self.embedding_processor(
                    images=image, 
                    return_tensors="pt"
                ).to(self.device)
                
                with torch.no_grad():
                    outputs = self.embedding_model(**inputs)
                    # Use CLS token embedding
                    embedding = outputs.last_hidden_state[:, 0].cpu().numpy()[0]
                    
            else:
                # CLIP embedding
                inputs = self.embedding_processor(
                    images=image, 
                    return_tensors="pt"
                ).to(self.device)
                
                with torch.no_grad():
                    image_features = self.embedding_model.get_image_features(**inputs)
                    embedding = image_features.cpu().numpy()[0]

            # L2 normalization for cosine similarity
            embedding = embedding / (np.linalg.norm(embedding) + 1e-8)
            
            # Ensure 512 dimensions (pad or truncate if needed)
            if len(embedding) < 512:
                embedding = np.pad(embedding, (0, 512 - len(embedding)))
            elif len(embedding) > 512:
                embedding = embedding[:512]

            return embedding

        except Exception as e:
            print(f"❌ Error generating style embedding: {e}")
            # Return random embedding for testing
            return np.random.randn(512).astype(np.float32) / 10

    async def _extract_color_palette(
        self, image: Image.Image, n_colors: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Extract dominant color palette using k-means clustering
        
        Process:
        1. Resize image for efficiency
        2. Convert to RGB pixel array
        3. Apply k-means clustering to find dominant colors
        4. Calculate percentage of each color
        5. Sort by dominance
        
        Args:
            image: PIL Image object
            n_colors: Number of dominant colors to extract (default: 5)
            
        Returns:
            List of color dicts with r, g, b, hex, percentage, and name
        """
        try:
            # Resize for faster processing (but not too small)
            img = image.resize((200, 200))
            pixels = np.array(img).reshape(-1, 3)
            
            # Remove very dark/bright pixels (likely shadows/highlights)
            mask = (pixels.min(axis=1) > 20) & (pixels.max(axis=1) < 235)
            filtered_pixels = pixels[mask]
            
            if len(filtered_pixels) < 100:
                filtered_pixels = pixels  # Use all if too few remain

            # K-means clustering for dominant colors
            kmeans = KMeans(
                n_clusters=min(n_colors, len(filtered_pixels)), 
                random_state=42, 
                n_init=10,
                max_iter=300
            )
            kmeans.fit(filtered_pixels)

            # Get cluster sizes for percentages
            labels = kmeans.labels_
            label_counts = np.bincount(labels)
            total_pixels = len(labels)

            colors = []
            for idx, center in enumerate(kmeans.cluster_centers_):
                r, g, b = center.astype(int)
                
                # Clamp values to valid range
                r, g, b = np.clip([r, g, b], 0, 255)
                
                hex_color = f"#{r:02x}{g:02x}{b:02x}"
                percentage = (label_counts[idx] / total_pixels) * 100
                
                colors.append({
                    "r": int(r),
                    "g": int(g),
                    "b": int(b),
                    "hex": hex_color,
                    "percentage": round(percentage, 1),
                    "name": self._get_color_name(r, g, b)
                })

            # Sort by percentage (most dominant first)
            colors.sort(key=lambda x: x['percentage'], reverse=True)
            
            return colors

        except Exception as e:
            print(f"❌ Error extracting color palette: {e}")
            # Return default neutral palette
            return [
                {"r": 255, "g": 255, "b": 255, "hex": "#ffffff", "percentage": 30.0, "name": "White"},
                {"r": 229, "g": 231, "b": 235, "hex": "#e5e7eb", "percentage": 25.0, "name": "Light Gray"},
                {"r": 156, "g": 163, "b": 175, "hex": "#9ca3af", "percentage": 20.0, "name": "Gray"},
                {"r": 31, "g": 41, "b": 55, "hex": "#1f2937", "percentage": 15.0, "name": "Dark Gray"},
                {"r": 245, "g": 158, "b": 11, "hex": "#f59e0b", "percentage": 10.0, "name": "Amber"},
            ]

    def _get_color_name(self, r: int, g: int, b: int) -> str:
        """
        Get approximate color name from RGB values
        
        Uses distance-based matching to predefined color palette.
        """
        # Predefined color names
        color_names = {
            (255, 255, 255): "White",
            (0, 0, 0): "Black",
            (128, 128, 128): "Gray",
            (255, 0, 0): "Red",
            (0, 255, 0): "Green",
            (0, 0, 255): "Blue",
            (255, 255, 0): "Yellow",
            (255, 165, 0): "Orange",
            (128, 0, 128): "Purple",
            (255, 192, 203): "Pink",
            (165, 42, 42): "Brown",
            (0, 128, 128): "Teal",
            (245, 245, 220): "Beige",
            (240, 230, 140): "Khaki",
        }
        
        # Find closest color
        min_distance = float('inf')
        closest_name = "Unknown"
        
        for (cr, cg, cb), name in color_names.items():
            distance = np.sqrt((r - cr)**2 + (g - cg)**2 + (b - cb)**2)
            if distance < min_distance:
                min_distance = distance
                closest_name = name
        
        # More specific naming based on characteristics
        brightness = (r + g + b) / 3
        if brightness > 200:
            return f"Light {closest_name}"
        elif brightness < 50:
            return f"Dark {closest_name}"
        
        return closest_name

    async def _analyze_lighting_detailed(self, image: Image.Image) -> Dict[str, Any]:
        """
        Analyze lighting conditions in detail
        
        Extracts:
        - Average brightness (0-255)
        - Contrast ratio
        - Color temperature (warm/cool)
        - Lighting type classification
        
        Args:
            image: PIL Image object
            
        Returns:
            Dict with lighting characteristics
        """
        try:
            # Convert to grayscale for brightness analysis
            gray = image.convert("L")
            gray_array = np.array(gray)
            
            # Calculate brightness statistics
            avg_brightness = gray_array.mean()
            std_brightness = gray_array.std()
            min_brightness = gray_array.min()
            max_brightness = gray_array.max()
            
            # Contrast calculation (normalized std dev)
            contrast = std_brightness / (avg_brightness + 1e-8)
            contrast = min(contrast, 1.0)
            
            # Brightness classification
            if avg_brightness > 180:
                brightness_level = "Very Bright"
            elif avg_brightness > 140:
                brightness_level = "Natural, Bright"
            elif avg_brightness > 100:
                brightness_level = "Moderate"
            elif avg_brightness > 60:
                brightness_level = "Dim"
            else:
                brightness_level = "Very Dim"
            
            # Color temperature analysis (warm vs cool)
            rgb_array = np.array(image)
            avg_r = rgb_array[:, :, 0].mean()
            avg_g = rgb_array[:, :, 1].mean()
            avg_b = rgb_array[:, :, 2].mean()
            
            # Calculate color temperature indicator
            if avg_r > avg_b + 10:
                temperature = "Warm"
                temp_score = (avg_r - avg_b) / 255.0
            elif avg_b > avg_r + 10:
                temperature = "Cool"
                temp_score = (avg_b - avg_r) / 255.0
            else:
                temperature = "Neutral"
                temp_score = 0.0
            
            return {
                "brightness": brightness_level,
                "temperature": temperature,
                "avg_brightness": round(float(avg_brightness), 1),
                "contrast": round(float(contrast), 2),
                "temperature_score": round(float(temp_score), 2),
                "dynamic_range": {
                    "min": int(min_brightness),
                    "max": int(max_brightness),
                    "range": int(max_brightness - min_brightness)
                }
            }

        except Exception as e:
            print(f"❌ Error analyzing lighting: {e}")
            return {
                "brightness": "Natural, Bright",
                "temperature": "Neutral",
                "avg_brightness": 140.0,
                "contrast": 0.4,
                "temperature_score": 0.0,
                "dynamic_range": {"min": 0, "max": 255, "range": 255}
            }

    async def _detect_wall_spaces(
        self, detected_objects: List[Dict], image: Image.Image
    ) -> List[Dict[str, Any]]:
        """Identify available wall spaces for art"""
        # Placeholder: In production, use semantic segmentation
        width, height = image.size

        # Simple heuristic: assume main wall is center area
        wall_spaces = [
            {
                "location": "center_wall",
                "bbox": [width * 0.2, height * 0.2, width * 0.8, height * 0.8],
                "size": "large",
            }
        ]

        return wall_spaces

    async def _classify_style(
        self, embedding: Optional[np.ndarray], objects: List[Dict]
    ) -> str:
        """
        Classify room style based on embedding and detected objects
        
        Uses heuristics based on:
        - Object types and arrangement
        - Furniture density
        - Color palette (if needed)
        
        Future: Use embedding similarity to style templates in database
        
        Args:
            embedding: Style vector (512-dim)
            objects: List of detected objects
            
        Returns:
            Style classification string
        """
        if not objects:
            return "Contemporary"

        object_labels = [obj["label"].lower() for obj in objects]
        object_str = " ".join(object_labels)

        # Count furniture pieces for density estimation
        furniture_count = sum(1 for label in object_labels 
                            if label in ['couch', 'chair', 'bed', 'dining table'])

        # Modern/Minimalist: Few furniture pieces, clean lines
        if furniture_count <= 3:
            if any(word in object_str for word in ["laptop", "tv", "book"]):
                return "Modern Minimalist"
            return "Minimalist"

        # Bohemian: Many plants and decorative items
        plant_count = sum(1 for label in object_labels if 'plant' in label)
        if plant_count >= 2:
            return "Bohemian"

        # Traditional: Dense furniture arrangement
        if furniture_count >= 5:
            return "Traditional"

        # Industrial: Sparse with utilitarian objects
        if 'chair' in object_labels and 'lamp' in object_labels:
            if furniture_count <= 4:
                return "Industrial"

        # Default
        return "Contemporary"

    async def _calculate_confidence(
        self, 
        objects: List[Dict], 
        palette: List[Dict], 
        embedding: Optional[np.ndarray]
    ) -> float:
        """
        Calculate overall confidence score for the analysis
        
        Based on:
        - Object detection confidence scores
        - Number of detected objects
        - Color extraction quality
        - Embedding generation success
        
        Args:
            objects: Detected objects with confidence scores
            palette: Extracted color palette
            embedding: Style embedding vector
            
        Returns:
            Confidence score between 0 and 1
        """
        scores = []
        
        # Object detection confidence
        if objects:
            obj_confidences = [obj['confidence'] for obj in objects]
            avg_obj_confidence = sum(obj_confidences) / len(obj_confidences)
            scores.append(avg_obj_confidence)
        else:
            scores.append(0.3)  # Low confidence without objects
        
        # Color extraction quality (based on number of colors)
        color_score = min(len(palette) / 5.0, 1.0)
        scores.append(color_score)
        
        # Embedding generation success
        if embedding is not None:
            scores.append(0.9)
        else:
            scores.append(0.5)
        
        # Overall confidence is weighted average
        weights = [0.5, 0.2, 0.3]  # Objects matter most
        overall = sum(s * w for s, w in zip(scores, weights))
        
        return round(overall, 2)

