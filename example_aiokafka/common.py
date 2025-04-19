from abc import ABC, abstractmethod
from enum import StrEnum, auto
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Dict, List, Type

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

KAFKA_HOST = "localhost:9092"


class TopicsEnum(StrEnum):
    BOT = auto()
    MICRO_BEFORE = auto()
    MICRO_AFTER = auto()
    TG_SERVICE = auto()


class MessageHandler(ABC):
    @abstractmethod
    async def handle(self, value: Any) -> None: ...


type Handlers = Dict[TopicsEnum, Type[MessageHandler]]


class MessageBroker:
    def __init__(self, handlers: Handlers) -> None:
        self.handlers = handlers

    async def process_message(self, topic: TopicsEnum, value: Any) -> None:
        if handler := self.handlers.get(topic):
            await handler().handle(value=value)

    def get_topics(self) -> None:
        return list(self.handlers.keys())


@asynccontextmanager
async def acquire_producer() -> AsyncIterator[AIOKafkaProducer]:
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_HOST)

    await producer.start()

    try:
        yield producer
    finally:
        await producer.stop()


@asynccontextmanager
async def acquire_consumer(topics: List[TopicsEnum]) -> AsyncIterator[AIOKafkaConsumer]:
    consumer = AIOKafkaConsumer(*topics, bootstrap_servers=KAFKA_HOST)

    await consumer.start()

    try:
        yield consumer
    finally:
        await consumer.stop()
