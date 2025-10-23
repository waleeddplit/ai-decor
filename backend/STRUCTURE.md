# Backend Structure Overview

## 📁 Directory Layout

```
backend/
│
├── main.py                          # FastAPI application entry point
├── requirements.txt                 # Python dependencies
├── setup.sh                         # Automated setup script
├── .env.example                     # Environment variables template
├── .gitignore                       # Git ignore rules
├── README.md                        # Documentation
│
├── routes/                          # API Endpoints
│   ├── __init__.py
│   ├── room_analysis.py            # POST /api/analyze_room
│   ├── recommendations.py          # POST /api/recommend
│   └── profile.py                  # GET/POST /api/profile
│
├── agents/                          # AI Agent Modules
│   ├── __init__.py
│   ├── vision_match_agent.py       # YOLOv8 + CLIP vision analysis
│   ├── trend_intel_agent.py        # Tavily trend discovery
│   ├── geo_finder_agent.py         # Google Maps store finder
│   └── decision_router.py          # Agent orchestration
│
├── models/                          # Pydantic Schemas
│   ├── __init__.py
│   ├── common.py                   # Shared models (Error, Success)
│   ├── room_analysis.py            # Room analysis request/response
│   ├── recommendation.py           # Recommendation request/response
│   └── profile.py                  # User profile models
│
├── db/                              # Database Clients
│   ├── __init__.py
│   ├── supabase_client.py          # PostgreSQL operations
│   └── faiss_client.py             # Vector similarity search
│
└── utils/                           # Helper Functions
    └── __init__.py
```

## 🔗 Data Flow

```
┌─────────────┐
│   Client    │
│  (Frontend) │
└──────┬──────┘
       │
       │ HTTP Request
       ▼
┌─────────────────────────────────────────┐
│            FastAPI (main.py)            │
│  • CORS middleware                      │
│  • Error handling                       │
│  • Route registration                   │
└──────┬──────────────────────────────────┘
       │
       │ Routes to appropriate endpoint
       ▼
┌──────────────────────────────────────────┐
│         Routes (routes/)                 │
│  • room_analysis.py                      │
│  • recommendations.py                    │
│  • profile.py                            │
└──────┬───────────────────────────────────┘
       │
       │ Calls AI agents or database
       ▼
┌──────────────────────────────────────────┐
│      DecisionRouter (agents/)            │
│  Orchestrates:                           │
│  • VisionMatchAgent (YOLOv8 + CLIP)     │
│  • TrendIntelAgent (Tavily API)         │
│  • GeoFinderAgent (Google Maps)         │
└──────┬───────────────────────────────────┘
       │
       ├──────────────┬──────────────┐
       ▼              ▼              ▼
┌──────────┐  ┌──────────┐  ┌───────────┐
│ Supabase │  │  FAISS   │  │ External  │
│   (DB)   │  │ (Vectors)│  │   APIs    │
└──────────┘  └──────────┘  └───────────┘
       │              │              │
       └──────────────┴──────────────┘
                      │
                      ▼
              ┌───────────────┐
              │   Response    │
              │   (JSON)      │
              └───────────────┘
```

## 📡 API Endpoints

### 1. Room Analysis
```
POST /api/analyze_room
├── Input: Multipart form (image + optional description)
├── Processing:
│   ├── VisionMatchAgent.analyze_room()
│   │   ├── YOLO object detection
│   │   ├── CLIP style embedding
│   │   ├── Color analysis
│   │   └── Lighting detection
│   └── Save to Supabase (if user_id provided)
└── Output: RoomAnalysisResponse
    ├── style
    ├── colors[]
    ├── lighting
    ├── detected_objects[]
    ├── wall_spaces[]
    └── processing_time
```

### 2. Recommendations
```
POST /api/recommend
├── Input: RecommendationRequest
│   ├── room_style
│   ├── colors[]
│   ├── lighting
│   └── preferences (optional)
├── Processing:
│   ├── TrendIntelAgent.get_trending_styles()
│   ├── FAISS vector search
│   ├── Supabase artwork metadata
│   └── DecisionRouter reasoning
└── Output: RecommendationResponse
    ├── recommendations[]
    │   ├── artwork details
    │   ├── match_score
    │   ├── reasoning
    │   └── stores[]
    └── trending_styles[]
```

### 3. User Profile
```
GET /api/profile/{user_id}
├── Processing: Supabase query
└── Output: ProfileResponse

POST /api/profile
├── Input: ProfileRequest
├── Processing: Supabase insert/update
└── Output: ProfileResponse

POST /api/profile/{user_id}/favorites
GET /api/profile/{user_id}/favorites
DELETE /api/profile/{user_id}/favorites/{artwork_id}
```

## 🤖 AI Agents

### VisionMatchAgent
**File**: `agents/vision_match_agent.py`

**Models Used**:
- YOLOv8 (Ultralytics) - Object detection
- CLIP (OpenAI) - Style embeddings

**Methods**:
```python
async analyze_room(image, description) -> Dict
├── _detect_objects()          # YOLO inference
├── _get_style_embedding()     # CLIP embedding
├── _analyze_colors()          # K-means clustering
├── _analyze_lighting()        # Brightness analysis
├── _detect_wall_spaces()      # Segmentation
└── _classify_style()          # Style classification
```

### TrendIntelAgent
**File**: `agents/trend_intel_agent.py`

**External APIs**:
- Tavily API - Real-time trend search

