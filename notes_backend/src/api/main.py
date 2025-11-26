import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from src.api.notes import router as notes_router
from src.db.database import init_db

# Load .env as early as possible for CORS and server config
load_dotenv()

openapi_tags = [
    {"name": "Health", "description": "Service health and info endpoints."},
    {"name": "Notes", "description": "CRUD operations for managing notes."},
]

app = FastAPI(
    title="Notes Backend API",
    description="Backend API for the Notes application providing CRUD operations for notes.",
    version="0.1.0",
    openapi_tags=openapi_tags,
)

# Initialize database on startup
@app.on_event("startup")
def on_startup() -> None:
    """Initialize database tables on application startup."""
    init_db(drop_all=False)

# CORS configuration from environment (defaults to localhost:3000 for dev)
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000")
allow_origins = [o.strip() for o in cors_origins.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(notes_router)

# PUBLIC_INTERFACE
@app.get("/", summary="Health Check", tags=["Health"])
def health_check():
    """Health check endpoint.

    Returns:
    - 200 OK with a simple payload indicating service health status.
    """
    return {"message": "Healthy"}
