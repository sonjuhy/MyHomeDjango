import json
import threading
import traceback

from kafka import KafkaConsumer

from MyHome.File import fileJSON
from MyHome.File import fileMove
from MyHome.Kafka.lightReserve import job
from MyHome.MQTT import jsonParser
from MyHome.MQTT import publisher


class KafkaConsumerDefault:

    def run(self, topic):
        task = threading.Thread(target=self.listen, args=[topic])
        task.setDaemon(True)
        task.start()

    def listen(self, topic):
        print('Starting listening {}'.format(topic))
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=['192.168.0.254:9092'],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='django-kafka',
            # value_deserializer=lambda x: loads(x.decode('utf-8')),
            consumer_timeout_ms=1000
        )

        # sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
        # from MQTT import publisher
        # from MQTT import jsonParser

        while True:
            consumer.commit()
            for message in consumer:
                print(
                    "Topic: {}, Partition: {}, Offset: {}, Key: {}, Value: {}".format(message.topic, message.partition,
                                                                                      message.offset, message.key,
                                                                                      message.value.decode('utf-8')))
                value = message.value.decode('utf-8')
                if topic == 'iot-topic':
                    if json.loads(value):
                        parsing_data = jsonParser.JSON_Parser_android(value)
                        publisher.pub('MyHome/Light/Pub/' + parsing_data['room'], value)
                        print('parsing_data on Kafka: %s' % value)
                    else:
                        print('value is not JSON')
                elif topic == 'cloud-topic':
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
                elif topic == 'reserve-topic':
                    print('reserve topic refresh job schedule')
                    # from apscheduler.schedulers.background import BackgroundScheduler
                    # scheduler = BackgroundScheduler()
                    from MyHome.Schedule.MainScheduler import MainScheduler
                    main_scheduler = MainScheduler()
                    scheduler = main_scheduler.get_scheduler()
                    job.job_refresh(scheduler)


def kafka_cloud_producer(msg):
    from kafka import KafkaProducer
    from json import dumps

    producer = KafkaProducer(
        acks=1,
        compression_type='gzip',
        bootstrap_servers=['192.168.0.254:9092'],
        value_serializer=lambda x: dumps(x).encode('utf-8')
    )

    try:
        data = {'messages': msg}
        response = producer.send('cloud-topic', value=data).get()
        producer.flush()
        print(response)
    except:
        traceback.print_exc()
