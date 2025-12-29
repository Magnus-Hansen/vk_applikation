from fastapi import HTTPException
from app.model import Kriterie, Vandstand, Dkhype, Upload


def all_varslinger(conn) -> list[Kriterie]:
    try:
        with conn.cursor() as cur:
            cur.execute("""SELECT * FROM varslingskriterier;""")
            rows = cur.fetchall()
            if not rows:
                return []

            colnames = [desc[0] for desc in cur.description]
            data = []

            for row in rows:
                row_dict = dict(zip(colnames, row))
                kriterie = Kriterie(
                    id=row_dict.get("upload_id"),
                    vandstand=Vandstand(
                        **{
                            "varsel": row_dict.get("varsel"),
                            "1.1": row_dict.get("vandstand_1.1"),
                            "2": row_dict.get("vandstand_2"),
                            "5": row_dict.get("vandstand_5"),
                            "10": row_dict.get("vandstand_10"),
                        }
                    ),
                    dkhype=Dkhype(
                        **{
                            "1.1": row_dict.get("dkhype_1.1"),
                            "5": row_dict.get("dkhype_5"),
                            "20": row_dict.get("dkhype_20"),
                            "50": row_dict.get("dkhype_50"),
                        }
                    ),
                    station_id=row_dict.get("station_id"),
                )
                data.append(kriterie)

        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def varslinger(conn) -> list[Kriterie]:
    try:
        with conn.cursor() as cur:
            cur.execute("""SELECT vk.*
                FROM varslingskriterier vk
                JOIN upload ud ON vk.upload_id = ud.id
                WHERE vk.upload_id = (SELECT MAX(id) FROM upload);""")
            rows = cur.fetchall()
            if not rows:
                return []

            colnames = [desc[0] for desc in cur.description]
            data = []

            for row in rows:
                row_dict = dict(zip(colnames, row))
                kriterie = Kriterie(
                    id=row_dict.get("upload_id"),
                    vandstand=Vandstand(
                        **{
                            "varsel": row_dict.get("varsel"),
                            "1.1": row_dict.get("vandstand_1.1"),
                            "2": row_dict.get("vandstand_2"),
                            "5": row_dict.get("vandstand_5"),
                            "10": row_dict.get("vandstand_10"),
                        }
                    ),
                    dkhype=Dkhype(
                        **{
                            "1.1": row_dict.get("dkhype_1.1"),
                            "5": row_dict.get("dkhype_5"),
                            "20": row_dict.get("dkhype_20"),
                            "50": row_dict.get("dkhype_50"),
                        }
                    ),
                    station_id=row_dict.get("station_id"),
                )
                data.append(kriterie)

        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def all_uploads(conn) -> list[Upload]:
    try:
        with conn.cursor() as cur:
            cur.execute("""SELECT * FROM Upload;""")
            rows = cur.fetchall()
            if not rows:
                return []

            colnames = [desc[0] for desc in cur.description]
            data = []

            for row in rows:
                row_dict = dict(zip(colnames, row))
                upload = Upload(
                    id=row_dict.get("id"),
                    Datetime=row_dict.get("date"),
                    note=row_dict.get("note"),
                    sommer=row_dict.get("sommer"),
                )
                data.append(upload)

        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def upload(conn) -> Upload:
    try:
        with conn.cursor() as cur:
            cur.execute("""SELECT * FROM Upload ORDER BY id DESC LIMIT 1""")
            row = cur.fetchone()
            if not row:
                return None

            return Upload(id=row[0], Datetime=row[1], note=row[2], sommer=row[3])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
