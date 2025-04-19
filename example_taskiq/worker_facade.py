"""
Facade Gateway

>>> taskiq worker example_aiokafka.worker_facade:broker
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


broker.configure_consumer(group_id="facade_gateway_group_id")


@broker.task(task_name=TopicsEnum.BOT)
async def recieved_message_from_bot(message: str) -> None:
    print(f"{Fore.YELLOW}Message: recieved from bot: {Fore.GREEN}{message}{Fore.RESET}")

    await send_message_to_microservice_service.kiq(message=message)


@broker.task(task_name=TopicsEnum.MICRO_AFTER)
async def recieved_message_from_microservice(message: str) -> None:
    print(
        f"{Fore.YELLOW}Message recieved from microcervice after moderation: {Fore.WHITE}{message}{Fore.RESET}"
    )

    await send_message_to_tg_service.kiq(message=message)


@broker.task(task_name=TopicsEnum.MICRO_BEFORE)
async def send_message_to_microservice_service(message: str) -> None:
    print(
        f"{Fore.YELLOW}Message sent to microservice: {Fore.BLUE}{message}{Fore.RESET}"
    )


@broker.task(task_name=TopicsEnum.TG_SERVICE)
async def send_message_to_tg_service(message: str) -> None:
    print(
        f"{Fore.YELLOW}Message sent to tg service: {Fore.MAGENTA}{message}{Fore.RESET}"
    )
