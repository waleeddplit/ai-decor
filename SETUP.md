# 🛠️ Complete Setup Guide - Art.Decor.AI

**Get the full AI-powered décor platform running in 15 minutes!**

---

## 📋 Prerequisites

### Required Software
- **Node.js** 18+ → [Download](https://nodejs.org/)
- **Python** 3.10+ → [Download](https://www.python.org/)
- **Git** → [Download](https://git-scm.com/)

### System Requirements
- **Disk Space:** 2GB (for AI models)
- **RAM:** 4GB minimum, 8GB recommended
- **OS:** macOS, Linux, or Windows

---

## 🚀 Quick Start (3 Steps)

### Step 1: Clone Repository

```bash
git clone <your-repo-url>
cd ai-decorator
```

### Step 2: Start Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

**Backend running at:** http://localhost:8000

### Step 3: Start Frontend

```bash
# In a new terminal
cd frontend
npm install
npm run dev
```

**Frontend running at:** http://localhost:3000

---

## 🎯 Environment Setup (Detailed)

### 📦 Frontend Environment

Create `/frontend/.env.local`:

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

That's it! The frontend needs only one variable.

---

### 🐍 Backend Environment

Create `/backend/.env` with the following:

#### 🔰 **Minimum Configuration (No API Keys Needed!)**

```env
# Server
FRONTEND_URL=http://localhost:3000
DEBUG=True

# Models auto-download on first run
CLIP_MODEL_NAME=openai/clip-vit-base-patch32
```

**This works!** The system uses local models only (YOLOv8 + CLIP).

---

#### ⭐ **Recommended Configuration (Free APIs)**

Add these for full features:

```env
# GROQ API (FREE, Fast inference)
# Get from: https://console.groq.com/keys
GROQ_API_KEY=gsk_your_api_key_here
CHAT_MODEL=llama-3.2-90b-vision-preview

# Tavily API (FREE tier: 1000 requests/month)
# Get from: https://tavily.com
TAVILY_API_KEY=tvly_your_api_key_here

# Google Maps API (FREE tier: $200 credit/month)
# Get from: https://console.cloud.google.com/google/maps-apis
GOOGLE_MAPS_API_KEY=AIza_your_api_key_here
```

---

#### 🚀 **Full Configuration (All Features)**

```env
# ============================================
# SERVER
# ============================================
FRONTEND_URL=http://localhost:3000
DEBUG=True
PORT=8000

# ============================================
# AI MODELS
# ============================================
# Option 1: Ollama (Local, FREE)
USE_OLLAMA=false
OLLAMA_BASE_URL=http://localhost:11434
CHAT_MODEL=llava

# Option 2: Groq (Cloud, FREE tier)
GROQ_API_KEY=gsk_your_key_here

# Option 3: Gemini (FREE tier)
GEMINI_API_KEY=your_key_here

# Option 4: OpenAI (Paid)
OPENAI_API_KEY=sk_your_key_here

# Vision Models (auto-download)
CLIP_MODEL_NAME=openai/clip-vit-base-patch32

# ============================================
# EXTERNAL APIs
# ============================================
# Tavily - Trend Intelligence
TAVILY_API_KEY=tvly_your_key_here

# Google Maps - Store Finder
GOOGLE_MAPS_API_KEY=AIza_your_key_here

# Unsplash - Artwork Images (Optional)
UNSPLASH_ACCESS_KEY=your_key_here

# ============================================
# DATABASE (Optional)
# ============================================
# Supabase - User Profiles
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_anon_key_here

# ============================================
# STORAGE (Optional)
# ============================================
# AWS S3 - Cloud Storage
# AWS_ACCESS_KEY_ID=AKIA_your_key_here
# AWS_SECRET_ACCESS_KEY=your_secret_here
# AWS_S3_BUCKET=artdecor-images
```

---

## 🔑 Getting API Keys (Step-by-Step)

### 1. Groq API Key (Recommended - FREE & Fast)

1. Visit: https://console.groq.com
2. Sign up with Google/GitHub
3. Go to **API Keys** → **Create API Key**
4. Copy key: `gsk_...`
5. Add to `.env`: `GROQ_API_KEY=gsk_...`

**Why Groq?** 10-20x faster than OpenAI, free tier available.

---

### 2. Tavily API Key (Trend Intelligence)

1. Visit: https://tavily.com
2. Sign up for free account
3. Go to **Dashboard** → **API Keys**
4. Copy key: `tvly-...`
5. Add to `.env`: `TAVILY_API_KEY=tvly-...`

**Free Tier:** 1000 requests/month

---

### 3. Google Maps API Key (Store Finder)

1. Visit: https://console.cloud.google.com
2. Create new project: "Art.Decor.AI"
3. Enable APIs:
   - **Places API**
   - **Geocoding API**
   - **Directions API**
4. Go to **Credentials** → **Create API Key**
5. Copy key: `AIza...`
6. Add to `.env`: `GOOGLE_MAPS_API_KEY=AIza...`

**Free Tier:** $200 credit/month (~28,000 requests)

**Detailed Guide:** See `/GOOGLE_MAPS_API_SETUP.md`

---

### 4. Gemini API Key (Alternative to Groq)

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google
3. Click **Create API Key**
4. Copy key
5. Add to `.env`: `GEMINI_API_KEY=your_key_here`

---

### 5. Unsplash API Key (Optional - More Artworks)

1. Visit: https://unsplash.com/oauth/applications
2. Create new application
3. Accept terms
4. Copy **Access Key**
5. Add to `.env`: `UNSPLASH_ACCESS_KEY=your_key_here`

**Free Tier:** 50 requests/hour

**Detailed Guide:** See `/GET_UNSPLASH_API_KEY.md`

---

## 🎨 First Run - What Happens?

### Backend First Start:

```bash
cd backend
source venv/bin/activate
python main.py
```

**You'll see:**

```
📦 Downloading YOLOv8 model (6.2MB)... ✓
📦 Downloading CLIP model (~200MB)... ✓
🚀 Backend started on http://localhost:8000
📖 API docs: http://localhost:8000/docs
✅ All systems ready!
```

**First run takes 2-3 minutes to download models.**  
**Subsequent runs start in 5 seconds.**

---

### Frontend First Start:

```bash
cd frontend
npm install
npm run dev
```

**You'll see:**

```
npm install (takes ~30 seconds)
✓ Ready in 3.2s
○ Local: http://localhost:3000
```

---

## 🧪 Testing Your Setup

### 1. Test Backend API

```bash
curl http://localhost:8000/health
```

**Expected Response:**

```json
{
  "status": "healthy",
  "timestamp": "2024-10-24T12:34:56Z",
  "models": {
    "yolov8": "loaded",
    "clip": "loaded"
  }
}
```

---

### 2. Test Frontend

1. Open: http://localhost:3000
2. Click **"Upload Room Photo"**
3. Upload any room image
4. Click **"Analyze & Get Recommendations"**
5. Wait ~3 seconds
6. See AI-generated recommendations!

---

### 3. Test Chat Interface

1. Go to: http://localhost:3000/chat
2. Type: "I want modern art for my living room"
3. Get AI response (if LLM configured)

---

### 4. Run Backend Tests

```bash
cd backend
source venv/bin/activate

# Test vision analysis
python scripts/test_vision_agent.py

# Test FAISS search
python scripts/test_faiss_search.py

# Test end-to-end
python scripts/test_end_to_end.py
```

---

## 🐛 Troubleshooting

### ❌ "Port 8000 already in use"

```bash
# Find and kill process
lsof -ti:8000 | xargs kill -9

# Or use different port
PORT=8001 python main.py
```

---

### ❌ "ModuleNotFoundError"

```bash
# Ensure venv is activated
source venv/bin/activate  # You should see (venv) in prompt

# Reinstall dependencies
pip install -r requirements.txt
```

---

### ❌ "CUDA not available" or "torch.cuda"

**This is normal!** The system works on CPU.

If you want GPU acceleration:
```bash
# For NVIDIA GPUs
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

---

### ❌ "Failed to download models"

```bash
# Manual download
cd backend
python scripts/download_models.py
```

---

### ❌ Frontend "Failed to analyze room"

1. Check backend is running: http://localhost:8000/health
2. Check CORS: Ensure `FRONTEND_URL=http://localhost:3000` in `.env`
3. Check console for errors: Open DevTools → Console

---

### ❌ "No recommendations found"

1. Ensure FAISS index has data:
   ```bash
   cd backend
   python scripts/init_faiss.py
   python scripts/seed_artworks.py
   ```

2. Check index exists:
   ```bash
   ls -lh data/artwork_vectors.index
   ```

---

## 📊 System Architecture

```
┌─────────────────────────────────────────┐
│  Frontend (Next.js)                      │
│  http://localhost:3000                   │
└─────────────────┬───────────────────────┘
                  │
                  │ HTTP Requests
                  ▼
┌─────────────────────────────────────────┐
│  Backend (FastAPI)                       │
│  http://localhost:8000                   │
│                                          │
│  ┌─────────────────────────────────┐   │
│  │  AI Agents                       │   │
│  │  • VisionMatchAgent (YOLOv8+CLIP)│   │
│  │  • ChatAgent (LLM)               │   │
│  │  • TrendIntelAgent (Tavily)      │   │
│  │  • GeoFinderAgent (Maps)         │   │
│  │  • DecisionRouter                │   │
│  └─────────────────────────────────┘   │
│                                          │
│  ┌─────────────────────────────────┐   │
│  │  Data Layer                      │   │
│  │  • FAISS (vector search)         │   │
│  │  • Local storage (images)        │   │
│  │  • Supabase (optional)           │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

---

## 🎯 Feature Checklist

After setup, you should have:

- ✅ **Image Upload** - Drag-drop room photos
- ✅ **AI Analysis** - YOLOv8 object detection + CLIP embeddings
- ✅ **Recommendations** - FAISS similarity search
- ✅ **AI Reasoning** - "Why This Works" explanations (if LLM configured)
- ✅ **Chat Interface** - Conversational AI (if LLM configured)
- ✅ **Trend Intelligence** - Current décor trends (if Tavily configured)
- ✅ **Store Finder** - Nearby galleries (if Google Maps configured)
- ✅ **Voice Input** - Speech recognition
- ✅ **Dark Mode** - Theme toggle

---

## 📚 Next Steps

### For Development:
1. ✅ Follow this setup guide
2. 📖 Read `/README.md` for architecture overview
3. 🧪 Run tests in `/backend/scripts/`
4. 🎨 Explore frontend pages
5. 📡 Check API docs: http://localhost:8000/docs

### For Production:
1. 🔐 Set up proper environment variables
2. 🗄️ Configure Supabase database
3. ☁️ Deploy frontend to Vercel
4. 🚀 Deploy backend to Render/Railway
5. 📊 Set up monitoring (Sentry, DataDog)

---

## 🆘 Getting Help

### Documentation
- **Main README:** `/README.md`
- **Backend README:** `/backend/README.md`
- **Frontend README:** `/frontend/README.md`
- **API Docs:** http://localhost:8000/docs

### Specific Guides
- **Google Maps Setup:** `/GOOGLE_MAPS_API_SETUP.md`
- **Unsplash Setup:** `/GET_UNSPLASH_API_KEY.md`
- **Ollama Setup:** `/OLLAMA_LLAVA_SETUP.md`
- **Database Setup:** `/backend/DATABASE_SETUP.md`

### Common Issues
- **Troubleshooting:** See `/TROUBLESHOOTING_PURCHASE_BUTTONS.md`
- **Integration:** See `/FRONTEND_INTEGRATION_COMPLETE.md`

---

## ✅ Setup Complete Checklist

Before you start developing, verify:

- [ ] Backend starts without errors
- [ ] Frontend starts on port 3000
- [ ] Can access http://localhost:8000/health
- [ ] Can access http://localhost:8000/docs
- [ ] Can upload image and get analysis
- [ ] FAISS index has data (check `data/artwork_vectors.index`)
- [ ] At least one LLM API key configured (Groq/Gemini/OpenAI/Ollama)

---

## 🎉 You're Ready!

Your Art.Decor.AI platform is now fully set up and ready for development!

**Test the full flow:**
1. Go to http://localhost:3000
2. Upload a room photo
3. Get AI analysis in ~0.5 seconds
4. See personalized recommendations
5. Chat with AI about your preferences

**Happy coding!** 🚀

---

**Need help?** Check `/README.md` for detailed architecture or `/backend/README.md` for API documentation.

