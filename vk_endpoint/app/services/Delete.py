from fastapi import HTTPException


def upload(upload_id: int, conn):
    try:
        with conn.cursor() as cur:
            deleted_upload = 0
            cur.execute("DELETE FROM upload WHERE id = %s;", (upload_id,))
            deleted_upload = cur.rowcount

        if deleted_upload == 0:
            raise HTTPException(404, detail=f"upload: {upload_id} not found")

        return {"deleted": upload_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def varsling(upload_id: int, station_id: str, conn):
    try:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM varslingskriterier WHERE upload_id = %s AND station_id = %s RETURNING upload_id;",
                (upload_id, station_id),
            )
            deleted_kriterie = cur.fetchone()

            if not deleted_kriterie:
                raise HTTPException(
                    status_code=404,
                    detail=f"kunne ikke finde varsling station: {station_id} upload: {upload_id}",
                )

            cur.execute(
                "SELECT 1 FROM varslingskriterier WHERE upload_id = %s LIMIT 1;",
                (upload_id,),
            )
            still_used = cur.fetchone()

            if not still_used:
                cur.execute("DELETE FROM upload WHERE id = %s;", (upload_id,))
        return {"deleted": station_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
