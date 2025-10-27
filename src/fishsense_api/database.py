# pylint: disable=unused-import
"""Database interaction module for FishSense API Workflow Worker."""

from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, and_, select
from sqlmodel.ext.asyncio.session import AsyncSession

from fishsense_api.config import PG_CONNECTION_STRING
from fishsense_api.models.camera import Camera
from fishsense_api.models.camera_intrinsics import CameraIntrinsics
from fishsense_api.models.dive import Dive
from fishsense_api.models.dive_frame_cluster import (
    DiveFrameCluster,
    DiveFrameClusterImageMapping,
)
from fishsense_api.models.dive_slate import DiveSlate
from fishsense_api.models.head_tail_label import HeadTailLabel
from fishsense_api.models.image import Image
from fishsense_api.models.laser_label import LaserLabel
from fishsense_api.models.species_label import SpeciesLabel
from fishsense_api.models.user import User


class Database:
    # pylint: disable=too-few-public-methods

    """Database interaction class for FishSense API Workflow Worker."""

    def __init__(self, database_url: str):
        self.engine = create_async_engine(database_url)

    async def init_database(self, conn: AsyncSession) -> None:
        """Initialize the database by creating all tables."""
        await conn.run_sync(SQLModel.metadata.create_all)

    async def dispose(self) -> None:
        """Dispose of the database engine."""
        await self.engine.dispose()


DATABASE = Database(PG_CONNECTION_STRING)
__ASYNC_SESSION_LOCAL = sessionmaker(
    DATABASE.engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """A context manager for getting a session.

    Yields:
        AsyncSession: An asynchronous database session.
    """
    async with __ASYNC_SESSION_LOCAL() as session:
        yield session
