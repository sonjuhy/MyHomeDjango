import os

from django.apps import AppConfig
from django.conf import settings


class MyhomeConfig(AppConfig):
    # default_auto_field = 'django.db.models.BigAutoField'
    name = 'MyHome'

    def ready(self):
        super().ready()
        if os.environ.get('RUN_main', None) != 'true':
            from .MQTT import subscribe
            from MyHome.Kafka.KafkaEnum import KafkaEnum as kafkaEnum
            from MyHome.Kafka.KafkaConsumer import run
            mqtt_android = subscribe.Subscribe()
            mqtt_android.connection(topic='server')

            mqtt_switch = subscribe.Subscribe()
            mqtt_switch.connection(topic='switch')

            # Kafka_Consumer_default().run('iot-topic')
            # iot_kafka = KafkaConsumerDefault()
            run(topic=kafkaEnum.TOPIC_IOT.value)

            # cloud_kafka = KafkaConsumerDefault()
            run(topic=kafkaEnum.TOPIC_CLOUD.value)

            # reserve_kafka = KafkaConsumerDefault()
            run(topic=kafkaEnum.TOPIC_RESERVE.value)

            if settings.SCHEDULER_DEFAULT:
                from .Schedule import operator
                operator.start()
