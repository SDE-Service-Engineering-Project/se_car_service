import logging
from typing import cast

import uvicorn
from dotenv import dotenv_values
from pydantic import BaseSettings
from starlite import Starlite, State, OpenAPIConfig, LoggingConfig

from src.controller.car_controller import CarController
from src.repository.db import MongoDatabaseConnection
from src.services.car_service import CarService

config = dotenv_values(".env")


class AppSettings(BaseSettings):
    db_name = "car_service"
    mongo_hostname = config["MONGO_HOSTNAME"]
    mongo_username = config["MONGO_USERNAME"]
    mongo_password = config["MONGO_PASSWORD"]


settings = AppSettings()

logger = logging.getLogger()
logging_config = LoggingConfig(
    loggers={
        "my_app": {
            "level": "INFO",
        }
    }
)


def get_db_connection(state: State) -> MongoDatabaseConnection:
    """Returns the db engine. """
    if not getattr(state, "db_connection", None):
        state.db_connection = MongoDatabaseConnection(db_name=settings.db_name, mongo_hostname=settings.mongo_hostname,
                                                      mongo_username=settings.mongo_username,
                                                      mongo_password=settings.mongo_password)
    return cast("MongoDatabaseConnection", state.db_connection)


async def close_db_connection(state: State) -> None:
    """Closes the db connection stored in the application State object."""
    if getattr(state, "engine", None):
        await cast("MongoDatabaseConnection", state.engine).close_connection()


async def define_car_service(state: State) -> CarService:
    """Returns the car service."""
    if not getattr(state, "car_service", None):
        state.car_service = CarService(state.db_connection)
    return cast("CarService", state.car_service)


app = Starlite(route_handlers=[CarController], on_startup=[get_db_connection, define_car_service],
               on_shutdown=[close_db_connection], openapi_config=OpenAPIConfig(title="Car Service", version="1.0.0"),
               logging_config=logging_config)

if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 8000
    logger.info(f"Swagger : http://{ip}:{port}/schema/swagger")
    uvicorn.run(app, host=ip, port=port)
