"""Router til håndtering af fil uploads."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from psycopg2.extensions import connection

import model
from db import cursor
from services import create

router = APIRouter()


@router.post("/", status_code=201)
async def post_file(
    data: model.UploadRequest,
    conn: Annotated[connection, Depends(cursor.get_db)],
) -> dict[int, int]:
    """Opretter en ny upload med tilhørende varslingskriterier."""
    try:
        result = create.file(conn, data.note, data.sommer, data.kriterier)
        conn.commit()
        return result
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e)) from e
