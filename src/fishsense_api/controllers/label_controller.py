"""Label Controller for FishSense API."""

from fastapi import Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from fishsense_api.database import get_async_session
from fishsense_api.models.laser_label import LaserLabel
from fishsense_api.models.species_label import SpeciesLabel
from fishsense_api.server import app


@app.get("/api/v1/labels/laser/{image_id}")
async def get_laser_label(
    image_id: int, session: AsyncSession = Depends(get_async_session)
) -> LaserLabel | None:
    """Retrieve a laser label for a given image ID."""

    query = select(LaserLabel).where(LaserLabel.image_id == image_id)

    return (await session.exec(query)).first()


@app.get("/api/v1/labels/species/{image_id}")
async def get_species_label(
    image_id: int, session: AsyncSession = Depends(get_async_session)
) -> SpeciesLabel | None:
    """Retrieve a species label for a given image ID."""
    query = select(SpeciesLabel).where(SpeciesLabel.image_id == image_id)

    return (await session.exec(query)).first()


@app.post("/api/v1/labels/species/{image_id}", status_code=201)
async def post_species_label(
    image_id: int,
    label: SpeciesLabel,
    session: AsyncSession = Depends(get_async_session),
) -> int:
    """Create or update a species label for a given image ID."""
    label.image_id = image_id

    label = await session.merge(label)
    await session.flush()

    label_id = label.id

    await session.commit()
    return label_id
