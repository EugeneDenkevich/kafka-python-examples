"""
Facade Gateway

>>> python example_aiokafka/worker_facade.py
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


send_to_micro_before = broker.publisher(TopicsEnum.MICRO_BEFORE)
send_to_tg = broker.publisher(TopicsEnum.TG_SERVICE)


@send_to_micro_before
@broker.subscriber(TopicsEnum.BOT)
async def recieve_from_bot(message: Message) -> None:
    print(f"{Fore.YELLOW}Recieved in facade from bot: {Fore.BLUE}{message.value}{Fore.RESET}")

    return message


@send_to_tg
@broker.subscriber(TopicsEnum.MICRO_AFTER)
async def recieve_from_bot(message: Message) -> None:
    print(f"{Fore.YELLOW}Recieved in facade from micro: {Fore.BLUE}{message.value}{Fore.RESET}")

    return message


def get_app() -> FastStream:
    return FastStream(broker=broker).as_asgi(asyncapi_path="/docs")


def main() -> None:
    uvicorn.run(
        "example_aiokafka.worker_facade:get_app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        factory=True,
    )


if __name__ == "__main__":
    main()
