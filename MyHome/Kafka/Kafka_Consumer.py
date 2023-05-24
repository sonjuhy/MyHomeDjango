import threading
from threading import Thread

from kafka import KafkaConsumer

class Kafka_Consumer_default:

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
        while True:
            consumer.commit()
            for message in consumer:
                print("Topic: {}, Partition: {}, Offset: {}, Key: {}, Value: {}".format( message.topic, message.partition, message.offset, message.key, message.value.decode('utf-8')))
