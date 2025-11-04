"""Label Studio Project model."""

from datetime import datetime

from sqlmodel import DateTime, Field, SQLModel


class LabelStudioProjectDiveMapping(SQLModel, table=True):
    """Association table mapping Label Studio projects to dives."""

    label_studio_project_id: int = Field(
        default=None, foreign_key="labelstudioproject.id", primary_key=True
    )
    dive_id: int = Field(default=None, foreign_key="dive.id", primary_key=True)


class LabelStudioProject(SQLModel, table=True):
    """Model representing a Label Studio project."""

    id: int | None = Field(default=None, primary_key=True)
    label_studio_project_id: int | None = Field(default=None, unique=True, index=True)
    name: str | None = Field(default=None, max_length=255)
    date_created: datetime | None = Field(sa_type=DateTime(timezone=True), default=None)
