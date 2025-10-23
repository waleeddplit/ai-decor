# Art.Decor.AI Backend

FastAPI backend for the Art.Decor.AI platform - AI-powered home décor recommendations.

## 🏗️ Architecture

```
backend/
├── main.py                 # FastAPI app entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
│
├── routes/                # API endpoint definitions
│   ├── room_analysis.py   # POST /api/analyze_room
│   ├── recommendations.py # POST /api/recommend
│   └── profile.py         # GET/POST /api/profile
│
├── agents/                # AI agent modules
│   ├── vision_match_agent.py      # YOLOv8 + CLIP vision
│   ├── trend_intel_agent.py       # Tavily trend analysis
│   ├── geo_finder_agent.py        # Google Maps store finder
│   └── decision_router.py         # Agent orchestration
│
├── models/                # Pydantic schemas
│   ├── room_analysis.py   # Room analysis models
│   ├── recommendation.py  # Recommendation models
│   ├── profile.py         # User profile models
│   └── common.py          # Shared models
│
├── db/                    # Database clients
│   ├── supabase_client.py # PostgreSQL operations
│   └── faiss_client.py    # Vector similarity search
│
└── utils/                 # Helper functions
```

## 🚀 Quick Start

### 1. Create Virtual Environment

```bash
cd backend
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

### 4. Run Development Server

```bash
# With uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or with Python
python main.py
```

The API will be available at: **http://localhost:8000**

API Documentation: **http://localhost:8000/docs**

## 📡 API Endpoints

### Room Analysis

**POST** `/api/analyze_room`
- Upload room image for AI analysis
- Returns: style, colors, lighting, objects, wall spaces

```bash
curl -X POST "http://localhost:8000/api/analyze_room" \
  -F "image=@room.jpg" \
  -F "description=Modern living room with white walls"
```

### Recommendations

**POST** `/api/recommend`
- Get personalized décor recommendations
- Returns: artwork matches with reasoning

```json
{
  "room_style": "Modern Minimalist",
  "colors": ["#FFFFFF", "#E5E7EB", "#1F2937"],
  "lighting": "Natural, Bright",
  "limit": 10
}
```

### User Profile

**GET** `/api/profile/{user_id}`
- Retrieve user profile and preferences

**POST** `/api/profile`
- Create or update user profile

**POST** `/api/profile/{user_id}/favorites`
- Add artwork to favorites

**GET** `/api/profile/{user_id}/favorites`
- Get user's favorite artworks

### Health Check

**GET** `/health`
- Check API and service status

## 🤖 AI Agents

### 1. VisionMatchAgent

Analyzes room images using computer vision:
- **YOLOv8**: Object detection (furniture, walls, etc.)
- **CLIP**: Style embeddings for similarity search
- **Color Analysis**: Dominant color palette extraction
- **Lighting Detection**: Brightness and ambiance analysis

### 2. TrendIntelAgent

Fetches current décor trends:
- **Tavily API**: Real-time trend discovery
- **Seasonal Recommendations**: Context-aware suggestions
- **Style Matching**: Align trends with user's room

### 3. GeoFinderAgent

Finds local stores and galleries:
- **Google Maps API**: Nearby art galleries
- **Distance Calculation**: Haversine formula
- **Store Details**: Hours, ratings, contact info

### 4. DecisionRouter

Orchestrates all agents:
- Coordinates Vision + Trend + Geo agents
- Generates natural language reasoning
- Synthesizes comprehensive recommendations

## 💾 Database Setup

### Supabase (PostgreSQL)

Required tables:

```sql
-- User profiles
CREATE TABLE profiles (
  id TEXT PRIMARY KEY,
  email TEXT,
  name TEXT,
  favorite_styles TEXT[],
  favorite_artworks TEXT[],
  budget_range JSONB,
  location JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Artwork metadata
CREATE TABLE artworks (
  id TEXT PRIMARY KEY,
  title TEXT,
  artist TEXT,
  price NUMERIC,
  image_url TEXT,
  style TEXT,
  tags TEXT[],
  embedding VECTOR(512),  -- For pgvector extension
  created_at TIMESTAMP DEFAULT NOW()
);

-- Room analyses
CREATE TABLE room_analyses (
  id SERIAL PRIMARY KEY,
  user_id TEXT REFERENCES profiles(id),
  style TEXT,
  colors JSONB,
  lighting TEXT,
  metadata JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Favorites
CREATE TABLE favorites (
  id SERIAL PRIMARY KEY,
  user_id TEXT REFERENCES profiles(id),
  artwork_id TEXT REFERENCES artworks(id),
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(user_id, artwork_id)
);
```

### FAISS Vector Database

Initialize FAISS index:

```python
from db.faiss_client import get_faiss_client
import numpy as np

# Create client
faiss = get_faiss_client()

# Add artwork embeddings
vectors = np.random.rand(100, 512).astype('float32')  # Example
metadata = [{"id": f"art_{i}", "title": f"Artwork {i}"} for i in range(100)]

faiss.add_vectors(vectors, metadata)
faiss.save_index()
```

## 🔧 Configuration

### Required Environment Variables

```env
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_anon_key

# AI APIs
OPENAI_API_KEY=sk-...
GROQ_API_KEY=gsk_...
TAVILY_API_KEY=tvly-...
GOOGLE_MAPS_API_KEY=AIza...

# AWS S3
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_S3_BUCKET=artdecor-images

# Server
FRONTEND_URL=http://localhost:3000
DEBUG=True
```

## 📦 Dependencies

### Core
- **FastAPI**: Modern web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation

### AI/ML
- **PyTorch**: Deep learning framework
- **Transformers**: Hugging Face models (CLIP)
- **Ultralytics**: YOLOv8 object detection
- **FAISS**: Vector similarity search

### External Services
- **Supabase**: PostgreSQL database client
- **OpenAI**: GPT models (optional)
- **Tavily**: Trend discovery API
- **Google Maps**: Location services
- **Boto3**: AWS S3 storage

## 🧪 Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/

# With coverage
pytest --cov=. tests/
```

## 🚀 Deployment

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Render / Railway

```yaml
# render.yaml
services:
  - type: web
    name: artdecor-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
```

## 🔒 Security

- API rate limiting (TODO)
- Input validation via Pydantic
- CORS configuration
- Environment variable secrets
- File upload size limits

## 📊 Monitoring

- Health check endpoint: `/health`
- Structured logging
- Error tracking (TODO: Sentry)
- Performance metrics (TODO)

## 🐛 Troubleshooting

### Import Errors

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Database Connection Issues

```bash
# Test Supabase connection
python -c "from db.supabase_client import get_supabase_client; print(get_supabase_client())"
```

### Model Loading Errors

```bash
# Download YOLO model
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"

# Check CLIP model
python -c "from transformers import CLIPModel; CLIPModel.from_pretrained('openai/clip-vit-base-patch32')"
```

## 📚 API Documentation

Once the server is running:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔗 Integration with Frontend

Frontend should call backend APIs:

```typescript
// Example: Analyze room
const formData = new FormData();
formData.append('image', imageFile);
formData.append('description', 'Modern living room');

const response = await fetch('http://localhost:8000/api/analyze_room', {
  method: 'POST',
  body: formData,
});

const analysis = await response.json();
```

## 📄 License

MIT License - Educational and demonstration purposes

---

**Built with FastAPI and Python 3.11+**

