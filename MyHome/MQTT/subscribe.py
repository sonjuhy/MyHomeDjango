import traceback

import paho.mqtt.client as mqtt
from . import jsonParser
from . import publisher

from .MqttEnum import MQTTEnum as mqttEnum
import time

from MyHome.Kafka.KafkaProducer import producer, get_kafka_data, kafka_topic
from ..DB.DatabaseEnum import Default as dbDefaultEnum
import MyHome.DB.DatabaseConnection as dbConn


class Subscribe:

    def __init__(self):
        self.Room = {'balcony main': 'Off', 'balcony sub': 'Off', 'bathRoom1': 'Off', 'bathRoom2': 'Off',
                     'big Room1': 'Off', 'big Room2': 'Off', 'kitchen sink': 'Off'
            , 'kitchen table': 'Off', 'living Room sub': 'Off', 'living Room1': 'Off',
                     'living Room2': 'Off', 'living Room3': 'Off', 'middle Room1': 'Off'
            , 'middle Room2': 'Off', 'small Room': 'Off'}

        self.topic_to_server = mqttEnum.TOPIC_PUB_SERVER.value
        self.topic_from_switch = mqttEnum.TOPIC_SUB_SWITCH.value
        self.server_host = mqttEnum.SERVER_IP.value
        self.selected_topic = ''
        self.client = mqtt.Client()
        self.database_conn = dbConn

    def connection(self, topic):
        if topic == 'server':
            self.selected_topic = self.topic_to_server
        else:
            self.selected_topic = self.topic_from_switch

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect_async(host=self.server_host, port=mqttEnum.SERVER_PORT.value)
        self.client.loop_start()

    def on_connect(self, client, user_data, flags, rc):
        self.client.subscribe(self.selected_topic)

    def on_message(self, client, user_data, msg):
        # print('topic : {}, msg : {}'.format(self.selected_topic, msg.payload.decode('utf-8')))
        try:
            if self.selected_topic == self.topic_to_server:  # payload from not switch
                payload = msg.payload.decode('utf-8')
                if payload == 'reserve':
                    # will delete part(for legacy service work)
                    pass
                else:
                    dic_from_payload = jsonParser.json_parser_from_else(payload)
                    if dic_from_payload['sender'] == 'ServerReserveDjango':  # from reserve job
                        msg_to_switch = jsonParser.json_encode_to_switch(dic_from_payload)
                    else:
                        msg_to_switch = payload
                    publisher.pub(mqttEnum.TOPIC_PUB_DEFAULT.value + dic_from_payload['room'], msg_to_switch)

                    print('msgToSwitch : {}'.format(msg_to_switch))
                    kafka_msg = '[on_message] selected == server topic : {topic}, msg : {msg}, time : {time}'.format(topic=self.selected_topic, msg=msg_to_switch, time=time.strftime('%Y-%m-%d %H:%M:%S'))
                    producer.send(topic=kafka_topic['iot'], value=get_kafka_data(True, 'iot', kafka_msg))
            else:  # msg from switch or server
                payload = msg.payload.decode('utf-8')
                msg_diction = jsonParser.json_parser_from_switch(payload)

                if msg_diction['sender'] == 'Server':  # switch connection checking
                    if msg_diction['room'] in self.Room:
                        db_diction = {'message': msg_diction['message'], 'room': msg_diction['room'], 'status': 'On'}
                        self.database_conn.main(dbDefaultEnum.UPDATE_CONN_STATUS.value, db_diction)
                else:  # send msg to android
                    self.database_conn.main(dbDefaultEnum.SAVE_LIGHT_RECORD.value, msg_diction)
                    self.database_conn.main(dbDefaultEnum.UPDATE_LIGHT.value, msg_diction)

                    msg_to_android = jsonParser.json_encode_to_android(msg_diction)
                    publisher.pub(mqttEnum.TOPIC_PUB_RESULT.value, msg_to_android)

                    print('msgToAndroid : {}'.format(msg_to_android))
                    kafka_msg = '[on_message] from switch, to android topic : {topic}, msg : {msg}, time : {time}'.format(
                        topic=self.selected_topic, msg=msg_to_android, time=time.strftime('%Y-%m-%d %H:%M:%S'))
                    producer.send(topic=kafka_topic['iot'], value=get_kafka_data(True, 'iot', kafka_msg))

        except Exception as e:
            kafka_msg = '[on_message] error : {error}, msg={msg}'.format(error=traceback.format_exc(), msg=msg.payload.decode('utf-8'))
            producer.send(topic=kafka_topic['iot'], value=get_kafka_data(False, 'iot', kafka_msg))
