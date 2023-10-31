from aiohttp.web import Application

from . import storage


def get_app() -> Application:
    """
    Create app funcion.

    :return Application: Main server subapp. Aggregates all the project's subapps.
    """
    app = Application()
    app.add_subapp(prefix="/storage", subapp=storage.get_app())

    return app
