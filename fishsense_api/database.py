"""Database interaction module for FishSense API Workflow Worker."""

from __future__ import annotations

from typing import Iterable

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel, and_, select
from sqlmodel.ext.asyncio.session import AsyncSession

from fishsense_api.models.camera import Camera
from fishsense_api.models.dive import Dive
from fishsense_api.models.dive_frame_cluster import (
    DiveFrameCluster,
    DiveFrameClusterImageMapping,
)
from fishsense_api.models.dive_slate import DiveSlate
from fishsense_api.models.head_tail_label import HeadTailLabel
from fishsense_api.models.image import Image
from fishsense_api.models.laser_label import LaserLabel
from fishsense_api.models.user import User


class Database:
    # pylint: disable=too-many-public-methods
    """Database interaction class for FishSense API Workflow Worker."""

    def __init__(self, database_url: str):
        self.engine = create_async_engine(database_url)

    async def init_database(self) -> None:
        """Initialize the database by creating all tables."""
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
