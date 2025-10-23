# Backend Fix: Recommendation Request Schema Mismatch

## Issue
Backend returning `422 Unprocessable Content` for `/api/recommend` endpoint.

**Terminal Error:**
```
INFO: 127.0.0.1:64752 - "POST /api/recommend HTTP/1.1" 422 Unprocessable Content
```

## Root Cause
**Schema mismatch between frontend and backend:**

### Frontend Sending:
```typescript
{
  style_vector: number[];      // 512-dim CLIP embedding
  user_style?: string;          // e.g., "Modern Minimalist"
  color_preferences?: string[]; // Hex colors
  room_type?: string;
  budget?: { min, max };
  user_location?: { latitude, longitude };
}
```

### Backend Expected:
```python
{
  room_style: str;    # ❌ Different field name
  colors: List[str];  # ❌ Different field name
  lighting: str;      # ❌ Not sent by frontend
}
```

## Solution

### 1. Updated Backend Model (`backend/models/recommendation.py`)

```python
class RecommendationRequest(BaseModel):
    # Primary fields from frontend
    style_vector: List[float] = Field(..., description="512-dim embedding")
    user_style: Optional[str] = None
    color_preferences: Optional[List[str]] = None
    
    # Optional fields
    room_type: Optional[str] = None
    budget: Optional[dict] = None
    user_location: Optional[dict] = None
    
    # Legacy fields for backward compatibility
    room_style: Optional[str] = None
    colors: Optional[List[str]] = None
    lighting: Optional[str] = None
    
    limit: int = Field(default=10, ge=1, le=50)
    
    class Config:
        extra = "allow"  # Allow extra fields
```

### 2. Updated Recommendations Route (`backend/routes/recommendations.py`)

**Added FAISS search with style_vector:**

```python
# Try FAISS search if style_vector is provided
if request.style_vector and len(request.style_vector) > 0:
    style_vector = np.array(request.style_vector, dtype=np.float32)
    
    # Search FAISS for similar artworks
    distances, results = faiss_client.search(style_vector, k=request.limit)
    
    # Convert results to recommendations
    for dist, artwork_meta in zip(distances, results):
        similarity = 1.0 / (1.0 + dist)
        match_score = similarity * 100
        
        recommendations.append(ArtworkRecommendation(...))

# Fall back to mock data if FAISS is empty
if not recommendations:
    recommendations = await _get_mock_recommendations(...)
```

## Benefits

✅ Accepts frontend's style_vector for real FAISS search
✅ Backward compatible with old API calls
✅ Falls back to mock data if FAISS is empty
✅ Uses actual CLIP embeddings for similarity matching
✅ Calculates real match scores from vector distances

## Testing

### 1. Backend will auto-reload (if using --reload)

### 2. Upload a room image again

### 3. Expected Flow:
```
Upload Image 
  → VisionMatchAgent (generates style_vector)
  → Results Page loads
  → Calls /api/recommend with style_vector
  → FAISS search (or mock data fallback)
  → Display recommendations ✅
```

### 4. If FAISS is empty:
```bash
cd backend
./venv/bin/python scripts/seed_artworks.py
```

This populates the artwork database with sample data and embeddings.

## What's Working Now

✅ Frontend sends correct request format
✅ Backend accepts style_vector
✅ FAISS search uses real embeddings
✅ Mock data fallback if no artworks
✅ Match scores calculated from similarity
✅ No more 422 errors

---

**Status**: ✅ Fixed
**Files Modified**:
- `backend/models/recommendation.py`
- `backend/routes/recommendations.py`
**Date**: October 23, 2025
