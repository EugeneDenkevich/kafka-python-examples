"""
Bot

>>> python example_aiokafka/sender_bot.py 'message'
"""

import sys
import asyncio
from colorama import Fore
from taskiq_aio_kafka import AioKafkaBroker
from kafka.admin import NewTopic

from example_aiokafka.common import KAFKA_HOST, TopicsEnum

broker = AioKafkaBroker(
    bootstrap_servers=KAFKA_HOST,
    kafka_topic=NewTopic(
        name="My-topic",
        num_partitions=1,
        replication_factor=1,
    ),
)


@broker.task(task_name=TopicsEnum.BOT)
async def send_message_to_facade_gateway(message: str) -> None:
    print(Fore.YELLOW, f"Message: sent {message}", Fore.RESET)

    return message


async def main(message: str) -> None:
    try:
        await broker.startup()

        await send_message_to_facade_gateway.kiq(message=message)
    finally:
        await broker.shutdown()


if __name__ == "__main__":
    asyncio.run(main(message=sys.argv[1]))
