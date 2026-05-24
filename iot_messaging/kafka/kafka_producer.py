from typing import Dict, Any
from json import dumps
from kafka import KafkaProducer
from iot_messaging.kafka.kafka_enum import KafkaEnum as kafkaEnum

producer = KafkaProducer(
    acks=1,
    compression_type='gzip',
    bootstrap_servers=[kafkaEnum.SERVER_IP.value],
    value_serializer=lambda x: dumps(x).encode('utf-8')
)

kafka_data = {
    'id': 0,
    'type': True,
    'sender': 'Django',
    'service': 'service_name',
    'content': 'msg_content'
}
iot_to_spring_kafka_data = {
    'sender': 'sender',
    'room': 'room_name',
    'state': True

}

kafka_topic = {
    'cloud': kafkaEnum.TOPIC_LOG_CLOUD.value,
    'cloud_check': kafkaEnum.TOPIC_LOG_CLOUD_CHECK.value,
    'iot': kafkaEnum.TOPIC_LOG_IOT.value,
    'iot_spring': kafkaEnum.TOPIC_SPRING_IOT.value,
    'reserve': kafkaEnum.TOPIC_LOG_RESERVE.value,
    'weather': kafkaEnum.TOPIC_LOG_WEATHER.value
}


def get_kafka_data(result: bool, service: str, content: str) -> Dict[str, Any]:
    kafka_data['type'] = result
    kafka_data['service'] = service
    kafka_data['content'] = content
    return kafka_data
