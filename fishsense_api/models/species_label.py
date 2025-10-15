from datetime import datetime
from typing import Any, Dict

from sqlmodel import JSON, Column, DateTime, Field, SQLModel

from fishsense_api.models.label_studio_label_base import LabelStudioLabelBase


class SpeciesLabel(LabelStudioLabelBase, SQLModel, table=True):
    """Model representing a species label."""

    id: int | None = Field(default=None, primary_key=True)
    label_studio_task_id: int | None = Field(default=None, unique=True, index=True)
    image_url: str | None = Field(default=None)
    updated_at: datetime | None = Field(sa_type=DateTime(timezone=True), default=None)
    completed: bool | None = Field(default=False)
    label_studio_json: Dict[str, Any] | None = Field(
        default=None, sa_column=Column(JSON)
    )

    image_id: int | None = Field(default=None, foreign_key="image.id")
    user_id: int | None = Field(default=None, foreign_key="user.id")
