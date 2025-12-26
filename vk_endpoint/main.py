import model
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from connection import get_conn, put_conn
from CRUD import Get, Update, Delete, Create


app = FastAPI()

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Connection dependency
def get_db():
    conn = get_conn()
    try:
        yield conn
    finally:
        put_conn(conn)


# Cursor dependency
def get_cursor(conn=Depends(get_db)):
    with conn.cursor() as cur:
        yield cur
        # Cursor closes automatically at the end of request


@app.get("/all", status_code=200)
async def get_all_varslinger(conn=Depends(get_db)):
    return Get.all_varslinger(conn)


@app.get("/", status_code=200)
async def get_varslinger(conn=Depends(get_db)):
    return Get.varslinger(conn)


@app.get("/uploads", status_code=200)
async def get_all_uploads(conn=Depends(get_db)):
    return Get.all_uploads(conn)


@app.get("/upload", status_code=200)
async def get_upload(conn=Depends(get_db)):
    return Get.upload(conn)


@app.put("/varsling", status_code=200)
async def update_varsling(kriterie: model.Kriterie, conn=Depends(get_db)):
    try:
        results = Update.varsling(kriterie, conn)
        conn.commit()
        return results
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/upload", status_code=200)
async def update_upload(upload: model.Upload, conn=Depends(get_db)):
    try:
        results = Update.upload(upload, conn)
        conn.commit()
        return results
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/{upload_id}", status_code=200)
async def delete_upload(upload_id: int, conn=Depends(get_db)):
    try:
        results = Delete.upload(upload_id, conn)
        conn.commit()
        return results
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/{upload_id}/{station_id}", status_code=204)
async def delete_varsling(upload_id: int, station_id: str, conn=Depends(get_db)):
    try:
        results = Delete.varsling(upload_id, station_id, conn)
        conn.commit()
        return results
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/", status_code=201)
async def post_file(data: model.UploadRequest, conn=Depends(get_db)):
    try:
        result = Create.file(conn, data.note, data.sommer, data.kriterier)
        conn.commit()
        return result
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
