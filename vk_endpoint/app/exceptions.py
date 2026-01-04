"""Brugerdefinerede exceptions til applikationen."""

class DuplicateStationIdError(Exception):
    """Rejses når et station_id forekommer mere end én gang."""

class VarslingNotFoundError(Exception):
    """Rejses når en varsling ikke kan findes til opdatering."""

class UploadNotFoundError(Exception):
    """Rejses når en upload ikke kan findes til opdatering."""
