import asyncio
import os
import sys

from dotenv import load_dotenv

from example.kafka_producer import ProducerTask


async def run_tasks():
    load_dotenv()
    kafka_servers = os.getenv("KAFKA_SERVERS")
    kafka_username = os.getenv("KAFKA_USERNAME")
    kafka_api_token = os.getenv("KAFKA_API_TOKEN")

    driver_options = {
        'bootstrap.servers': kafka_servers,
        'security.protocol': 'SASL_SSL',
        'sasl.mechanisms': 'PLAIN',
        'sasl.username': kafka_username,
        'sasl.password': kafka_api_token,
        'api.version.request': True,
        'broker.version.fallback': '0.10.2.1',
        'log.connection.close': False,
    }

    producer_opts = {
        'client.id': 'kafka-python-console-sample-producer',
    }

    tasks = []

    producer = ProducerTask({**driver_options, **producer_opts}, "bookings")
    tasks.append(asyncio.ensure_future(producer.run()))

    done, pending = await asyncio.wait(tasks)
    for future in done | pending:
        future.result()
    sys.exit(0)


if __name__ == "__main__":
    asyncio.run(run_tasks())
