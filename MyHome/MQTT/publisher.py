import paho.mqtt.client as mqtt

import time
from .MqttEnum import MQTTEnum as mqttEnum
from MyHome.Kafka.KafkaProducer import producer, get_kafka_data, kafka_topic


def pub(topic, msg):
    print('On Publisher topic : {topic}, msg : {msg}'.format(topic=topic, msg=msg))
    client = mqtt.Client('Django-mqtt')
    client.connect(host=mqttEnum.SERVER_IP, port=mqttEnum.SERVER_PORT, keepalive=60)
    client.publish(topic, msg)

    if topic == mqttEnum.TOPIC_PUB_SERVER:
        kafka_msg = '[pub] topic : {topic}, msg : {msg}, time : {time}'.format(topic=topic, msg=msg,
                                                                               time=time.strftime('%Y-%m-%d %H:%M:%S'))
        producer.send(topic=kafka_topic['iot'], value=get_kafka_data(True, 'iot', kafka_msg))

    client.loop(2)
