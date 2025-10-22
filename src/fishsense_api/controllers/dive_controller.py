"""Dive Controller for FishSense API."""

from typing import List

from fastapi import Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from fishsense_api.database import Database, get_async_session
from fishsense_api.models.dive import Dive
from fishsense_api.server import app


@app.get("/api/v1/dives/")
async def get_dives(session: AsyncSession = Depends(get_async_session)) -> List[Dive]:
    """Retrieve all dives."""
    query = select(Dive)

    return (await session.exec(query)).all()


@app.get("/api/v1/dives/{dive_id}")
async def get_dive(
    dive_id: int, session: AsyncSession = Depends(get_async_session)
) -> Dive | None:
    """Retrieve a dive by its ID."""
    query = select(Dive).where(Dive.id == dive_id)

    return (await session.exec(query)).first()
