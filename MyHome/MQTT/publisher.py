import paho.mqtt.client as mqtt

import time
from MyHome.Kafka.Kafka_Producer import producer, get_kafka_data, kafka_topic


def pub(topic, msg):
    print('On Publisher topic : {topic}, msg : {msg}'.format(topic=topic, msg=msg))
    client = mqtt.Client('Django-mqtt')
    client.connect("192.168.0.254", 1883, 60)
    client.publish(topic, msg)

    if topic == 'MyHome/Light/Pub/Server':
        kafka_msg = '[pub] topic : {topic}, msg : {msg}, time : {time}'.format(topic=topic, msg=msg,
                                                                               time=time.strftime('%Y-%m-%d %H:%M:%S'))
        producer.send(topic=kafka_topic['iot'], value=get_kafka_data(True, 'iot', kafka_msg))

    client.loop(2)
