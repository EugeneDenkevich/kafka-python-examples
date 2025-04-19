"""
Telegram Service

>>> python example_aiokafka/worker_tg.py
"""

import asyncio
from typing import Any
from colorama import Fore

from example_aiokafka.common import (
    MessageBroker,
    MessageHandler,
    TopicsEnum,
    acquire_producer,
    acquire_consumer,
)


class TgMessageHandler(MessageHandler):
    async def handle(self, value: Any):
        async with acquire_producer() as p:
            print(
                f"{Fore.YELLOW}Recieved from facade: {Fore.CYAN}{value.decode()}{Fore.RESET}"
            )

            print(f"{Fore.YELLOW}Send to telegram...{Fore.RESET}")
            await asyncio.sleep(5)

            print(
                f"{Fore.YELLOW}Message was blocked: {Fore.RED}{value.decode()}{Fore.RESET}"
            )


async def main():
    try:
        print(f"{Fore.GREEN}PROGRAM STARTED{Fore.RESET}")

        broker = MessageBroker(
            handlers={
                TopicsEnum.TG_SERVICE: TgMessageHandler,
            },
        )

        async with acquire_consumer(topics=broker.get_topics()) as c:
            async for msg in c:
                await broker.process_message(topic=msg.topic, value=msg.value)
    finally:
        print(f"{Fore.MAGENTA}PROGRAMM FINISHED{Fore.RESET}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
