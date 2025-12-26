from CRUD import Create
from model import Kriterie, Dkhype, Vandstand
import pytest


class TestClassCreate:
    def test_no_note(self, conn):
        kriterie1 = Kriterie(
            dkhype=Dkhype(**{"1.1": 4.0, "5": 8.7, "20": 13.7, "50": 18.1}),
            vandstand=Vandstand(
                **{"varsel": 1.5, "1.1": 1.69, "2": 2.09, "5": 2.34, "10": 2.5}
            ),
            station_id="02001038",
        )
        result = Create.file(conn, None, False, [kriterie1])
        assert result["rows_inserted"] == 1

    def test_note(self, conn):
        kriterie1 = Kriterie(
            dkhype=Dkhype(**{"1.1": 4.0, "5": 8.7, "20": 13.7, "50": 18.1}),
            vandstand=Vandstand(
                **{"varsel": 1.5, "1.1": 1.69, "2": 2.09, "5": 2.34, "10": 2.5}
            ),
            station_id="02001038",
        )
        result = Create.file(conn, "dfkojaspasjdpspojdpasdjpo", False, [kriterie1])
        assert result["rows_inserted"] == 1

    def test_null_values(self, conn):
        kriterie1 = Kriterie(
            dkhype=Dkhype(**{"1.1": None, "5": None, "20": None, "50": None}),
            vandstand=Vandstand(
                **{"varsel": None, "1.1": None, "2": None, "5": None, "10": None}
            ),
            station_id="02001038",
        )
        result = Create.file(conn, "dfkojaspasjdpspojdpasdjpo", False, [kriterie1])
        assert result["rows_inserted"] == 1

    def test_incomplete_dkhype(self, conn):
        with pytest.raises(Exception):
            kriterie1 = Kriterie(
                dkhype=Dkhype(**{"5": None, "20": None, "50": None}),
                vandstand=Vandstand(
                    **{"varsel": None, "1.1": None, "2": None, "5": None, "10": None}
                ),
                station_id="02001038",
            )
            Create.file(conn, "dfkojaspasjdpspojdpasdjpo", False, [kriterie1])

    def test_incomplete_vandstand(self, conn):
        with pytest.raises(Exception):
            kriterie1 = Kriterie(
                dkhype=Dkhype(**{"1.1": None, "5": None, "20": None, "50": None}),
                vandstand=Vandstand(**{"1.1": None, "2": None, "5": None, "10": None}),
                station_id="02001038",
            )
            result = Create.file(conn, "dfkojaspasjdpspojdpasdjpo", False, [kriterie1])
            assert result["rows_inserted"] == 1

    def test_stationid_7(self, conn):
        with pytest.raises(Exception):
            kriterie1 = Kriterie(
                dkhype=Dkhype(**{"1.1": 4.0, "5": 8.7, "20": 13.7, "50": 18.1}),
                vandstand=Vandstand(
                    **{"varsel": 1.5, "1.1": 1.69, "2": 2.09, "5": 2.34, "10": 2.5}
                ),
                station_id="2001038",
            )
            result = Create.file(conn, "dfkojaspasjdpspojdpasdjpo", False, [kriterie1])
            assert result["rows_inserted"] == 1

    def test_stationid_9(self, conn):
        with pytest.raises(Exception):
            kriterie1 = Kriterie(
                dkhype=Dkhype(**{"1.1": 4.0, "5": 8.7, "20": 13.7, "50": 18.1}),
                vandstand=Vandstand(
                    **{"varsel": 1.5, "1.1": 1.69, "2": 2.09, "5": 2.34, "10": 2.5}
                ),
                station_id="902001038",
            )
            result = Create.file(conn, "dfkojaspasjdpspojdpasdjpo", False, [kriterie1])
            assert result["rows_inserted"] == 1

    def test_bulk_insert(self, conn):
        kriterie1 = Kriterie(
            dkhype=Dkhype(**{"1.1": 4.0, "5": 8.7, "20": 13.7, "50": 18.1}),
            vandstand=Vandstand(
                **{"varsel": 1.5, "1.1": 1.69, "2": 2.09, "5": 2.34, "10": 2.5}
            ),
            station_id="02001038",
        )
        kriterie2 = Kriterie(
            dkhype=Dkhype(**{"1.1": 4.0, "5": 8.7, "20": 13.7, "50": 18.1}),
            vandstand=Vandstand(
                **{"varsel": 1.5, "1.1": 1.69, "2": 2.09, "5": 2.34, "10": 2.5}
            ),
            station_id="82001038",
        )
        kriterie3 = Kriterie(
            dkhype=Dkhype(**{"1.1": 4.0, "5": 8.7, "20": 13.7, "50": 18.1}),
            vandstand=Vandstand(
                **{"varsel": 1.5, "1.1": 1.69, "2": 2.09, "5": 2.34, "10": 2.5}
            ),
            station_id="92001038",
        )
        kriterielist = []
        kriterielist.append(kriterie1)
        kriterielist.append(kriterie2)
        kriterielist.append(kriterie3)
        result = Create.file(conn, "dfkojaspasjdpspojdpasdjpo", False, kriterielist)
        assert result["rows_inserted"] == 3

    def test_bulk_insert_same_id(self, conn):
        with pytest.raises(Exception):
            kriterie1 = Kriterie(
                dkhype=Dkhype(**{"1.1": 4.0, "5": 8.7, "20": 13.7, "50": 18.1}),
                vandstand=Vandstand(
                    **{"varsel": 1.5, "1.1": 1.69, "2": 2.09, "5": 2.34, "10": 2.5}
                ),
                station_id="02001038",
            )
            kriterielist = []
            kriterielist.append(kriterie1)
            kriterielist.append(kriterie1)
            kriterielist.append(kriterie1)
            Create.file(conn, "dfkojaspasjdpspojdpasdjpo", kriterielist)
