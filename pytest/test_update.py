from CRUD import Create, Update
from model import Kriterie, Dkhype, Vandstand, Upload_get
import pytest

kriterie1 = Kriterie(
    dkhype=Dkhype(**{"1.1": 4.0, "5": 8.7, "20": 13.7, "50": 18.1}),
    vandstand=Vandstand(
        **{"varsel": 1.5, "1.1": 1.69, "2": 2.09, "5": 2.34, "10": 2.5}
    ),
    station_id="02001038",
)


class TestClassUpdate:
    def test_update_varslinger(self, conn):
        kriterie2 = Kriterie(
            dkhype=Dkhype(**{"1.1": 0.0, "5": 0.0, "20": 0.0, "50": 0.0}),
            vandstand=Vandstand(
                **{"varsel": 0.0, "1.1": 0.0, "2": 0.0, "5": 0.0, "10": 0.0}
            ),
            id="1",
            station_id="02001038",
        )
        Create.file(conn, None, False, [kriterie1])
        result = Update.varsling(kriterie2, conn)
        assert result == {"upload": kriterie2.id, "station": kriterie2.station_id}

    def test_update_varslinger_none(self, conn):
        Create.file(conn, None, False, [kriterie1])
        kriterie2 = Kriterie(
            dkhype=Dkhype(**{"1.1": None, "5": None, "20": None, "50": None}),
            vandstand=Vandstand(
                **{"varsel": None, "1.1": None, "2": None, "5": None, "10": None}
            ),
            id="1",
            station_id="02001038",
        )
        result = Update.varsling(kriterie2, conn)
        assert result == {"upload": kriterie2.id, "station": kriterie2.station_id}

    def test_update_varslinger_fail_wrong_stationid(self, conn):
        with pytest.raises(Exception):
            Create.file(conn, None, False, [kriterie1])
            kriterie2 = Kriterie(
                dkhype=Dkhype(**{"1.1": 0.0, "5": 0.0, "20": 0.0, "50": 0.0}),
                vandstand=Vandstand(
                    **{"varsel": 0.0, "1.1": 0.0, "2": 0.0, "5": 0.0, "10": 0.0}
                ),
                id="1",
                station_id="2001038",
            )
            result = Update.varsling(kriterie2, conn)
            assert result == {"upload": kriterie2.id, "station": kriterie2.station_id}

    def test_update_varslinger_fail_wrong_id(self, conn):
        with pytest.raises(Exception):
            Create.file(conn, None, False, [kriterie1])
            kriterie2 = Kriterie(
                dkhype=Dkhype(**{"1.1": 0.0, "5": 0.0, "20": 0.0, "50": 0.0}),
                vandstand=Vandstand(
                    **{"varsel": 0.0, "1.1": 0.0, "2": 0.0, "5": 0.0, "10": 0.0}
                ),
                id="2",
                station_id="02001038",
            )
            result = Update.varsling(kriterie2, conn)
            assert result == {"upload": kriterie2.id, "station": kriterie2.station_id}

    def test_update_varslinger_fail_wrongformat_string(self, conn):
        with pytest.raises(Exception):
            Create.file(conn, None, False, [kriterie1])
            kriterie2 = Kriterie(
                dkhype=Dkhype(**{"1.1": "0.0", "5": "0.0", "20": "0.0", "50": "0.0"}),
                vandstand=Vandstand(
                    **{
                        "varsel": "0.0",
                        "1.1": "0.0",
                        "2": "0.0",
                        "5": "0.0",
                        "10": "0.0",
                    }
                ),
                id="1",
                station_id="2001038",
            )
            result = Update.varsling(kriterie2, conn)
            assert result == {"upload": kriterie2.id, "station": kriterie2.station_id}

    def test_update_varslinger_fail_wrongformat_int(self, conn):
        with pytest.raises(Exception):
            Create.file(conn, None, False, [kriterie1])
            kriterie2 = Kriterie(
                dkhype=Dkhype(**{"1.1": 0, "5": 0, "20": 0, "50": 0}),
                vandstand=Vandstand(**{"varsel": 0, "1.1": 0, "2": 0, "5": 0, "10": 0}),
                id="1",
                station_id="2001038",
            )
            result = Update.varsling(kriterie2, conn)
            assert result == {"upload": kriterie2.id, "station": kriterie2.station_id}

    def test_update_upload(self, conn):
        upload2 = Upload_get(id="1", Datetime="2025-12-22", note="test", sommer=False)
        Create.file(conn, None, False, [kriterie1])
        result = Update.upload(upload2, conn)
        assert result == {"upload_id": upload2.id}

    def test_update_upload_no_note(self, conn):
        upload2 = Upload_get(id="1", Datetime="2025-12-22", note=None, sommer=False)
        Create.file(conn, None, False, [kriterie1])
        result = Update.upload(upload2, conn)
        assert result == {"upload_id": upload2.id}

    def test_update_upload_no_date_fail(self, conn):
        with pytest.raises(Exception):
            upload2 = Upload_get(id="1", Datetime=None, note="test", sommer=False)
            Create.file(conn, None, False, [kriterie1])
            result = Update.upload(upload2, conn)
            assert result == {"upload_id": upload2.id}

    def test_update_upload_no_sommer_fail(self, conn):
        with pytest.raises(Exception):
            upload2 = Upload_get(
                id="1", Datetime="2025-12-22", note="test", sommer=None
            )
            Create.file(conn, None, False, [kriterie1])
            result = Update.upload(upload2, conn)
            assert result == {"upload_id": upload2.id}

    def test_update_upload_wrong_id(self, conn):
        with pytest.raises(Exception):
            upload2 = Upload_get(
                id="3", Datetime="2025-12-22", note="test", sommer=False
            )
            Create.file(conn, None, False, [kriterie1])
            result = Update.upload(upload2, conn)
            assert result == {"upload_id": upload2.id}
