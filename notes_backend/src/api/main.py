from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.db.database import init_db

app = FastAPI(
    title="Notes Backend API",
    description="Backend API for the Notes application providing CRUD operations for notes.",
    version="0.1.0",
)

# Initialize database on startup
@app.on_event("startup")
def on_startup() -> None:
    """Initialize database tables on application startup."""
    init_db(drop_all=False)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# PUBLIC_INTERFACE
@app.get("/", summary="Health Check", tags=["Health"])
def health_check():
    """Health check endpoint.

    Returns:
    - 200 OK with a simple payload indicating service health status.
    """
    return {"message": "Healthy"}
