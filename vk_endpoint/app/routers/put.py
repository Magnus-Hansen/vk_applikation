from services import Update
from fastapi import Depends, HTTPException
import model
from fastapi import APIRouter
from db import cursor

router = APIRouter()


@router.put("/varsling", status_code=200)
async def update_varsling(kriterie: model.Kriterie, conn=Depends(cursor.get_db)):
    try:
        results = Update.varsling(kriterie, conn)
        conn.commit()
        return results
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/upload", status_code=200)
async def update_upload(upload: model.Upload, conn=Depends(cursor.get_db)):
    try:
        results = Update.upload(upload, conn)
        conn.commit()
        return results
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
