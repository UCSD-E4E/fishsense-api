from sqlmodel import Field, SQLModel


class Species(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    scientific_name: str | None = Field(default=None, index=True)
    common_name: str | None = Field(default=None, index=True)
