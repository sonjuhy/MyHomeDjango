import logging
logger = logging.getLogger(__name__)
import traceback
import time

import paho.mqtt.client as mqtt
import core.db.iot_database_connection as db_conn

from iot_messaging.MQTT import mqtt_json_parser
from iot_messaging.MQTT import publisher

from iot_messaging.kafka.kafka_producer import producer, get_kafka_data, kafka_topic, iot_to_spring_kafka_data

from core.db.database_enum import Default as dbDefaultEnum
from iot_messaging.MQTT.mqtt_enum import MQTTEnum as mqttEnum
from iot_messaging.MQTT.mqtt_enum import RoomEnum as roomEnum
from iot_messaging.MQTT.mqtt_enum import RoomStatusEnum as roomStatusEnum


from typing import Any

class Subscribe:

    def __init__(self) -> None:
        self.Room = {
            roomEnum.BALCONY_MAIN.value: roomStatusEnum.OFF.value,
            roomEnum.BALCONY_SUB.value: roomStatusEnum.OFF.value,
            roomEnum.BATH_ROOM_MAIN.value: roomStatusEnum.OFF.value,
            roomEnum.BATH_ROOM_SUB.value: roomStatusEnum.OFF.value,
            roomEnum.BIG_ROOM_TOP.value: roomStatusEnum.OFF.value,
            roomEnum.BIG_ROOM_BOTTOM.value: roomStatusEnum.OFF.value,
            roomEnum.KITCHEN_SINK.value: roomStatusEnum.OFF.value,
            roomEnum.KITCHEN_TABLE.value: roomStatusEnum.OFF.value,
            roomEnum.LIVING_ROOM_SUB.value: roomStatusEnum.OFF.value,
            roomEnum.LIVING_ROOM_TOP.value: roomStatusEnum.OFF.value,
            roomEnum.LIVING_ROOM_MIDDLE.value: roomStatusEnum.OFF.value,
            roomEnum.LIVING_ROOM_BOTTOM.value: roomStatusEnum.OFF.value,
            roomEnum.MIDDLE_ROOM_TOP.value: roomStatusEnum.OFF.value,
            roomEnum.MIDDLE_ROOM_BOTTOM.value: roomStatusEnum.OFF.value,
            roomEnum.SMALL_ROOM.value: roomStatusEnum.OFF.value
        }

        self.topic_to_server = mqttEnum.TOPIC_PUB_SERVER.value
        self.topic_from_switch = mqttEnum.TOPIC_SUB_SWITCH.value
        self.server_host = mqttEnum.SERVER_IP.value
        self.selected_topic = ''
        self.client = mqtt.Client()
        self.database_conn = db_conn

    def connection(self, topic: str) -> None:
        logger.info('connection : topic - {topic}, self to_server : {to_server}, from_switch - {from_switch}'
              .format(topic=topic, to_server=self.topic_to_server, from_switch=self.topic_from_switch))
        logger.info("MyHome/Light/Pub/Server" == mqttEnum.TOPIC_PUB_SERVER.value)
        if topic == 'server':
            self.selected_topic = self.topic_to_server
        else:
            self.selected_topic = self.topic_from_switch

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect_async(host=self.server_host, port=mqttEnum.SERVER_PORT.value)
        self.client.loop_start()

    def on_connect(self, client, user_data, flags, rc) -> None:
        logger.info(f'on_connect topic : ${self.selected_topic}')
        self.client.subscribe(self.selected_topic)

    def on_message(self, client: Any, user_data: Any, msg: Any) -> None:
        try:
            logger.info('on message : msg - {msg}'.format(msg=msg.payload.decode('utf-8')))
            if self.selected_topic == self.topic_to_server:  # payload from not switch
                payload = msg.payload.decode('utf-8')
                if payload == 'reserve':
                    # will delete part(for legacy service work)
                    pass
                else:
                    dic_from_payload = mqtt_json_parser.json_parser_from_else(msg=payload)
                    if dic_from_payload['sender'] == 'ServerReserveDjango':  # from reserve job
                        msg_to_switch = mqtt_json_parser.json_encode_to_switch(dic=dic_from_payload)
                    else:
                        msg_to_switch = payload
                    publisher.pub(topic=mqttEnum.TOPIC_PUB_DEFAULT.value + dic_from_payload['room'], msg=msg_to_switch)
                    kafka_msg = ('[on_message] selected == server topic : {topic}, msg : {msg}, time : {time}'
                                 .format(topic=self.selected_topic, msg=msg_to_switch, time=time.strftime('%Y-%m-%d %H:%M:%S')))
                    producer.send(topic=kafka_topic['iot'], value=get_kafka_data(result=True, service='iot', content=kafka_msg))

            else:  # msg from switch or server
                payload = msg.payload.decode('utf-8')
                msg_diction = mqtt_json_parser.json_parser_from_switch(msg=payload)

                if msg_diction['sender'] == 'Server':  # switch connection checking
                    if msg_diction['room'] in self.Room:
                        db_diction = {'message': msg_diction['message'], 'room': msg_diction['room'], 'status': roomStatusEnum.ON.value}
                        self.database_conn.main(mode=dbDefaultEnum.UPDATE_CONN_STATUS.value, data=db_diction)
                else:  # send msg to android
                    try:
                        self.database_conn.main(mode=dbDefaultEnum.SAVE_LIGHT_RECORD.value, data=msg_diction)
                        self.database_conn.main(mode=dbDefaultEnum.UPDATE_LIGHT.value, data=msg_diction)
                    except Exception as e:
                        kafka_msg = '[on_message] error : {error}, msg={msg}'.format(error=traceback.format_exc(),
                                                                                     msg=msg.payload.decode('utf-8'))
                        producer.send(topic=kafka_topic['iot'], value=get_kafka_data(False, 'iot', kafka_msg))

                    msg_to_android = mqtt_json_parser.json_encode_to_android(msg_diction)
                    publisher.pub(topic=mqttEnum.TOPIC_PUB_RESULT.value, msg=msg_to_android)

                    kafka_msg = '[on_message] from switch, to android topic : {topic}, msg : {msg}, time : {time}'.format(
                        topic=self.selected_topic, msg=msg_to_android, time=time.strftime('%Y-%m-%d %H:%M:%S'))
                    producer.send(topic=kafka_topic['iot'], value=get_kafka_data(True, 'iot', kafka_msg))

                    kafka_iot_spring_msg: iot_to_spring_kafka_data = {
                        'sender': msg_diction['sender'],
                        'room': msg_diction['room'],
                        'state': msg_diction['message']
                    }
                    logger.info(f'kafka iot spring msg : {kafka_iot_spring_msg}')
                    producer.send(topic=kafka_topic['iot_spring'],
                                  value=kafka_iot_spring_msg)
        except Exception as e:
            kafka_msg = '[on_message] error : {error}, msg={msg}'.format(error=traceback.format_exc(), msg=str(msg.payload))
            producer.send(topic=kafka_topic['iot'], value=get_kafka_data(False, 'iot', kafka_msg))

