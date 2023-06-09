import asyncio
import logging
import os
from concurrent.futures.thread import ThreadPoolExecutor
from typing import cast

from dotenv import load_dotenv
from pydantic import BaseSettings
from starlite import Starlite, State, OpenAPIConfig, LoggingConfig, HTTPException

from src.exception.exception_handler import json_exception_handler
from src.controller.car_controller import CarController
from src.repository.db import MongoDatabaseConnection
from src.services.booking_service import BookingService
from src.services.car_service import CarService
from src.services.kafka_consumer import ConsumerTask

load_dotenv()


class AppSettings(BaseSettings):
    db_name = "car_service"
    mongo_hostname = os.getenv("MONGO_HOSTNAME")
    mongo_username = os.getenv("MONGO_USERNAME")
    mongo_password = os.getenv("MONGO_PASSWORD")
    kafka_servers = os.getenv("KAFKA_SERVERS")
    kafka_username = os.getenv("KAFKA_USERNAME")
    kafka_api_token = os.getenv("KAFKA_API_TOKEN")


settings = AppSettings()

log = logging.getLogger()
logging_config = LoggingConfig(
    loggers={
        "se_car_service": {
            "level": "INFO",
        }
    }
)


async def register_kafka_consumer(state: State) -> ConsumerTask:
    """Registers the kafka consumer."""
    if not getattr(state, "kafka_consumer", None):
        state.kafka_consumer = ConsumerTask(servers=settings.kafka_servers, username=settings.kafka_username,
                                            api_token=settings.kafka_api_token, topic_name="bookings")
    return cast("ConsumerTask", state.kafka_consumer)


async def get_db_connection(state: State) -> MongoDatabaseConnection:
    """Returns the db engine. """
    if not getattr(state, "db_connection", None):
        state.db_connection = MongoDatabaseConnection(db_name=settings.db_name, mongo_hostname=settings.mongo_hostname,
                                                      mongo_username=settings.mongo_username,
                                                      mongo_password=settings.mongo_password)
        log.info("Connecting to db")
    return cast("MongoDatabaseConnection", state.db_connection)


async def close_db_connection(state: State) -> None:
    """Closes the db connection stored in the application State object."""
    if getattr(state, "db_connection", None):
        log.info("Closing db connection")
        await cast("MongoDatabaseConnection", state.db_connection).close_connection()


async def define_car_service(state: State) -> CarService:
    """Returns the car service."""
    if not getattr(state, "car_service", None):
        state.car_service = CarService(state.db_connection, car_collection_name="cars",
                                       booking_collection_name="bookings")
    return cast("CarService", state.car_service)


async def define_booking_service(state: State) -> BookingService:
    """Returns the car service."""
    if not getattr(state, "booking_service", None):
        state.booking_service = BookingService(state.db_connection, collection_name="bookings")
        # Register the booking service to listen for kafka events
        state.kafka_consumer.add_event_handler(state.booking_service.handle_booking)
    return cast("BookingService", state.booking_service)


async def start_kafka_consumer(state: State) -> None:
    # handle kafka events
    if getattr(state, "kafka_consumer", None):
        # Kafka consumer is blocking, so we need to run it in a separate thread
        loop = asyncio.get_running_loop()
        executor = ThreadPoolExecutor(max_workers=1)
        loop.run_in_executor(executor, state.kafka_consumer.run)


async def stop_kafka_consumer(state: State) -> None:
    # handle kafka events
    if getattr(state, "kafka_consumer", None):
        await state.kafka_consumer.stop()


app = Starlite(route_handlers=[CarController],
               on_startup=[get_db_connection, define_car_service, register_kafka_consumer,
                           define_booking_service, start_kafka_consumer],
               on_shutdown=[stop_kafka_consumer, close_db_connection],
               exception_handlers={HTTPException: json_exception_handler},
               openapi_config=OpenAPIConfig(title="Car Service", version="1.0.0"),
               logging_config=logging_config)

log.info(f"Swagger : http://127.0.0.1:{os.getenv('PORT', 8000)}/schema/swagger")
