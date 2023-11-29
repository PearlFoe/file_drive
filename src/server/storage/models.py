"""Model of api data for storage application."""
from pydantic import BaseModel


class FileMetadata(BaseModel):
    """File metadata model."""

    file_name: str



class DownloadRequest(BaseModel):
    """Download file request data model."""

    file_name: str
