from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from fishsense_api.config import PG_CONNECTION_STRING
from fishsense_api.database import Database
from fishsense_api.models.laser_label import LaserLabel
from fishsense_api.models.species_label import SpeciesLabel
from fishsense_api.server import app


@app.get("/api/v1/labels/laser/{image_id}")
async def get_laser_label(image_id: int) -> LaserLabel:
    database = Database(PG_CONNECTION_STRING)
    await database.init_database()

    query = select(LaserLabel).where(LaserLabel.image_id == image_id)

    async with AsyncSession(database.engine) as session:
        return (await session.exec(query)).first()


@app.get("/api/v1/labels/species/{image_id}")
async def get_species_label(image_id: int) -> SpeciesLabel:
    database = Database(PG_CONNECTION_STRING)
    await database.init_database()

    query = select(SpeciesLabel).where(SpeciesLabel.image_id == image_id)

    async with AsyncSession(database.engine) as session:
        return (await session.exec(query)).first()


@app.post("/api/v1/labels/species/{image_id}", status_code=201)
async def post_species_label(image_id: int, label: SpeciesLabel) -> int:
    database = Database(PG_CONNECTION_STRING)
    await database.init_database()

    label.image_id = image_id

    async with AsyncSession(database.engine) as session:
        label = await session.merge(label)
        await session.flush()

        label_id = label.id

        await session.commit()
        return label_id
