import paho.mqtt.client as mqtt

import time
from .mqtt_enum import MQTTEnum as mqttEnum
from MyHome.kafka.kafka_producer import producer, get_kafka_data, kafka_topic


def pub(topic: str, msg: any) -> None:
    print('On Publisher topic : {topic}, msg : {msg}'.format(topic=topic, msg=msg))
    client = mqtt.Client('Django-mqtt')
    client.connect(host=mqttEnum.SERVER_IP.value, port=mqttEnum.SERVER_PORT.value, keepalive=60)
    client.publish(topic, msg)

    if topic == mqttEnum.TOPIC_PUB_SERVER.value:
        kafka_msg = '[pub] topic : {topic}, msg : {msg}, time : {time}'.format(topic=topic, msg=msg,
                                                                               time=time.strftime('%Y-%m-%d %H:%M:%S'))
        producer.send(topic=kafka_topic['iot'], value=get_kafka_data(True, 'iot', kafka_msg))

    client.loop(2)
