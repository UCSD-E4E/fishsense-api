"""Model representing a user."""

from datetime import datetime

from sqlmodel import DateTime, Field, SQLModel


class User(SQLModel, table=True):
    """Model representing a user."""

    id: int | None = Field(default=None, primary_key=True)
    label_studio_id: int | None = Field(default=None, unique=True, index=True)
    email: str | None = Field(max_length=100, unique=True, index=True)
    first_name: str | None = Field(max_length=100)
    last_name: str | None = Field(max_length=100)
    last_activity: datetime | None = Field(
        sa_type=DateTime(timezone=True), default=None
    )
    date_joined: datetime | None = Field(sa_type=DateTime(timezone=True), default=None)
