"""
Bot

>>> python example_aiokafka/sender_bot.py
"""

import asyncio
from faststream.kafka import KafkaBroker
from pydantic import BaseModel

from example_aiokafka.common import KAFKA_HOST, TopicsEnum


broker = KafkaBroker(bootstrap_servers=KAFKA_HOST)


class Message(BaseModel):
    value: str


async def main() -> None:
    message = Message(value="message")
    topic = TopicsEnum.BOT

    await broker.connect()

    await broker.publish(message, topic)


if __name__ == "__main__":
    asyncio.run(main())
