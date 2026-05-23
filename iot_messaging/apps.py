import os
from django.apps import AppConfig


class IotMessagingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'iot_messaging'

    def ready(self) -> None:
        if os.environ.get('RUN_main', None) != 'true':
            from iot_messaging.MQTT import subscribe
            from iot_messaging.kafka.kafka_enum import KafkaEnum as kafkaEnum
            from iot_messaging.kafka.kafka_consumer import run
            mqtt_android = subscribe.Subscribe()
            mqtt_android.connection(topic='server')

            mqtt_switch = subscribe.Subscribe()
            mqtt_switch.connection(topic='switch')

            run(topic=kafkaEnum.TOPIC_IOT.value)
            run(topic=kafkaEnum.TOPIC_CLOUD.value)
            run(topic=kafkaEnum.TOPIC_RESERVE.value)
