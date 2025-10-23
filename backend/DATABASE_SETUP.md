# Database Setup Guide

Complete guide to setting up Supabase PostgreSQL, FAISS vector database, and local file storage for Art.Decor.AI.

---

## 🗄️ Components

1. **Supabase (PostgreSQL)** - Relational data (profiles, artworks, analyses)
2. **FAISS** - Vector similarity search (artwork embeddings)
3. **Local Storage** - Image files (artworks, room photos)

---

## 📋 Prerequisites

- Supabase account (free tier works)
- Python 3.10+ with dependencies installed
- `.env` file configured

---

## 🚀 Quick Setup

### 1. Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Click "Start your project"
3. Create new organization (if needed)
4. Create new project
   - Name: `artdecor-ai`
   - Database Password: (save this!)
   - Region: Choose closest to you
5. Wait for project to initialize (~2 minutes)

### 2. Get Supabase Credentials

Once project is ready:

1. Go to **Settings** → **API**
2. Copy these values to your `.env` file:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-public-key
SUPABASE_SERVICE_KEY=your-service-role-key
```

### 3. Run Database Schema

1. Go to **SQL Editor** in Supabase dashboard
2. Click **New query**
3. Copy entire contents of `db/schema.sql`
4. Paste and click **Run**
5. Verify tables created: Go to **Table Editor**

You should see these tables:
- profiles
- artworks
- room_analyses
- favorites
- stores
- store_inventory
- recommendations_log

### 4. Initialize FAISS Index

```bash
cd backend
python scripts/init_faiss.py
```

Expected output:
```
📊 Initializing FAISS vector database...
Creating new index with test vectors...
✓ Created index with 5 test vectors
```

### 5. Test Database Connections

```bash
python scripts/test_database.py
```

Expected output:
```
✨ All tests passed! Database is ready.
```

### 6. Seed Sample Artwork Data

```bash
python scripts/seed_artworks.py
```

This will:
- Download 10 sample artwork images
- Save to local storage
- Generate embeddings
- Insert into Supabase
- Add to FAISS index

---

## 📊 Database Schema

### Tables

#### **profiles**
```sql
- id (UUID, PK)
- email (TEXT, UNIQUE)
- name (TEXT)
- favorite_styles (TEXT[])
- favorite_artworks (TEXT[])
- budget_range (JSONB)
- location (JSONB)
- created_at, updated_at
```

#### **artworks**
```sql
- id (UUID, PK)
- title (TEXT)
- artist (TEXT)
- description (TEXT)
- price (NUMERIC)
- image_url (TEXT) → Points to local storage
- thumbnail_url (TEXT)
- style (TEXT)
- tags (TEXT[])
- dimensions (TEXT)
- medium (TEXT)
- embedding (JSONB) → 512-dim vector as JSON
- metadata (JSONB)
- is_available (BOOLEAN)
- created_at, updated_at
```

#### **room_analyses**
```sql
- id (UUID, PK)
- user_id (UUID, FK → profiles)
- image_url (TEXT)
- style (TEXT)
- colors (JSONB)
- lighting (JSONB)
- detected_objects (JSONB)
- wall_spaces (JSONB)
- style_embedding (JSONB)
- confidence_score (NUMERIC)
- metadata (JSONB)
- created_at
```

#### **favorites**
```sql
- id (UUID, PK)
- user_id (UUID, FK → profiles)
- artwork_id (UUID, FK → artworks)
- created_at
- UNIQUE(user_id, artwork_id)
```

#### **stores**
```sql
- id (UUID, PK)
- name (TEXT)
- address, city, state, zipcode (TEXT)
- latitude, longitude (NUMERIC)
- phone, website (TEXT)
- rating (NUMERIC)
- opening_hours (JSONB)
- categories (TEXT[])
- created_at, updated_at
```

---

## 💾 Local File Storage

### Directory Structure

```
backend/uploads/
├── artworks/          # Artwork images
│   └── 2025/
│       └── 01/
│           └── artwork-id.jpg
├── rooms/             # User uploaded room photos
│   └── 2025/
│       └── 01/
│           └── room_user-id_uuid.jpg
├── thumbnails/        # Generated thumbnails
│   ├── artworks/
│   └── rooms/
└── temp/              # Temporary files (auto-cleanup)
```

### URLs

Images are served via FastAPI static files:

```
http://localhost:8000/uploads/artworks/2025/01/artwork-id.jpg
http://localhost:8000/uploads/thumbnails/artworks/2025/01/thumb_artwork-id.jpg
```

### Usage

```python
from utils.file_storage import get_file_storage
from PIL import Image

