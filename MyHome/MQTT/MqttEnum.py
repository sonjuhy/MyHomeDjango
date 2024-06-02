from enum import Enum


class MQTTEnum(Enum):
    SERVER_IP: str = "192.168.0.254"
    SERVER_PORT: int = 1883
    TOPIC_PUB_DEFAULT: str = "MyHome/Light/Pub/"
    TOPIC_PUB_SERVER: str = "MyHome/Light/Pub/Server"
    TOPIC_PUB_RESULT: str = "MyHome/Light/Result"
    TOPIC_SUB_SWITCH: str = "MyHome/Light/Sub/Server"
