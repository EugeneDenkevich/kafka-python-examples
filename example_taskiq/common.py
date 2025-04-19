from enum import StrEnum, auto

KAFKA_HOST = "localhost:9092"


class TopicsEnum(StrEnum):
    BOT = auto()
    MICRO_BEFORE = auto()
    MICRO_AFTER = auto()
    TG_SERVICE = auto()