storage = get_file_storage()

# Save artwork
image = Image.open("artwork.jpg")
image_url, thumbnail_url = storage.save_artwork(image, artwork_id="123")

# Save room photo
room_url = storage.save_room_image(image, user_id="user_456")

# Get storage stats
stats = storage.get_storage_stats()
print(f"Total size: {stats['total_size_mb']} MB")
```

---

## 🔍 FAISS Vector Database

### Structure

- **Dimension**: 512 (CLIP embedding size)
- **Index Type**: IndexFlatL2 (exact search)
- **Storage**: `data/artwork_vectors.index`
- **Metadata**: `data/artwork_vectors_metadata.pkl`

### Usage

```python
from db.faiss_client import get_faiss_client
import numpy as np

faiss = get_faiss_client()

# Add vectors
vectors = np.random.randn(10, 512).astype(np.float32)
metadata = [{"id": f"art_{i}", "title": f"Artwork {i}"} for i in range(10)]
faiss.add_vectors(vectors, metadata)
faiss.save_index()

# Search
query_vector = np.random.randn(512).astype(np.float32)
distances, results = faiss.search(query_vector, k=5)

for dist, meta in zip(distances, results):
    print(f"{meta['title']}: {dist}")
```

---

## 🧪 Testing

### Individual Tests

```bash
# Test Supabase only
python -c "from db.supabase_client import get_supabase_client; import asyncio; asyncio.run(get_supabase_client().get_artworks())"

# Test FAISS only
python scripts/init_faiss.py

# Test local storage only
python -c "from utils.file_storage import get_file_storage; print(get_file_storage().get_storage_stats())"
```

### Full Test Suite

```bash
python scripts/test_database.py
```

---

## 🔧 Troubleshooting

### Issue: "Could not connect to Supabase"

**Solution**: Check credentials in `.env`

```bash
# Verify .env has correct values
cat .env | grep SUPABASE

# Test connection
python -c "from supabase import create_client; import os; from dotenv import load_dotenv; load_dotenv(); client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY')); print('Connected!')"
```

### Issue: "FAISS index file not found"

**Solution**: Initialize index

```bash
python scripts/init_faiss.py
```

### Issue: "Permission denied on uploads directory"

**Solution**: Fix permissions

```bash
chmod -R 755 uploads/
```

### Issue: "No artworks in database"

**Solution**: Run seeding script

```bash
python scripts/seed_artworks.py
```

---

## 📊 Verify Setup

Run this to check everything:

```bash
cd backend

# 1. Check directories exist
ls -la uploads/

# 2. Check FAISS index
ls -la data/

# 3. Run tests
python scripts/test_database.py

# 4. Check Supabase (in SQL Editor)
# SELECT COUNT(*) FROM artworks;
```

Expected results:
- ✓ `uploads/` directory with subfolders
- ✓ `data/artwork_vectors.index` file exists
- ✓ All tests pass
- ✓ Artworks count > 0 in Supabase

---

## 🚀 Next Steps

After setup is complete:

1. **Start backend server**:
   ```bash
   uvicorn main:app --reload
   ```

2. **Test API endpoints**:
   ```bash
   curl http://localhost:8000/health
   curl http://localhost:8000/api/recommend -X POST -H "Content-Type: application/json" -d '{"room_style":"Modern","colors":["#ffffff"],"lighting":"Bright","limit":5}'
   ```

3. **View documentation**:
   - Swagger: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

---

## 📈 Production Considerations

For production deployment:

1. **Supabase**:
   - Use service role key for backend operations
   - Enable Row Level Security (RLS)
   - Set up backups

2. **FAISS**:
   - Use IndexIVFFlat for larger datasets (>100k vectors)
   - Consider GPU acceleration
   - Implement index rebuilding schedule

3. **Local Storage**:
   - Set up CDN (Cloudflare, etc.)
   - Implement image optimization pipeline
   - Add automatic cleanup for old files
   - Consider migrating to S3 for scale

---

## 📚 Additional Resources

- [Supabase Documentation](https://supabase.com/docs)
- [FAISS Wiki](https://github.com/facebookresearch/faiss/wiki)
- [FastAPI Static Files](https://fastapi.tiangolo.com/tutorial/static-files/)

---

**Status**: ✅ Database Setup Complete
**Next**: Test API endpoints and integrate with frontend

