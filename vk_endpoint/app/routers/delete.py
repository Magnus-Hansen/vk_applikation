from fastapi import APIRouter
from services import Delete
from fastapi import Depends, HTTPException
from db import cursor

router = APIRouter()


@router.delete("/{upload_id}", status_code=200)
async def delete_upload(upload_id: int, conn=Depends(cursor.get_db)):
    try:
        results = Delete.upload(upload_id, conn)
        conn.commit()
        return results
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{upload_id}/{station_id}", status_code=204)
async def delete_varsling(upload_id: int, station_id: str, conn=Depends(cursor.get_db)):
    try:
        results = Delete.varsling(upload_id, station_id, conn)
        conn.commit()
        return results
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
