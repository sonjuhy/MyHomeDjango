import json
import threading
import traceback

from MyHome.MQTT import jsonParser
from MyHome.MQTT import publisher
from MyHome.File import fileJSON
from MyHome.File import fileMove

from kafka import KafkaConsumer


class KafkaConsumerDefault:

    def run(self, topic):
        task = threading.Thread(target=self.listen, args=[topic])
        task.setDaemon(True)
        task.start()

    def listen(self, topic):
        print('Starting listening')
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
                        result = fileMove.file_move(json_object['uuid'], json_object['file'], json_object['path'])
                    elif json_object['purpose'] == 'delete':
                        result = fileMove.file_delete(json_object['uuid'], json_object['file'])
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

