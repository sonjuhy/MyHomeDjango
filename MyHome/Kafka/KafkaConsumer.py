import json
import threading
import traceback

from kafka import KafkaConsumer
from kafka import KafkaProducer

from MyHome.File import fileJSON
from MyHome.File import fileMove
from MyHome.Kafka.lightReserve import job
from MyHome.MQTT import jsonParser
from MyHome.MQTT import publisher
from json import dumps

from MyHome.DB.LightDatabase import set_reserve_result
from MyHome.MQTT.MqttEnum import MQTTEnum as mqttEnum
from .KafkaEnum import KafkaEnum as kafkaEnum


def listen(topic):
    print('Starting listening {topic}, server ip : {ip}'.format(topic=topic, ip=kafkaEnum.SERVER_IP.value))
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=[kafkaEnum.SERVER_IP.value],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='django-kafka',
        # value_deserializer=lambda x: loads(x.decode('utf-8')),
        consumer_timeout_ms=1000
    )

    while True:
        consumer.commit()
        for message in consumer:
            print(
                "Topic: {}, Partition: {}, Offset: {}, Key: {}, Value: {}".format(message.topic, message.partition,
                                                                                  message.offset, message.key,
                                                                                  message.value.decode('utf-8')))
            value = message.value.decode('utf-8')
            if topic == kafkaEnum.TOPIC_IOT.value:
                if json.loads(value):
                    parsing_data = jsonParser.json_parser_from_else(value)
                    publisher.pub(mqttEnum.TOPIC_PUB_DEFAULT.value + parsing_data['room'], value)
                    print('parsing_data on Kafka: %s' % value)
                else:
                    print('value is not JSON')
            elif topic == kafkaEnum.TOPIC_CLOUD.value:
                json_object = fileJSON.json_parsing(value)
                if json_object['purpose'] == 'move':
                    result = fileMove.file_move(uuid=json_object['uuid'], file=json_object['file'],
                                                path=json_object['path'], action=json_object['action'])
                elif json_object['purpose'] == 'delete':
                    result = fileMove.file_delete(uuid=json_object['uuid'], file=json_object['file'])
                else:
                    result = -1

                if result < 0:
                    result_msg = 'false'
                    if result == -1:
                        print('error : file error')
                    elif result == -2:
                        print('error : db connection error')
                else:
                    result_msg = 'success'
                # tmp_json = {'message': 'no', 'result': result_msg}
                # kafka_cloud_producer(fileJSON.json_encoding(result_msg))
            elif topic == kafkaEnum.TOPIC_RESERVE.value:
                print('reserve topic refresh job schedule')
                # from apscheduler.schedulers.background import BackgroundScheduler
                # scheduler = BackgroundScheduler()
                from MyHome.Schedule.MainScheduler import MainScheduler
                main_scheduler = MainScheduler()
                scheduler = main_scheduler.get_scheduler()
                job.job_refresh(scheduler)
            elif topic == kafkaEnum.TOPIC_RESERVE_UPDATE.value:
                json_object = jsonParser.json_parser_from_job(value)
                reserve_pk = json_object['pk']
                activation = json_object['activation']
                set_reserve_result(pk=reserve_pk, activation=activation)


def run(topic):
    task = threading.Thread(target=listen, args=[topic])
    task.setDaemon(True)
    task.start()


def kafka_cloud_producer(msg):

    producer = KafkaProducer(
        acks=1,
        compression_type='gzip',
        bootstrap_servers=[kafkaEnum.SERVER_IP.value],
        value_serializer=lambda x: dumps(x).encode('utf-8')
    )

    try:
        data = {'messages': msg}
        response = producer.send(kafkaEnum.TOPIC_CLOUD.value, value=data).get()
        producer.flush()
        print(response)
    except:
        traceback.print_exc()
