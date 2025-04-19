"""
Microservice

>>> taskiq worker example_aiokafka.worker_micro:broker
"""

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


broker.configure_consumer(group_id="microservice_group_id")


@broker.task(task_name=TopicsEnum.MICRO_BEFORE)
async def recieved_message_from_facade_gateway(message: str) -> None:
    print(
        f"{Fore.YELLOW}Message: recieved from facade gateway before moderation: {Fore.BLUE}{message}{Fore.RESET}"
    )

    await send_message_to_gateway.kiq(message=message)


@broker.task(task_name=TopicsEnum.MICRO_AFTER)
async def send_message_to_gateway(message: str) -> None:
    print(
        f"{Fore.YELLOW}Message sent to facade gateway after moderation: {Fore.WHITE}{message}{Fore.RESET}"
    )
