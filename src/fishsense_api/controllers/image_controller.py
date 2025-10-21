"""Image Controller for FishSense API."""

import asyncio
from typing import List

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from fishsense_api.config import PG_CONNECTION_STRING
from fishsense_api.database import Database
from fishsense_api.models.dive_frame_cluster import (
    DiveFrameCluster,
    DiveFrameClusterImageMapping,
    DiveFrameClusterJson,
)
from fishsense_api.models.image import Image
from fishsense_api.server import app


@app.get("/api/v1/images/{image_id}")
async def get_image(image_id: int) -> Image | None:
    """Retrieve an image by its ID."""
    database = Database(PG_CONNECTION_STRING)
    await database.init_database()

    query = select(Image).where(Image.id == image_id)

    async with AsyncSession(database.engine) as session:
        return (await session.exec(query)).first()


@app.get("/api/v1/dives/{dive_id}/images/")
async def get_dive_images(dive_id: int) -> List[Image] | None:
    """Retrieve all images associated with a specific dive ID."""
    database = Database(PG_CONNECTION_STRING)
    await database.init_database()

    query = select(Image).where(Image.dive_id == dive_id)

    async with AsyncSession(database.engine) as session:
        return (await session.exec(query)).all()


@app.get("/api/v1/dives/{dive_id}/images/clusters/")
async def get_clusters(dive_id: int) -> List[DiveFrameClusterJson] | None:
    """Retrieve all image clusters associated with a specific dive ID."""
    database = Database(PG_CONNECTION_STRING)
    await database.init_database()

    query = select(DiveFrameCluster).where(DiveFrameCluster.dive_id == dive_id)

    async with AsyncSession(database.engine) as session:
        clusters = (await session.exec(query)).all()
        cluster_queries = [
            select(DiveFrameClusterImageMapping).where(
                DiveFrameClusterImageMapping.dive_frame_cluster_id == c.id
            )
            for c in clusters
        ]

        cluster_mappings = await asyncio.gather(
            *[session.exec(q) for q in cluster_queries]
        )
        return [
            DiveFrameClusterJson(id=c.id, image_ids=[m.image_id for m in ms])
            for c, ms in zip(clusters, cluster_mappings)
        ]


@app.post("/api/v1/dives/{dive_id}/images/clusters/", status_code=201)
async def post_cluster(dive_id: int, image_ids: List[int]) -> int:
    """Create a new image cluster for a specific dive ID."""
    database = Database(PG_CONNECTION_STRING)
    await database.init_database()

    async with AsyncSession(database.engine) as session:
        images = (
            await session.exec(
                select(Image).where(
                    Image.id.in_(image_ids)  # pylint: disable=no-member
                )
            )
        ).all()

        dive_frame_cluster = DiveFrameCluster(dive_id=dive_id)
        dive_frame_cluster = await session.merge(dive_frame_cluster)
        await session.flush()  # Ensure ID is populated

        dive_frame_cluster_id = dive_frame_cluster.id  # Access ID to ensure it's loaded

        mappings = []
        for image in images:
            mapping = DiveFrameClusterImageMapping(
                dive_frame_cluster_id=dive_frame_cluster.id, image_id=image.id
            )
            mappings.append(mapping)

        session.add_all(mappings)

        await session.commit()

    return dive_frame_cluster_id
