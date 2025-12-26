from CRUD import Create, Get
from model import Kriterie, Dkhype, Vandstand, Upload_get
import pytest
import datetime


class TestClassDelete:
    def test_get_varslinger(self, conn):
        kriterie1 = Kriterie(
            dkhype=Dkhype(**{"1.1": 4.0, "5": 8.7, "20": 13.7, "50": 18.1}),
            vandstand=Vandstand(
                **{"varsel": 1.5, "1.1": 1.69, "2": 2.09, "5": 2.34, "10": 2.5}
            ),
            station_id="02001038",
        )
        kriterie2 = Kriterie(
            dkhype=Dkhype(**{"1.1": 2.2, "5": 4.4, "20": 6.6, "50": 8.8}),
            vandstand=Vandstand(
                **{"varsel": 2.5, "1.1": 3.69, "2": 4.09, "5": 5.34, "10": 6.5}
            ),
            station_id="88888888",
        )
        Create.file(conn, None, False, [kriterie1])
        Create.file(conn, None, False, [kriterie2])
        kriterie2.id = 2
        assert Get.varslinger(conn) == [kriterie2]

    def test_get_varslinger_fail(self, conn):
        with pytest.raises(Exception):
            kriterie1 = Kriterie(
                dkhype=Dkhype(**{"1.1": 4.0, "5": 8.7, "20": 13.7, "50": 18.1}),
                vandstand=Vandstand(
                    **{"varsel": 1.5, "1.1": 1.69, "2": 2.09, "5": 2.34, "10": 2.5}
                ),
                station_id="02001038",
            )
            kriterie2 = Kriterie(
                dkhype=Dkhype(**{"1.1": 2.2, "5": 4.4, "20": 6.6, "50": 8.8}),
                vandstand=Vandstand(
                    **{"varsel": 2.5, "1.1": 3.69, "2": 4.09, "5": 5.34, "10": 6.5}
                ),
                station_id="88888888",
            )
            Create.file(conn, None, False, [kriterie1])
            Create.file(conn, None, False, [kriterie2])
            kriterie1.id = 1
            assert Get.varslinger(conn) == [kriterie1]

    def test_get_all_varslinger(self, conn):
        kriterie1 = Kriterie(
            dkhype=Dkhype(**{"1.1": 4.0, "5": 8.7, "20": 13.7, "50": 18.1}),
            vandstand=Vandstand(
                **{"varsel": 1.5, "1.1": 1.69, "2": 2.09, "5": 2.34, "10": 2.5}
            ),
            station_id="02001038",
        )
        kriterie2 = Kriterie(
            dkhype=Dkhype(**{"1.1": 2.2, "5": 4.4, "20": 6.6, "50": 8.8}),
            vandstand=Vandstand(
                **{"varsel": 2.5, "1.1": 3.69, "2": 4.09, "5": 5.34, "10": 6.5}
            ),
            station_id="88888888",
        )
        Create.file(conn, None, False, [kriterie1])
        Create.file(conn, None, False, [kriterie2])
        kriterie1.id = 1
        kriterie2.id = 2
        assert Get.all_varslinger(conn) == [kriterie1, kriterie2]

    def test_get_all_uploads(self, conn):
        kriterie1 = Kriterie(
            dkhype=Dkhype(**{"1.1": 4.0, "5": 8.7, "20": 13.7, "50": 18.1}),
            vandstand=Vandstand(
                **{"varsel": 1.5, "1.1": 1.69, "2": 2.09, "5": 2.34, "10": 2.5}
            ),
            station_id="02001038",
        )
        kriterie2 = Kriterie(
            dkhype=Dkhype(**{"1.1": 2.2, "5": 4.4, "20": 6.6, "50": 8.8}),
            vandstand=Vandstand(
                **{"varsel": 2.5, "1.1": 3.69, "2": 4.09, "5": 5.34, "10": 6.5}
            ),
            station_id="88888888",
        )
        Create.file(conn, None, False, [kriterie1])
        Create.file(conn, None, False, [kriterie2])
        dateTime = datetime.datetime.now()
        date = dateTime.date()
        upload1 = Upload_get(id=1, Datetime=date, note=None, sommer=False)
        upload2 = Upload_get(id=2, Datetime=date, note=None, sommer=False)
        assert Get.all_uploads(conn) == [upload1, upload2]

    def test_get_upload(self, conn):
        kriterie1 = Kriterie(
            dkhype=Dkhype(**{"1.1": 4.0, "5": 8.7, "20": 13.7, "50": 18.1}),
            vandstand=Vandstand(
                **{"varsel": 1.5, "1.1": 1.69, "2": 2.09, "5": 2.34, "10": 2.5}
            ),
            station_id="02001038",
        )
        kriterie2 = Kriterie(
            dkhype=Dkhype(**{"1.1": 2.2, "5": 4.4, "20": 6.6, "50": 8.8}),
            vandstand=Vandstand(
                **{"varsel": 2.5, "1.1": 3.69, "2": 4.09, "5": 5.34, "10": 6.5}
            ),
            station_id="88888888",
        )
        Create.file(conn, None, False, [kriterie1])
        Create.file(conn, None, False, [kriterie2])
        dateTime = datetime.datetime.now()
        date = dateTime.date()
        upload2 = Upload_get(id=2, Datetime=date, note=None, sommer=False)
        assert Get.upload(conn) == upload2

    def test_get_upload_fail(self, conn):
        with pytest.raises(Exception):
            kriterie1 = Kriterie(
                dkhype=Dkhype(**{"1.1": 4.0, "5": 8.7, "20": 13.7, "50": 18.1}),
                vandstand=Vandstand(
                    **{"varsel": 1.5, "1.1": 1.69, "2": 2.09, "5": 2.34, "10": 2.5}
                ),
                station_id="02001038",
            )
            kriterie2 = Kriterie(
                dkhype=Dkhype(**{"1.1": 2.2, "5": 4.4, "20": 6.6, "50": 8.8}),
                vandstand=Vandstand(
                    **{"varsel": 2.5, "1.1": 3.69, "2": 4.09, "5": 5.34, "10": 6.5}
                ),
                station_id="88888888",
            )
            Create.file(conn, None, False, [kriterie1])
            Create.file(conn, None, False, [kriterie2])
            dateTime = datetime.datetime.now()
            date = dateTime.date()
            upload1 = Upload_get(id=1, Datetime=date, note=None, sommer=False)
            assert Get.upload(conn) == upload1
