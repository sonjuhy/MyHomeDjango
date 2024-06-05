import os

from django.apps import AppConfig
from django.conf import settings


class MyhomeConfig(AppConfig):
    name = 'MyHome'

    def ready(self):
        super().ready()
        if os.environ.get('RUN_main', None) != 'true':
            from .MQTT import subscribe
            from MyHome.kafka.kafka_enum import KafkaEnum as kafkaEnum
            from MyHome.kafka.kafka_consumer import run
            mqtt_android = subscribe.Subscribe()
            mqtt_android.connection(topic='server')

            mqtt_switch = subscribe.Subscribe()
            mqtt_switch.connection(topic='switch')

            run(topic=kafkaEnum.TOPIC_IOT.value)
            run(topic=kafkaEnum.TOPIC_CLOUD.value)
            run(topic=kafkaEnum.TOPIC_RESERVE.value)

            if settings.SCHEDULER_DEFAULT:
                from .schedule import operator
                operator.scheduler_start()
