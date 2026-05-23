from enum import Enum


class MQTTEnum(Enum):
    SERVER_IP: str = "192.168.0.254"
    SERVER_PORT: int = 1883
    TOPIC_PUB_DEFAULT: str = "MyHome/Light/Pub/"
    TOPIC_PUB_SERVER: str = "MyHome/Light/Pub/Server"
    TOPIC_PUB_RESULT: str = "MyHome/Light/Result"
    TOPIC_SUB_SWITCH: str = "MyHome/Light/Sub/Server"


class RoomEnum(Enum):
    BALCONY_MAIN: str = "balcony main"
    BALCONY_SUB: str = "balcony sub"
    BATH_ROOM_MAIN: str = "bathRoom1"
    BATH_ROOM_SUB: str = "bathRoom2"
    BIG_ROOM_TOP: str = "big Room1"
    BIG_ROOM_BOTTOM: str = "big Room2"
    KITCHEN_SINK: str = "kitchen sink"
    KITCHEN_TABLE: str = "kitchen table"
    LIVING_ROOM_TOP: str = "living Room1"
    LIVING_ROOM_MIDDLE: str = "living Room2"
    LIVING_ROOM_BOTTOM: str = "living Room3"
    LIVING_ROOM_SUB: str = "living Room sub"
    MIDDLE_ROOM_TOP: str = "middle Room1"
    MIDDLE_ROOM_BOTTOM: str = "middle Room2"
    SMALL_ROOM: str = "small Room"


class RoomStatusEnum(Enum):
    ON: str = "On"
    OFF: str = "Off"
