from .MQTT import subscribe
from .Kafka.Kafka_Consumer import KafkaConsumerDefault

mqttAndroid = subscribe.Subscribe()
mqttAndroid.connection(topic='android')

mqttSwitch = subscribe.Subscribe()
mqttSwitch.connection(topic='switch')

# Kafka_Consumer_default().run('iot-topic')
iot_kafka = KafkaConsumerDefault()
iot_kafka.run('iot-topic')

cloud_kafka = KafkaConsumerDefault()
cloud_kafka.run('cloud-topic')
