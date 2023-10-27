"""
Project settings container.

Parses .env file from the root of the project folder.
"""
from os import path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settigns(BaseSettings):
    """Parses variables from .env file."""

    _project_dir: str = path.join(path.dirname(path.realpath(__file__)), "..")

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        env_file=path.join(_project_dir, ".env")
    )

    storage_dir: str = path.join(_project_dir, "storage/")
