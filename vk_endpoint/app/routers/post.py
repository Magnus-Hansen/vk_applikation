from fastapi import APIRouter
from services import Create
from fastapi import Depends, HTTPException
import model
from db import cursor

router = APIRouter()


@router.post("/", status_code=201)
async def post_file(data: model.UploadRequest, conn=Depends(cursor.get_db)):
    try:
        result = Create.file(conn, data.note, data.sommer, data.kriterier)
        conn.commit()
        return result
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
