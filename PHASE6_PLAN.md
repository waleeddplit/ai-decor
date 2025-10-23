# Phase 6: Frontend-Backend Integration

## 🎯 Goal
Connect the beautiful Next.js frontend to the powerful FastAPI backend, replacing all mock data with real AI-powered recommendations.

## ✅ Progress

### Step 1: API Client Setup ✅
- [x] Created `/frontend/src/lib/api.ts` - TypeScript API client
- [x] Created `/frontend/.env.local` - Environment variables
- [x] Defined TypeScript interfaces for all API responses
- [x] Implemented helper functions for backend communication

### Step 2: Upload Page Integration (IN PROGRESS)
- [x] Created updated upload page with real API calls
- [ ] Replace old page with new implementation
- [ ] Test image upload flow
- [ ] Add error recovery and retry logic

### Step 3: Results Page Integration (TODO)
- [ ] Update results page to use real analysis data
- [ ] Display actual color palette from backend
- [ ] Show real artwork recommendations
- [ ] Display nearby stores from Geo API

### Step 4: Loading States & UX (TODO)
- [ ] Add progress indicators for long operations
- [ ] Implement skeleton loaders
- [ ] Add success/error toasts
- [ ] Handle network failures gracefully

### Step 5: Testing (TODO)
- [ ] Test complete flow: upload → analysis → results
- [ ] Test with various image types and sizes
- [ ] Test error scenarios
- [ ] Performance testing

## 🚀 Quick Start

### Terminal 1: Start Backend
```bash
cd backend
source venv/bin/activate
./venv/bin/uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 2: Start Frontend
```bash
cd frontend
npm run dev
```

Visit:
- Frontend: http://localhost:3000
- Backend API Docs: http://localhost:8000/docs

## 📝 Files Created

### New Files
1. **`frontend/src/lib/api.ts`** - API client (174 lines)
   - `analyzeRoom()` - Upload & analyze room images
   - `getRecommendations()` - Get artwork suggestions
   - `getNearbyStores()` - Find local galleries
   - `checkHealth()` - Backend health check

2. **`frontend/.env.local`** - Environment config
   - `NEXT_PUBLIC_API_URL=http://localhost:8000`

3. **`frontend/src/app/upload/page-new.tsx`** - Updated upload page
   - Real API integration
   - Error handling
   - Progress indicators
   - File validation (type, size)

## 🔄 Next Steps

1. **Replace Upload Page**
   ```bash
   cd frontend/src/app/upload
   mv page.tsx page-old.tsx
   mv page-new.tsx page.tsx
   ```

2. **Test the Flow**
   - Upload a room image
   - Check console for API calls
   - Verify data in session storage
   - Check results page

3. **Update Results Page**
   - Read from sessionStorage
   - Display real analysis data
   - Show color palette
   - Display recommendations

## 📊 API Endpoints Used

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Check backend status |
| `/api/analyze_room` | POST | Analyze room image |
| `/api/recommend` | POST | Get recommendations |
| `/api/stores/nearby` | GET | Find local stores |

## 🎨 Data Flow

```
User Upload Image
      ↓
analyzeRoom(image, description)
      ↓
Backend: VisionMatchAgent
      ↓
RoomAnalysisResponse
      ↓
sessionStorage.setItem("roomAnalysis", ...)
      ↓
Navigate to /results
      ↓
Results Page reads sessionStorage
      ↓
Display AI Recommendations
```

## ⚠️ Requirements

- Backend server running on port 8000
- Frontend dev server on port 3000
- AI models downloaded (run `scripts/download_models.py`)
- Valid image files (JPG, PNG, WEBP < 10MB)

## 💡 Testing Tips

1. **Backend Health Check**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Test Image Upload**
   - Use well-lit room photos
   - Show furniture and wall space
   - Avoid very dark or blurry images

3. **Check Console**
   - Open browser DevTools
   - Watch Network tab for API calls
   - Check Console for errors

## 🐛 Common Issues

1. **"Backend not available"**
   - Check backend is running
   - Verify port 8000 is correct
   - Check CORS settings

2. **"Failed to analyze"**
   - Check AI models are downloaded
   - Verify image size < 10MB
   - Check backend logs

3. **"No recommendations"**
   - Ensure FAISS index has data
   - Run seed_artworks.py script
   - Check backend logs

---

**Status**: Step 1 Complete | Step 2 In Progress
**Next**: Replace upload page and test integration