**Methods**:
```python
async get_trending_styles(location) -> List[Dict]
├── _fetch_real_trends()       # Tavily API call
├── _get_mock_trends()         # Fallback
└── _extract_style_name()      # NLP parsing

async get_seasonal_recommendations() -> Dict
async match_trends_to_style(style, colors) -> List[str]
```

### GeoFinderAgent
**File**: `agents/geo_finder_agent.py`

**External APIs**:
- Google Maps Places API

**Methods**:
```python
async find_nearby_stores(lat, lng, radius) -> List[Dict]
├── _search_real_stores()      # Google Maps API
├── _get_mock_stores()         # Fallback
└── _calculate_distance()      # Haversine formula

async get_store_inventory(store_id, artwork_id) -> Dict
async get_directions(origin, destination) -> Dict
```

### DecisionRouter
**File**: `agents/decision_router.py`

**Purpose**: Orchestrates all agents

**Methods**:
```python
async analyze_and_recommend(image, description, location, prefs) -> Dict
├── VisionMatchAgent.analyze_room()
├── TrendIntelAgent.get_trending_styles()
├── GeoFinderAgent.find_nearby_stores()
├── _generate_reasoning()      # NLG
└── _calculate_overall_confidence()

async refine_recommendations(analysis, feedback) -> Dict
```

## 💾 Database Schema

### Supabase Tables

```sql
profiles
├── id (TEXT, PK)
├── email (TEXT)
├── name (TEXT)
├── favorite_styles (TEXT[])
├── favorite_artworks (TEXT[])
├── budget_range (JSONB)
├── location (JSONB)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)

artworks
├── id (TEXT, PK)
├── title (TEXT)
├── artist (TEXT)
├── price (NUMERIC)
├── image_url (TEXT)
├── style (TEXT)
├── tags (TEXT[])
├── embedding (VECTOR(512))
└── created_at (TIMESTAMP)

room_analyses
├── id (SERIAL, PK)
├── user_id (TEXT, FK -> profiles)
├── style (TEXT)
├── colors (JSONB)
├── lighting (TEXT)
├── metadata (JSONB)
└── created_at (TIMESTAMP)

favorites
├── id (SERIAL, PK)
├── user_id (TEXT, FK -> profiles)
├── artwork_id (TEXT, FK -> artworks)
├── created_at (TIMESTAMP)
└── UNIQUE(user_id, artwork_id)
```

### FAISS Index

```python
FAISSClient
├── index: IndexFlatL2(dimension=512)
├── metadata: List[Dict] (parallel array)
├── Methods:
│   ├── add_vectors(vectors, metadata)
│   ├── search(query_vector, k)
│   ├── search_by_style(embedding, filters, k)
│   ├── save_index()
│   └── load_index()
```

## 🔧 Configuration

### Environment Variables

```env
# Server
HOST=0.0.0.0
PORT=8000
FRONTEND_URL=http://localhost:3000

# Database
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJ...

# AI Models
YOLO_MODEL_PATH=./models/yolov8n.pt
CLIP_MODEL_NAME=openai/clip-vit-base-patch32
FAISS_INDEX_PATH=./data/artwork_vectors.index

# External APIs
TAVILY_API_KEY=tvly-...
GOOGLE_MAPS_API_KEY=AIza...
OPENAI_API_KEY=sk-...
GROQ_API_KEY=gsk_...

# Storage
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_S3_BUCKET=artdecor-images
```

## 🚀 Startup Process

1. **Load Environment** (`.env`)
2. **Initialize FastAPI App** (`main.py`)
3. **Add Middleware** (CORS, error handlers)
4. **Lifespan Events**:
   - Connect to Supabase
   - Load FAISS index
   - Initialize AI agents (lazy loading)
5. **Register Routes** (room_analysis, recommendations, profile)
6. **Start Server** (Uvicorn)

## 📊 Request/Response Flow Example

### Analyze Room Flow

```
1. Client uploads image
   ↓
2. FastAPI receives multipart/form-data
   ↓
3. Route: room_analysis.analyze_room()
   ↓
4. Convert to PIL Image
   ↓
5. DecisionRouter.vision_agent.analyze_room()
   ├─→ YOLO detects: sofa, chair, lamp, wall
   ├─→ CLIP generates 512-dim embedding
   ├─→ K-means extracts 4 dominant colors
   └─→ Brightness analysis: "Natural, Bright"
   ↓
6. Classification: "Modern Minimalist"
   ↓
7. Save to Supabase (if user_id)
   ↓
8. Return RoomAnalysisResponse JSON
   ↓
9. Client displays results
```

## 🧪 Testing

```bash
# Test room analysis
curl -X POST http://localhost:8000/api/analyze_room \
  -F "image=@test_room.jpg" \
  -F "description=Modern living room"

# Test recommendations
curl -X POST http://localhost:8000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "room_style": "Modern Minimalist",
    "colors": ["#FFFFFF", "#E5E7EB"],
    "lighting": "Natural, Bright",
    "limit": 5
  }'

# Test health
curl http://localhost:8000/health
```

## 📈 Performance Considerations

- **Lazy Loading**: AI models load on first use
- **Caching**: FAISS index loaded once at startup
- **Async Operations**: All I/O operations are async
- **Connection Pooling**: Supabase client reuses connections
- **Mock Fallbacks**: Graceful degradation if APIs unavailable

## 🔐 Security

- **Input Validation**: Pydantic models validate all inputs
- **File Type Checking**: Only images allowed for upload
- **CORS**: Restricted to frontend URLs
- **Environment Secrets**: API keys in `.env` (not committed)
- **Error Handling**: Generic errors in production

---

**Status**: ✅ Backend Structure Complete
**Next**: Install dependencies and test endpoints

