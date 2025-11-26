from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    """Common fields shared across Note schemas."""
    title: str = Field(..., description="Title of the note", min_length=1, max_length=255)
    content: str = Field(..., description="Content/body of the note")


class NoteCreate(NoteBase):
    """Payload schema for creating a new note."""
    pass


class NoteUpdate(BaseModel):
    """Payload schema for updating an existing note."""
    title: Optional[str] = Field(None, description="Updated title of the note", min_length=1, max_length=255)
    content: Optional[str] = Field(None, description="Updated content/body of the note")


class NoteRead(NoteBase):
    """Response schema representing a note."""
    id: int = Field(..., description="Unique identifier for the note")
    created_at: datetime = Field(..., description="Timestamp when the note was created")
    updated_at: datetime = Field(..., description="Timestamp when the note was last updated")

    class Config:
        from_attributes = True
