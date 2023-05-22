from .MQTT import subscribe

mqttAndroid = subscribe.Subscribe()
mqttAndroid.connection(topic='android')

mqttSwitch = subscribe.Subscribe()
mqttSwitch.connection(topic='switch')
