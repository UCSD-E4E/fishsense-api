"""Camera Controller for FishSense API."""

from typing import List

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from fishsense_api.config import PG_CONNECTION_STRING
from fishsense_api.database import Database
from fishsense_api.models.camera import Camera
from fishsense_api.models.camera_intrinsics import CameraIntrinsics
from fishsense_api.server import app


@app.get("/api/v1/cameras/")
async def get_cameras() -> List[Camera]:
    """Retrieve all cameras."""
    database = Database(PG_CONNECTION_STRING)
    await database.init_database()

    query = select(Camera)

    async with AsyncSession(database.engine) as session:
        return (await session.exec(query)).all()


@app.get("/api/v1/cameras/{camera_id}")
async def get_camera(camera_id: int) -> Camera | None:
    """Retrieve a camera by its ID."""
    database = Database(PG_CONNECTION_STRING)
    await database.init_database()

    query = select(Camera).where(Camera.id == camera_id)

    async with AsyncSession(database.engine) as session:
        return (await session.exec(query)).first()


@app.get("/api/v1/cameras/{camera_id}/intrinsics/")
async def get_camera_intrinsics(camera_id: int) -> CameraIntrinsics | None:
    """Retrieve camera intrinsics for a given camera ID."""
    database = Database(PG_CONNECTION_STRING)
    await database.init_database()

    query = select(CameraIntrinsics).where(CameraIntrinsics.camera_id == camera_id)

    async with AsyncSession(database.engine) as session:
        return (await session.exec(query)).first()


@app.post("/api/v1/cameras/{camera_id}/intrinsics/", status_code=201)
async def post_camera_intrinsics(camera_id: int, intrinsics: CameraIntrinsics) -> int:
    """Create or update camera intrinsics for a given camera ID."""
    database = Database(PG_CONNECTION_STRING)
    await database.init_database()

    intrinsics.camera_id = camera_id
    async with AsyncSession(database.engine) as session:
        intrinsics = await session.merge(intrinsics)
        await session.flush()

        intrinsics_id = intrinsics.id

        await session.commit()
        return intrinsics_id
