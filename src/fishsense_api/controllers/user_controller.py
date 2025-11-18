"""Controller for user-related API endpoints."""

from typing import List

from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from fishsense_api.database import get_async_session
from fishsense_api.models.user import User
from fishsense_api.server import app


@app.get("/api/v1/users/")
async def get_users(session: AsyncSession = Depends(get_async_session)) -> List[User]:
    """Retrieve all users."""

    query = select(User)
    results = await session.exec(query)
    return results.all()


@app.get("/api/v1/users/{user_id}")
async def get_user(
    user_id: int, session: AsyncSession = Depends(get_async_session)
) -> User | None:
    """Retrieve a user by their ID."""

    query = select(User).where(User.id == user_id)
    result = await session.exec(query)
    return result.first()


@app.get("/api/v1/users/email/{email}")
async def get_user_by_email(
    email: str, session: AsyncSession = Depends(get_async_session)
) -> User | None:
    """Retrieve a user by their email."""

    query = select(User).where(User.email == email)
    result = await session.exec(query)
    return result.first()


@app.post("/api/v1/users/", status_code=201)
async def create_user(
    user: User, session: AsyncSession = Depends(get_async_session)
) -> int:
    """Create a new user."""
    user = User.model_validate(jsonable_encoder(user))
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user.id


@app.put("/api/v1/users/{user_id}", status_code=201)
async def create_or_update_user(
    user_id: int,
    user: User,
    session: AsyncSession = Depends(get_async_session),
) -> int:
    """Create or update a user by their ID."""
    user = User.model_validate(jsonable_encoder(user))
    user.id = user_id

    user = await session.merge(user)
    await session.flush()

    user_id = user.id

    await session.commit()
    return user_id
