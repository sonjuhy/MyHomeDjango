import paho.mqtt.client as mqtt

def pub(topic, msg):
    client = mqtt.Client('Django-mqtt')
    client.connect("192.168.0.254", 1883, 60)
    client.publish(topic, msg)

    client.loop(2)