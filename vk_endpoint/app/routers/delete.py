"""Håndtere route for delete."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from db import cursor
from services import delete

router = APIRouter()


@router.delete("/{upload_id}", status_code=200)
async def delete_upload(
    upload_id: int,
    conn: Annotated[any, Depends(cursor.get_db)],
):
    """Sletter upload og alle associeret kriterier."""
    try:
        results = delete.upload(upload_id, conn)
        conn.commit()
        return results
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.delete("/{upload_id}/{station_id}", status_code=200)
async def delete_varsling(
    upload_id: int,
    station_id: str,
    conn: Annotated[any, Depends(cursor.get_db)],
):
    """Sletter specifik kriterie.

    Sletter også upload hvis alle kriteier er slettet for den upload.
    """
    try:
        results = delete.varsling(upload_id, station_id, conn)
        conn.commit()
        return results
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e)) from e
