from app.model import Kriterie, Upload
from fastapi import HTTPException


def varsling(kriterie: Kriterie, conn):
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE varslingskriterier
                SET 
                    "dkhype_1.1" = %s,
                    "dkhype_5" = %s,
                    "dkhype_20" = %s,
                    "dkhype_50" = %s,
                    varsel = %s,
                    "vandstand_1.1" = %s,
                    "vandstand_2" = %s,
                    "vandstand_5" = %s,
                    "vandstand_10" = %s
                WHERE upload_id = %s AND station_id = %s
                """,
                (
                    kriterie.dkhype.et_et,
                    kriterie.dkhype.fem,
                    kriterie.dkhype.tyve,
                    kriterie.dkhype.halvtres,
                    kriterie.vandstand.varsel,
                    kriterie.vandstand.et_et,
                    kriterie.vandstand.to,
                    kriterie.vandstand.fem,
                    kriterie.vandstand.ti,
                    kriterie.id,
                    kriterie.station_id,
                ),
            )
            if cur.rowcount == 0:
                raise Exception("No upload found with that ID")
        return {"upload": kriterie.id, "station": kriterie.station_id}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def upload(upload: Upload, conn):
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE upload
                SET "date" = %s, "note" = %s, "sommer" = %s
                WHERE id = %s
                """,
                (upload.Datetime, upload.note, upload.sommer, upload.id),
            )
            if cur.rowcount == 0:
                raise Exception("No upload found with that ID")

        return {"upload_id": upload.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
