"""Model for Slate Labels."""

from datetime import datetime
from typing import Any, Dict

from sqlmodel import JSON, Column, DateTime, Field, SQLModel


class DiveSlateLabel(SQLModel, table=True):
    """Model representing slate labels."""

    id: int | None = Field(default=None, primary_key=True)
    label_studio_task_id: int | None = Field(default=None, unique=True, index=True)
    label_studio_project_id: int | None = Field(default=None, index=True)
    image_url: str | None = Field(default=None)
    updated_at: datetime | None = Field(sa_type=DateTime(timezone=True), default=None)
    completed: bool | None = Field(default=False)
    label_studio_json: Dict[str, Any] | None = Field(
        default=None, sa_column=Column(JSON)
    )

    image_id: int | None = Field(default=None, foreign_key="image.id")
    user_id: int | None = Field(default=None, foreign_key="user.id")
