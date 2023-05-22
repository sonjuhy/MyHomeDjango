from json import dumps
import traceback
from kafka import KafkaProducer


producer = KafkaProducer(
    acks=1,
    compression_type='gzip',
    bootstrap_servers=['192.168.0.254:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8')
)

# try:
#     data={'messages': 'test from django'}
#     response = producer.send('exam-topic', value=data).get()
#     producer.flush()
#     print(response)
# except:
#     traceback.print_exc()
# print('DONE')