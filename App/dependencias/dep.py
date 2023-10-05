from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession

from App.dapendencias.database import Session


# from jose import jwt, JWTError


async def get_session() -> Generator:
    session: AsyncSession = Session()

    try:  # Abre conexão
        yield session
    finally:  # Fecha conexão
        await session.close()
