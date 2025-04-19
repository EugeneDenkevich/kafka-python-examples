"""
Bot

>>> python example_aiokafka/sender_bot.py 'message'
"""

import asyncio
import sys
from typing import Any
from colorama import Fore

from example_aiokafka.common import (
    MessageBroker,
    MessageHandler,
    TopicsEnum,
    acquire_producer,
)


class BotMessageHandler(MessageHandler):
    async def handle(self, value: Any):
        async with acquire_producer() as p:
            await p.send_and_wait(topic=TopicsEnum.BOT, value=value)

            print(
                f"{Fore.YELLOW}Sent to facade gateway: {Fore.CYAN}{value.decode()}{Fore.RESET}"
            )


async def main():
    try:
        if len(sys.argv) < 2:
            print(f"{Fore.RED}Input something after script running{Fore.RESET}")

            exit()

        value = sys.argv[1].encode()

        broker = MessageBroker(
            handlers={
                TopicsEnum.BOT: BotMessageHandler,
            },
        )

        await broker.process_message(
            topic=TopicsEnum.BOT,
            value=value,
        )
    finally:
        print("Program finished")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
