from enum import Enum


class KafkaEnum(Enum):
    TOPIC_IOT = "iot-topic"
    TOPIC_CLOUD = "cloud-topic"
    TOPIC_RESERVE = "reserve-topic"
    TOPIC_RESERVE_UPDATE = "reserve-update"
    TOPIC_LOG_IOT = "iot-log-topic"
    TOPIC_LOG_CLOUD = "cloud-log-topic"
    TOPIC_LOG_CLOUD_CHECK = "cloud-check-log"
    TOPIC_LOG_RESERVE = "reserve-log-topic"
    TOPIC_LOG_WEATHER = "weather-log-topic"
    SERVER_IP = "192.168.0.254:9092"
