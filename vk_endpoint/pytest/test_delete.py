from app.services import Delete, Create
from vk_endpoint.app.model import Kriterie, Dkhype, Vandstand
import pytest


class TestClassDelete:
    def test_delete_no_varsling(self, conn):
        with pytest.raises(Exception):
            Delete.varsling(1, "02001038", conn)

    def test_delete_no_upload(self, conn):
        with pytest.raises(Exception):
            Delete.upload(1, conn)

    def test_delete_varsling(self, conn):
        kriterie1 = Kriterie(
            dkhype=Dkhype(**{"1.1": 4.0, "5": 8.7, "20": 13.7, "50": 18.1}),
            vandstand=Vandstand(
                **{"varsel": 1.5, "1.1": 1.69, "2": 2.09, "5": 2.34, "10": 2.5}
            ),
            station_id="02001038",
        )
        Create.file(conn, None, False, [kriterie1])
        result = Delete.varsling(1, "02001038", conn)
        assert result["deleted"] == "02001038"

    def test_delete_upload(self, conn):
        kriterie1 = Kriterie(
            dkhype=Dkhype(**{"1.1": 4.0, "5": 8.7, "20": 13.7, "50": 18.1}),
            vandstand=Vandstand(
                **{"varsel": 1.5, "1.1": 1.69, "2": 2.09, "5": 2.34, "10": 2.5}
            ),
            station_id="02001038",
        )
        Create.file(conn, None, False, [kriterie1])
        result = Delete.upload(1, conn)
        assert result["deleted"] == 1

    def test_delete_varsling_fail(self, conn):
        with pytest.raises(Exception):
            kriterie1 = Kriterie(
                dkhype=Dkhype(**{"1.1": 4.0, "5": 8.7, "20": 13.7, "50": 18.1}),
                vandstand=Vandstand(
                    **{"varsel": 1.5, "1.1": 1.69, "2": 2.09, "5": 2.34, "10": 2.5}
                ),
                station_id="02001038",
            )
            Create.file(conn, None, False, [kriterie1])
            result = Delete.varsling(1, "92001038", conn)
            assert result["deleted"] == "02001038"

    def test_delete_upload_fail(self, conn):
        with pytest.raises(Exception):
            kriterie1 = Kriterie(
                dkhype=Dkhype(**{"1.1": 4.0, "5": 8.7, "20": 13.7, "50": 18.1}),
                vandstand=Vandstand(
                    **{"varsel": 1.5, "1.1": 1.69, "2": 2.09, "5": 2.34, "10": 2.5}
                ),
                station_id="02001038",
            )
            Create.file(conn, None, False, [kriterie1])
            result = Delete.upload(2, conn)
            assert result["deleted"] == 2
