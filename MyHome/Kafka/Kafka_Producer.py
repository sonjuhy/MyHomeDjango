from json import dumps
import traceback
from kafka import KafkaProducer


producer = KafkaProducer(
    acks=1,
    compression_type='gzip',
    bootstrap_servers=['192.168.0.254:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8')
)
kafka_data = {
    'id': 0,
    'type': True,
    'sender': 'Django',
    'service': 'service_name',
    'content': 'msg_content'
}
kafka_topic = {
    'cloud': 'cloud-log-topic',
    'cloud_check': 'cloud-check-log',
    'iot': 'iot-log-topic',
    'reserve': 'reserve-log-topic',
    'weather': 'weather-log-topic'
}


def get_kafka_data(result, service, content):
    kafka_data['type'] = result
    kafka_data['service'] = service
    kafka_data['content'] = content
    producer.send(topic=kafka_topic['reserve'], value=kafka_data)
    return kafka_data

# try:
#     data={'messages': 'test from django'}
#     response = producer.send('exam-topic', value=data).get()
#     producer.flush()
#     print(response)
# except:
#     traceback.print_exc()
# print('DONE')