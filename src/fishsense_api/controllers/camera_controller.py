"""Camera Controller for FishSense API."""

from typing import List

from fastapi import Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from fishsense_api.database import get_async_session
from fishsense_api.models.camera import Camera
from fishsense_api.models.camera_intrinsics import CameraIntrinsics
from fishsense_api.server import app


@app.get("/api/v1/cameras/")
async def get_cameras(
    session: AsyncSession = Depends(get_async_session),
) -> List[Camera]:
    """Retrieve all cameras."""
    query = select(Camera)

    return (await session.exec(query)).all()


@app.get("/api/v1/cameras/{camera_id}")
async def get_camera(
    camera_id: int, session: AsyncSession = Depends(get_async_session)
) -> Camera | None:
    """Retrieve a camera by its ID."""
    query = select(Camera).where(Camera.id == camera_id)

    return (await session.exec(query)).first()


@app.get("/api/v1/cameras/{camera_id}/intrinsics/")
async def get_camera_intrinsics(
    camera_id: int, session: AsyncSession = Depends(get_async_session)
) -> CameraIntrinsics | None:
    """Retrieve camera intrinsics for a given camera ID."""
    query = select(CameraIntrinsics).where(CameraIntrinsics.camera_id == camera_id)

    return (await session.exec(query)).first()


@app.put("/api/v1/cameras/{camera_id}/intrinsics/", status_code=201)
async def put_camera_intrinsics(
    camera_id: int,
    intrinsics: CameraIntrinsics,
    session: AsyncSession = Depends(get_async_session),
) -> int:
    """Create or update camera intrinsics for a given camera ID."""
    intrinsics.camera_id = camera_id

    intrinsics = await session.merge(intrinsics)
    await session.flush()

    intrinsics_id = intrinsics.id

    return intrinsics_id
