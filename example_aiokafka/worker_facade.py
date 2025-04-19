"""
Facade Gateway

>>> python example_aiokafka/worker_facade.py
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


class BotMessageHandler(MessageHandler):
    async def handle(self, value: Any):
        async with acquire_producer() as p:
            print(
                f"{Fore.YELLOW}Recieved from bot: {Fore.CYAN}{value.decode()}{Fore.RESET}"
            )

            await p.send_and_wait(topic=TopicsEnum.MICRO_BEFORE, value=value)


class MicroMessageHandler(MessageHandler):
    async def handle(self, value: Any):
        async with acquire_producer() as p:
            print(
                f"{Fore.YELLOW}Recieved from microservice: {Fore.CYAN}{value.decode()}{Fore.RESET}"
            )

            await p.send_and_wait(topic=TopicsEnum.TG_SERVICE, value=value)


async def main():
    try:
        print(f"{Fore.GREEN}PROGRAM STARTED{Fore.RESET}")

        broker = MessageBroker(
            handlers={
                TopicsEnum.BOT: BotMessageHandler,
                TopicsEnum.MICRO_AFTER: MicroMessageHandler,
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
