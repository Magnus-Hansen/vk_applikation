from psycopg2.extras import execute_values
from model import Kriterie


def file(conn, note: str | None, sommer: bool, kriterier: list[Kriterie]):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO upload (date, note, sommer) VALUES (CURRENT_DATE, %s, %s) RETURNING id;",
            (note, sommer),
        )
        upload_id = cur.fetchone()[0]

    insert_sql = """
        INSERT INTO varslingskriterier (
            upload_id, "dkhype_1.1", "dkhype_5", "dkhype_20", "dkhype_50", varsel,
            "vandstand_1.1", "vandstand_2", "vandstand_5", "vandstand_10", station_id
        )
        VALUES %s
    """
    seen = set()
    values = []

    for kriterie in kriterier:
        if kriterie.station_id in seen:
            raise Exception(f"der var dublikeret stations_Id: {kriterie.station_id}")
        seen.add(kriterie.station_id)

        values.append(
            (
                upload_id,
                kriterie.dkhype.et_et,
                kriterie.dkhype.fem,
                kriterie.dkhype.tyve,
                kriterie.dkhype.halvtres,
                getattr(kriterie.vandstand, "varsel", None),
                getattr(kriterie.vandstand, "et_et", None),
                getattr(kriterie.vandstand, "to", None),
                getattr(kriterie.vandstand, "fem", None),
                getattr(kriterie.vandstand, "ti", None),
                kriterie.station_id,
            )
        )
    with conn.cursor() as cur:
        execute_values(cur, insert_sql, values)
    return {"upload_id": upload_id, "rows_inserted": len(values)}
