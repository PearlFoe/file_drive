"""Model of api data for storage application."""
from pydantic import BaseModel


class DownloadDataRequest(BaseModel):
    """Download file request data model."""

    file_name: str
