from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common import schemas
from common.constants import SourceStatus
from common.database.models import Source


async def create(db: AsyncSession,
                 source: schemas.SourceCreate) -> Source:
    """Create source in the database."""
    db_source = Source(**source.dict())
    db.add(db_source)
    await db.commit()
    await db.refresh(db_source)
    return db_source


async def read(db: AsyncSession, id: int) -> Source:
    """Read source from the database."""
    statement = select(Source).filter(Source.id == id)
    result = await db.execute(statement)
    return result.scalars().first()


async def read_all(db: AsyncSession,
                   status: Optional[SourceStatus] = None) -> list[Source]:
    """Read all sources from the database."""
    statement = select(Source)
    if status is not None:
        statement = statement.filter(Source.status_code == status)
    result = await db.execute(statement)
    return result.scalars().all()


async def update_status(db: AsyncSession, id: int, status: SourceStatus,
                        status_msg: str = None) -> Source:
    """Update source status and status message."""
    db_source = await read(db, id)
    db_source.status_code = status.value
    db_source.status_msg = status_msg
    await db.commit()
    return db_source


async def delete(db: AsyncSession, id: int) -> Source:
    """Delete source from the database."""
    db_source = await read(db, id)
    await db.delete(db_source)
    await db.commit()
    return db_source
