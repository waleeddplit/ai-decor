"""
Art.Decor.AI - FastAPI Backend
Main application entry point
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
# Load environment variables FIRST (before importing routes)
from dotenv import load_dotenv
load_dotenv()

# Now import routes (they will see the environment variables)
from routes import room_analysis_router, recommendations_router, profile_router, chat_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup/shutdown events
    """
    # Startup
    print("🚀 Starting Art.Decor.AI Backend...")
    print(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")

    # Initialize database connections
    try:
        from db.supabase_client import get_supabase_client
        from db.faiss_client import get_faiss_client

        # Test connections
        supabase = get_supabase_client()
        print("✅ Supabase client initialized")

        faiss = get_faiss_client()
        print(f"✅ FAISS client initialized ({faiss.get_total_vectors()} vectors)")

    except Exception as e:
        print(f"⚠️  Warning: Database initialization error: {e}")

    # Initialize AI agents
    try:
        from agents import VisionMatchAgent, TrendIntelAgent, GeoFinderAgent

        print("🤖 Initializing AI agents...")
        # Agents will be initialized lazily when first used
        print("✅ AI agents ready")

    except Exception as e:
        print(f"⚠️  Warning: Agent initialization error: {e}")

    print("✨ Backend ready!")

    yield  # Application runs

    # Shutdown
    print("👋 Shutting down Art.Decor.AI Backend...")


# Create FastAPI app
app = FastAPI(
    title="Art.Decor.AI API",
    description="AI-powered home décor recommendation platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS Configuration
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
origins = [
    frontend_url,
    "http://localhost:3000",
    "http://localhost:3001",
    "https://artdecor-ai.vercel.app",  # Add your production frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    print(f"❌ Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if os.getenv("DEBUG") else "An unexpected error occurred",
        },
    )


# Root endpoint
@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "Art.Decor.AI API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "endpoints": {
            "room_analysis": "/api/analyze_room",
            "recommendations": "/api/recommend",
            "profile": "/api/profile",
            "chat": "/api/chat",
            "health": "/health",
        },
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    try:
        from db.supabase_client import get_supabase_client
        from db.faiss_client import get_faiss_client

        supabase_status = "healthy"
        faiss_status = "healthy"
        faiss_vectors = 0

        try:
            supabase = get_supabase_client()
        except Exception as e:
            supabase_status = f"unhealthy: {str(e)}"

        try:
            faiss = get_faiss_client()
            faiss_vectors = faiss.get_total_vectors()
        except Exception as e:
            faiss_status = f"unhealthy: {str(e)}"

        return {
            "status": "healthy",
            "services": {
                "api": "healthy",
                "supabase": supabase_status,
                "faiss": faiss_status,
            },
            "faiss_vectors": faiss_vectors,
            "environment": os.getenv("ENVIRONMENT", "development"),
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "error": str(e)},
        )


# Include routers
app.include_router(room_analysis_router)
app.include_router(recommendations_router)
app.include_router(profile_router)
app.include_router(chat_router)

# Mount static files for local image storage
uploads_path = os.path.join(os.path.dirname(__file__), "uploads")
if os.path.exists(uploads_path):
    app.mount("/uploads", StaticFiles(directory=uploads_path), name="uploads")
    print(f"✓ Serving static files from {uploads_path}")


# Run with: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=os.getenv("DEBUG", "True").lower() == "true",
    )

