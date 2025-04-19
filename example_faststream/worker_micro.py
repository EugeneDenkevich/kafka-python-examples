"""
Microservice

>>> python example_aiokafka/worker_micro.py
"""

from colorama import Fore
from faststream import FastStream
from faststream.kafka import KafkaBroker
from pydantic import BaseModel
import uvicorn

from example_aiokafka.common import KAFKA_HOST, TopicsEnum


broker = KafkaBroker(bootstrap_servers=KAFKA_HOST)


class Message(BaseModel):
    value: str


send_to_facade = broker.publisher(TopicsEnum.MICRO_AFTER)


@send_to_facade
@broker.subscriber(TopicsEnum.MICRO_BEFORE)
async def recieve_from_facade(message: Message) -> None:
    print(f"{Fore.YELLOW}Recieved in micro from facade: {Fore.BLUE}{message.value}{Fore.RESET}")

    return message


def get_app() -> FastStream:
    return FastStream(broker=broker).as_asgi(asyncapi_path="/docs")


def main() -> None:
    uvicorn.run(
        "example_aiokafka.worker_micro:get_app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        factory=True,
    )


if __name__ == "__main__":
    main()
