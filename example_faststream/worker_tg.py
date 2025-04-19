"""
Telegram Service

>>> python example_aiokafka/worker_tg.py
"""

from asyncio import sleep
from colorama import Fore
from faststream import FastStream
from faststream.kafka import KafkaBroker
from pydantic import BaseModel
import uvicorn

from example_aiokafka.common import KAFKA_HOST, TopicsEnum


broker = KafkaBroker(bootstrap_servers=KAFKA_HOST)


class Message(BaseModel):
    value: str


@broker.subscriber(TopicsEnum.TG_SERVICE)
async def recieve_from_facade(message: Message) -> None:
    print(f"{Fore.YELLOW}Recieved in tg from facade: {Fore.BLUE}{message.value}{Fore.RESET}")
    
    print(f"{Fore.YELLOW}Send to telegram...{Fore.RESET}")
    await sleep(5)

    print(f"{Fore.YELLOW}Message was blocked: {Fore.RED}{message.value}{Fore.RESET}")


def get_app() -> FastStream:
    return FastStream(broker=broker).as_asgi(asyncapi_path="/docs")


def main() -> None:
    uvicorn.run(
        "example_aiokafka.worker_tg:get_app",
        host="0.0.0.0",
        port=8002,
        reload=True,
        factory=True,
    )


if __name__ == "__main__":
    main()
