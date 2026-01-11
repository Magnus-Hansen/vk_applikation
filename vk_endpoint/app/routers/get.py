"""Router til hentning af uploads og varslingskriterier."""

from typing import Annotated

from fastapi import APIRouter, Depends
from psycopg2.extensions import connection

from app.model import Kriterie, Upload
from db import cursor
from services import get

router = APIRouter()


@router.get("/all", status_code=200)
async def get_all_varslinger(
    conn: Annotated[connection, Depends(cursor.get_db)],
) -> list[Kriterie]:
    """Hent alle varslingskriterier uanset upload."""
    return get.all_varslinger(conn)


@router.get("/", status_code=200)
async def get_varslinger(
    conn: Annotated[connection, Depends(cursor.get_db)],
) -> list[Kriterie]:
    """Hent varslingskriterier for nyeste upload."""
    return get.varslinger(conn)


@router.get("/uploads", status_code=200)
async def get_all_uploads(
    conn: Annotated[connection, Depends(cursor.get_db)],
) -> list[Upload]:
    """Hent alle uploads."""
    return get.all_uploads(conn)


@router.get("/upload", status_code=200)
async def get_upload(conn: Annotated[connection, Depends(cursor.get_db)]) -> Upload:
    """Hent nyeste upload."""
    return get.upload(conn)
