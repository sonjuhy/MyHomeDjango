import paho.mqtt.client as mqtt
from . import jsonParser
from . import publisher
import os, sys


class Subscribe:

    def __init__(self):
        self.Room = {'balcony main': 'Off', 'balcony sub': 'Off', 'bathRoom1': 'Off', 'bathRoom2': 'Off',
                     'big Room1': 'Off', 'big Room2': 'Off', 'kitchen sink': 'Off'
            , 'kitchen table': 'Off', 'living Room sub': 'Off', 'living Room1': 'Off',
                     'living Room2': 'Off', 'living Room3': 'Off', 'middle Room1': 'Off'
            , 'middle Room2': 'Off', 'small Room': 'Off'}

        self.topic_android = 'MyHome/Light/Pub/Server'
        self.topic_switch = 'MyHome/Light/Sub/Server'
        self.server_host = '192.168.0.254'
        self.selected_topic = ''
        self.client = mqtt.Client()

    def connection(self, topic):
        if topic == 'android':
            self.selected_topic = self.topic_android
        else:
            self.selected_topic = self.topic_switch

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect_async(self.server_host, 1883)
        self.client.loop_start()

    def on_connect(self, client, user_data, flags, rc):
        self.client.subscribe(self.selected_topic)

    def on_message(self, client, user_data, msg):
        print('topic : {}, msg : {}'.format(self.selected_topic, msg.payload.decode('utf-8')))
        if self.selected_topic == self.topic_android:
            payload = msg.payload.decode('utf-8')
            msg_to_switch = jsonParser.JSON_Parser_android(payload)
            # publisher.pub('MyHome/Light/Pub'+msgToSwitch['room'], msgToSwitch)
            print('msgToSwitch : {}'.format(msg_to_switch))
        else:
            payload = msg.payload.decode('utf-8')
            msg_diction = jsonParser.JSON_Parser(payload)

            if msg_diction['sender'] == 'Server':  # switch connection checking
                if msg_diction['room'] in self.Room:
                    self.Room[msg_diction['room']] = 'On'
                    if msg_diction['room'] == 'small Room':
                        for (room, status) in self.Room.items():
                            dbDiction = [('message', status), ('room', room)]
                            # TODO: connection to DB
                            # network.SQL_Def("Connect", dbDiction)
                            self.Room[room] = 'Off'
            else:
                sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
                import MyHome.dbConnection as db
                db_container = db.Connection()
                db_container.main('LightRecordInsert', msg_diction)
                db_container.main('LightUpdate', msg_diction)

                msg_to_android = jsonParser.JSON_ENCODE(msg_diction)
                # publisher().pub('MyHome/Light/Result', msgToAndroid)
                print('msgToAndroid : {}'.format(msg_to_android))
