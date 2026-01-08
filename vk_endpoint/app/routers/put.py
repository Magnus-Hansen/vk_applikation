"""Router til opdatering af uploads og varslingskriterier."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from psycopg2.extensions import connection

import model
from db import cursor
from services import update

router = APIRouter()


@router.put("/varsling", status_code=200)
async def update_varsling(
    kriterie: model.Kriterie,
    conn: Annotated[connection, Depends(cursor.get_db)],
):
    """Opdatere eksisterende varsling baseret på upload_id og station_id."""
    try:
        results = update.varsling(kriterie, conn)
        conn.commit()
        return results
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.put("/upload", status_code=200)
async def update_upload(
    upload: model.Upload,
    conn: Annotated[connection, Depends(cursor.get_db)],
):
    """Opdatere eksisterende upload baseret på upload_id."""
    try:
        results = update.upload(upload, conn)
        conn.commit()
        return results
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e)) from e
