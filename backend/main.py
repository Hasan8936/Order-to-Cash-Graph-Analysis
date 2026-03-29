"""
FastAPI main application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from .api import graph, chat, health
from .db.connection import init_db
from .graph.builder import build_graph

# Initialize FastAPI app
app = FastAPI(
    title="Order-to-Cash Graph API",
    description="LLM-powered graph analysis of SAP O2C data",
    version="1.0.0"
)

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(health.router)
app.include_router(graph.router)
app.include_router(chat.router)


@app.on_event("startup")
async def startup_event():
    """
    Initialize database and build graph on startup.
    """
    print("Starting O2C Graph API...")
    print(f"GEMINI_API_KEY set: {bool(os.getenv('GEMINI_API_KEY'))}")
    print(f"GROQ_API_KEY set: {bool(os.getenv('GROQ_API_KEY'))}")
    print(f"LLM_PROVIDER: {os.getenv('LLM_PROVIDER', 'gemini')}")
    
    # Initialize database if needed
    db_path = os.getenv("DB_PATH", "backend/o2c.db")
    if not os.path.exists(db_path):
        print("Database not found, initializing...")
        try:
            init_db()
        except Exception as e:
            print(f"Warning: Database initialization failed: {e}")
    
    # Pre-build graph for faster first request
    try:
        print("Building graph...")
        build_graph()
        print("Graph built successfully")
    except Exception as e:
        print(f"Warning: Graph build failed: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    print("Shutting down O2C Graph API")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "Order-to-Cash Graph API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "graph": "/api/graph",
            "chat": "/api/chat"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        
        reload=os.getenv("ENV") != "production"
    )
