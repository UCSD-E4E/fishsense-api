from typing import List

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from fishsense_api.config import PG_CONNECTION_STRING
from fishsense_api.database import Database
from fishsense_api.models.dive import Dive
from fishsense_api.server import app


@app.get("/api/v1/dives/")
async def get_dives() -> List[Dive]:
    database = Database(PG_CONNECTION_STRING)
    await database.init_database()

    query = select(Dive)

    async with AsyncSession(database.engine) as session:
        return (await session.exec(query)).all()


@app.get("/api/v1/dives/{dive_id}")
async def get_dive(dive_id: int) -> Dive | None:
    database = Database(PG_CONNECTION_STRING)
    await database.init_database()

    query = select(Dive).where(Dive.id == dive_id)

    async with AsyncSession(database.engine) as session:
        return (await session.exec(query)).first()
