from fastapi import APIRouter
from services import Create, Delete, Get, Update

router = APIRouter()

@router.get("/all", status_code=200)
async def get_all_varslinger(conn=Depends(get_db)):
    return Get.all_varslinger(conn)


@router.get("/", status_code=200)
async def get_varslinger(conn=Depends(get_db)):
    return Get.varslinger(conn)


@router.get("/uploads", status_code=200)
async def get_all_uploads(conn=Depends(get_db)):
    return Get.all_uploads(conn)


@router.get("/upload", status_code=200)
async def get_upload(conn=Depends(get_db)):
    return Get.upload(conn)