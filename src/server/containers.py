"""Server containers."""
from dependency_injector import containers, providers

from src.server.storage.file_handlers import FileHandler
from src.server.storage.multipart_handlers import MutipartHandler


class Container(containers.DeclarativeContainer):
    """Manages server apps dependencies."""

    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.server.storage.api",
        ]
    )
    env = providers.Configuration()

    file_handler = providers.Factory(
        FileHandler,
        storage_dir=env.storage_dir,
    )

    multipart_handler = providers.Factory(
        MutipartHandler,
    )
