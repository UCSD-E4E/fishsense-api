from sqlmodel import Field, SQLModel


class Fish(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    species_id: int | None = Field(default=None, foreign_key="species.id")
