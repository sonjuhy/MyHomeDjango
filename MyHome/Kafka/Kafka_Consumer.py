from json import loads
from time import sleep
from kafka import KafkaConsumer


consumer = KafkaConsumer(
    'exam-topic',
    bootstrap_servers=['192.168.0.254:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='django-kafka',
    # value_deserializer=lambda x: loads(x.decode('utf-8')),
    consumer_timeout_ms=1000
)

def listen():
    print('Starting Consumer')

    while True:
        message = consumer.poll()
        if len(message) != 0:
            print("consumer")
            for topic, recodes in message.items():
                for recode in recodes:
                    print("recode :{}".format(recode.value))
            consumer.commit()