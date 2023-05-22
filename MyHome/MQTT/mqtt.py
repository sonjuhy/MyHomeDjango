import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    client.subscribe("MyHome/Light/Pub/Server")

def on_message(client, userdata, msg):
    # Do something
    print('topic : {}, payload : {}'.format(msg.topic, msg.payload))
    pass

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.254", 1883, 60)