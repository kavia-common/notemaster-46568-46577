# notemaster-46568-46577

Backend: FastAPI (notes_backend)
- Port: 3001 (configure via .env PORT=3001)
- CORS: allow http://localhost:3000 by default (frontend dev)
- Database: SQLite file at ./notes_backend/notes.db by default (DATABASE_URL in .env)

How to run backend locally:
1) cd notes_backend
2) Ensure .env is present (created by repo) or set:
   - DATABASE_URL=sqlite:///./notes.db
   - CORS_ORIGINS=http://localhost:3000
   - PORT=3001
3) Install deps: pip install -r requirements.txt
4) Start server:
   - uvicorn src.api.main:app --host 0.0.0.0 --port ${PORT:-3001}

Frontend configuration (in separate notes_frontend container):
- Create .env with:
  REACT_APP_API_BASE=http://localhost:3001
- The frontend should make requests to `${REACT_APP_API_BASE}/api/notes`.

OpenAPI:
- Visit http://localhost:3001/docs for interactive API docs.
- The OpenAPI schema is also generated to notes_backend/interfaces/openapi.json (update via src/api/generate_openapi.py if schemas change).