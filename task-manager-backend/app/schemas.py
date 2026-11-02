"""Pydantic schemas: request validation and response shape."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


def _clean_title(v: str | None) -> str | None:
    if v is None:
        return v
    v = v.strip()
    if not v:
        raise ValueError("title cannot be empty")
    return v


class TaskCreate(BaseModel):
    title: str = Field(..., max_length=100, examples=["Buy groceries"])
    description: str | None = Field(None, max_length=1000)

    _strip_title = field_validator("title")(_clean_title)


class TaskUpdate(BaseModel):
    """All fields optional so the same schema works for partial edits."""
    title: str | None = Field(None, max_length=100)
    description: str | None = Field(None, max_length=1000)
    completed: bool | None = None

    _strip_title = field_validator("title")(_clean_title)


class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    completed: bool
    created_at: datetime
    updated_at: datetime
