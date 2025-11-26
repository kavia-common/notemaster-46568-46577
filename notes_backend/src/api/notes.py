from typing import List, Optional, Tuple

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session

from src.api.deps import get_db_session
from src.db import models
from src.db.schemas import NoteCreate, NoteRead, NoteUpdate

router = APIRouter(
    prefix="/api/notes",
    tags=["Notes"],
)


def _parse_sort(sort: Optional[str]) -> Tuple:
    """Parse sort parameter like 'created_at:desc' or 'title:asc' into SQLAlchemy order_by expression."""
    if not sort:
        return (desc(models.Note.created_at),)

    parts = sort.split(",")
    orders = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if ":" in part:
            field, direction = part.split(":", 1)
        else:
            field, direction = part, "asc"
        field = field.strip()
        direction = direction.strip().lower()

        # Map allowed sortable fields
        if field not in {"id", "title", "created_at", "updated_at"}:
            # Ignore unknown fields for safety; alternatively, raise a 400 error
            continue

        column = getattr(models.Note, field)
        orders.append(asc(column) if direction == "asc" else desc(column))

    if not orders:
        orders = [desc(models.Note.created_at)]
    return tuple(orders)


# PUBLIC_INTERFACE
@router.get(
    "",
    response_model=List[NoteRead],
    summary="List notes",
    description="List notes with optional search by title/content. Supports pagination and sorting.",
)
def list_notes(
    q: Optional[str] = Query(None, description="Search query for title or content"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of notes to return"),
    offset: int = Query(0, ge=0, description="Number of notes to skip"),
    sort: Optional[str] = Query(
        None,
        description="Comma-separated sort fields, e.g. 'created_at:desc,title:asc'. Defaults to '-created_at'.",
    ),
    db: Session = Depends(get_db_session),
) -> List[NoteRead]:
    """Return a list of notes filtered by optional query and sorted with pagination."""
    stmt = select(models.Note)
    if q:
        # Basic LIKE filter on title or content
        like = f"%{q}%"
        stmt = stmt.where((models.Note.title.ilike(like)) | (models.Note.content.ilike(like)))
    stmt = stmt.order_by(*_parse_sort(sort)).limit(limit).offset(offset)
    results = db.execute(stmt).scalars().all()
    return results


# PUBLIC_INTERFACE
@router.get(
    "/{note_id}",
    response_model=NoteRead,
    summary="Get note by ID",
    description="Retrieve a single note by its unique identifier.",
)
def get_note(
    note_id: int,
    db: Session = Depends(get_db_session),
) -> NoteRead:
    """Get a note by ID or return 404 if not found."""
    note = db.get(models.Note, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


# PUBLIC_INTERFACE
@router.post(
    "",
    response_model=NoteRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create note",
    description="Create a new note with a title and content.",
)
def create_note(
    payload: NoteCreate,
    db: Session = Depends(get_db_session),
) -> NoteRead:
    """Create and persist a new note."""
    note = models.Note(title=payload.title, content=payload.content)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


# PUBLIC_INTERFACE
@router.put(
    "/{note_id}",
    response_model=NoteRead,
    summary="Update note",
    description="Update an existing note's fields.",
)
def update_note(
    note_id: int,
    payload: NoteUpdate,
    db: Session = Depends(get_db_session),
) -> NoteRead:
    """Update a note by ID; returns 404 if not found."""
    note = db.get(models.Note, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    # Apply changes only if provided
    if payload.title is not None:
        note.title = payload.title
    if payload.content is not None:
        note.content = payload.content

    db.add(note)
    db.commit()
    db.refresh(note)
    return note


# PUBLIC_INTERFACE
@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete note",
    description="Delete a note by its ID.",
)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db_session),
) -> None:
    """Delete a note; no content returned if successful."""
    note = db.get(models.Note, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    db.delete(note)
    db.commit()
    return None
