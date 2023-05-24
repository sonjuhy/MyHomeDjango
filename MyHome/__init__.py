from .MQTT import subscribe
from .Kafka.Kafka_Consumer import Kafka_Consumer_default

mqttAndroid = subscribe.Subscribe()
mqttAndroid.connection(topic='android')

mqttSwitch = subscribe.Subscribe()
mqttSwitch.connection(topic='switch')

Kafka_Consumer_default().run('exam-topic')