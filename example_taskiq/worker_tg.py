"""
Telegram Service

>>> taskiq worker example_aiokafka.worker_tg:broker
"""

from asyncio import sleep
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


broker.configure_consumer(group_id="tg_service_group_id")


@broker.task(task_name=TopicsEnum.TG_SERVICE)
async def recieved_message_from_facade_gateway(message: str) -> None:
    print(
        f"{Fore.YELLOW}Message: recieved from facade gateway: {Fore.MAGENTA}{message}{Fore.RESET}"
    )

    print(f"{Fore.YELLOW}Send to telegram...{Fore.RESET}")
    await sleep(5)

    print(f"{Fore.YELLOW}Message was blocked: {Fore.RED}{message}{Fore.RESET}")
