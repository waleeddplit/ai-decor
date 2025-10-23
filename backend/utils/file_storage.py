"""
Local file storage utility for images
Alternative to AWS S3 - stores files locally and serves via FastAPI
"""

import os
import uuid
import shutil
from typing import Optional, Tuple
from pathlib import Path
from PIL import Image
import hashlib
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()


class LocalFileStorage:
    """
    Local file storage manager for artwork and room images
    
    Features:
    - Store images in organized directory structure
    - Generate unique filenames
    - Create thumbnails
    - Serve URLs for stored images
    - Clean up old files
    """

    def __init__(self, base_path: Optional[str] = None):
        """
        Initialize local file storage
        
        Args:
            base_path: Base directory for storing files (default: ./uploads)
        """
        self.base_path = Path(base_path or os.getenv("LOCAL_STORAGE_PATH", "./uploads"))
        self.base_url = os.getenv("BASE_URL", "http://localhost:8000")
        
        # Create directory structure
        self.artworks_path = self.base_path / "artworks"
        self.rooms_path = self.base_path / "rooms"
        self.thumbnails_path = self.base_path / "thumbnails"
        self.temp_path = self.base_path / "temp"
        
        self._create_directories()
        
        print(f"✓ LocalFileStorage initialized at {self.base_path}")

    def _create_directories(self):
        """Create necessary directory structure"""
        for path in [self.artworks_path, self.rooms_path, self.thumbnails_path, self.temp_path]:
            path.mkdir(parents=True, exist_ok=True)

    def save_image(
        self, 
        image: Image.Image, 
        category: str = "artworks",
        filename: Optional[str] = None,
        create_thumbnail: bool = True
    ) -> Tuple[str, Optional[str]]:
        """
        Save image to local storage
        
        Args:
            image: PIL Image object
            category: Category folder (artworks, rooms, etc.)
            filename: Optional custom filename
            create_thumbnail: Whether to create thumbnail
            
        Returns:
            Tuple of (image_url, thumbnail_url)
        """
        # Generate unique filename if not provided
        if filename is None:
            filename = f"{uuid.uuid4()}.jpg"
        elif not filename.endswith(('.jpg', '.jpeg', '.png', '.webp')):
            filename = f"{filename}.jpg"
        
        # Determine save path
        if category == "artworks":
            save_dir = self.artworks_path
        elif category == "rooms":
            save_dir = self.rooms_path
        else:
            save_dir = self.base_path / category
            save_dir.mkdir(exist_ok=True)
        
        # Organize by date
        date_dir = save_dir / datetime.now().strftime("%Y/%m")
        date_dir.mkdir(parents=True, exist_ok=True)
        
        # Save original image
        image_path = date_dir / filename
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Optimize and save
        image.save(image_path, 'JPEG', quality=90, optimize=True)
        
        # Generate URL
        relative_path = image_path.relative_to(self.base_path)
        image_url = f"{self.base_url}/uploads/{relative_path.as_posix()}"
        
        # Create thumbnail if requested
        thumbnail_url = None
        if create_thumbnail:
            thumbnail_url = self._create_thumbnail(image, filename, category)
        
        return image_url, thumbnail_url

    def _create_thumbnail(
        self, 
        image: Image.Image, 
        filename: str,
        category: str,
        size: Tuple[int, int] = (400, 400)
    ) -> str:
        """
        Create thumbnail for image
        
        Args:
            image: PIL Image object
            filename: Original filename
            category: Category folder
            size: Thumbnail size (default: 400x400)
            
        Returns:
            Thumbnail URL
        """
        # Create thumbnail
        thumb = image.copy()
        thumb.thumbnail(size, Image.Resampling.LANCZOS)
        
        # Save thumbnail
        thumb_dir = self.thumbnails_path / category / datetime.now().strftime("%Y/%m")
        thumb_dir.mkdir(parents=True, exist_ok=True)
        
        thumb_filename = f"thumb_{filename}"
        thumb_path = thumb_dir / thumb_filename
        
        thumb.save(thumb_path, 'JPEG', quality=85, optimize=True)
        
        # Generate URL
        relative_path = thumb_path.relative_to(self.base_path)
        thumbnail_url = f"{self.base_url}/uploads/{relative_path.as_posix()}"
        
        return thumbnail_url

    def save_artwork(
        self, 
        image: Image.Image, 
        artwork_id: Optional[str] = None
    ) -> Tuple[str, str]:
        """
        Save artwork image with thumbnail
        
        Args:
            image: PIL Image object
            artwork_id: Optional artwork ID for filename
            
        Returns:
            Tuple of (image_url, thumbnail_url)
        """
        filename = f"{artwork_id}.jpg" if artwork_id else None
        return self.save_image(image, category="artworks", filename=filename, create_thumbnail=True)

    def save_room_image(
        self, 
        image: Image.Image, 
        user_id: Optional[str] = None
    ) -> str:
        """
        Save room analysis image
        
        Args:
            image: PIL Image object
            user_id: Optional user ID for organization
            
        Returns:
            Image URL
        """
        filename = f"room_{user_id}_{uuid.uuid4()}.jpg" if user_id else None
        image_url, _ = self.save_image(image, category="rooms", filename=filename, create_thumbnail=False)
        return image_url

    def delete_image(self, url: str) -> bool:
        """
        Delete image from storage
        
        Args:
            url: Image URL
            
        Returns:
            True if deleted successfully
        """
        try:
            # Extract relative path from URL
            relative_path = url.replace(f"{self.base_url}/uploads/", "")
            file_path = self.base_path / relative_path
            
            if file_path.exists():
                file_path.unlink()
                
                # Try to delete thumbnail
                thumb_path = self.thumbnails_path / relative_path.replace("artworks/", "").replace("rooms/", "")
                thumb_filename = f"thumb_{thumb_path.name}"
                thumb_full_path = thumb_path.parent / thumb_filename
                
                if thumb_full_path.exists():
                    thumb_full_path.unlink()
                
                return True
            
            return False
        
        except Exception as e:
            print(f"Error deleting image: {e}")
            return False

    def get_image_path(self, url: str) -> Optional[Path]:
        """
        Get local file path from URL
        
        Args:
            url: Image URL
            
        Returns:
            Path object or None if not found
        """
        try:
            relative_path = url.replace(f"{self.base_url}/uploads/", "")
            file_path = self.base_path / relative_path
            
            if file_path.exists():
                return file_path
            
            return None
        
        except Exception as e:
            print(f"Error getting image path: {e}")
            return None

    def get_file_hash(self, file_path: Path) -> str:
        """
        Calculate MD5 hash of file for deduplication
        
        Args:
            file_path: Path to file
            
        Returns:
            MD5 hash string
        """
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def cleanup_temp_files(self, max_age_hours: int = 24):
        """
        Clean up temporary files older than specified age
        
        Args:
            max_age_hours: Maximum age in hours (default: 24)
        """
        import time
        
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        deleted_count = 0
        
        for file_path in self.temp_path.iterdir():
            if file_path.is_file():
                file_age = current_time - file_path.stat().st_mtime
                if file_age > max_age_seconds:
                    file_path.unlink()
                    deleted_count += 1
        
        if deleted_count > 0:
            print(f"✓ Cleaned up {deleted_count} temporary files")

    def get_storage_stats(self) -> dict:
        """
        Get storage statistics
        
        Returns:
            Dict with storage stats
        """
        def get_dir_size(path: Path) -> int:
            """Calculate total size of directory"""
            total = 0
            for file_path in path.rglob('*'):
                if file_path.is_file():
                    total += file_path.stat().st_size
            return total
        
        def count_files(path: Path) -> int:
            """Count files in directory"""
            return sum(1 for _ in path.rglob('*') if _.is_file())
        
        return {
            "total_size_mb": round(get_dir_size(self.base_path) / (1024 * 1024), 2),
            "artworks": {
                "count": count_files(self.artworks_path),
                "size_mb": round(get_dir_size(self.artworks_path) / (1024 * 1024), 2)
            },
            "rooms": {
                "count": count_files(self.rooms_path),
                "size_mb": round(get_dir_size(self.rooms_path) / (1024 * 1024), 2)
            },
            "thumbnails": {
                "count": count_files(self.thumbnails_path),
                "size_mb": round(get_dir_size(self.thumbnails_path) / (1024 * 1024), 2)
            },
            "temp": {
                "count": count_files(self.temp_path),
                "size_mb": round(get_dir_size(self.temp_path) / (1024 * 1024), 2)
            }
        }


# Singleton instance
_storage: Optional[LocalFileStorage] = None


def get_file_storage() -> LocalFileStorage:
    """Get or create LocalFileStorage singleton"""
    global _storage
    if _storage is None:
        _storage = LocalFileStorage()
    return _storage

