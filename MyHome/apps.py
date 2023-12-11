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
            from .Kafka.Kafka_Consumer import KafkaConsumerDefault
            mqtt_android = subscribe.Subscribe()
            mqtt_android.connection(topic='server')

            mqtt_switch = subscribe.Subscribe()
            mqtt_switch.connection(topic='switch')

            # Kafka_Consumer_default().run('iot-topic')
            iot_kafka = KafkaConsumerDefault()
            iot_kafka.run('iot-topic')

            cloud_kafka = KafkaConsumerDefault()
            cloud_kafka.run('cloud-topic')

            reserve_kafka = KafkaConsumerDefault()
            reserve_kafka.run('reserve-topic')

            if settings.SCHEDULER_DEFAULT:
                from .Schedule import operator
                operator.start()
