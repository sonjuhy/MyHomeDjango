import pytest
from unittest.mock import patch, MagicMock
from MyHome.MQTT.subscribe import Subscribe
from MyHome.MQTT.mqtt_enum import MQTTEnum as mqttEnum
import json

class TestSubscribe:
    @patch('paho.mqtt.client.Client')
    def test_connection_server(self, mock_mqtt):
        sub = Subscribe()
        sub.connection('server')
        assert sub.selected_topic == mqttEnum.TOPIC_PUB_SERVER.value
        assert sub.client.connect_async.called
        assert sub.client.loop_start.called

    @patch('paho.mqtt.client.Client')
    def test_connection_switch(self, mock_mqtt):
        sub = Subscribe()
        sub.connection('switch')
        assert sub.selected_topic == mqttEnum.TOPIC_SUB_SWITCH.value
        assert sub.client.connect_async.called

    def test_on_connect(self):
        sub = Subscribe()
        sub.selected_topic = 'test_topic'
        sub.client = MagicMock()
        sub.on_connect(None, None, None, None)
        sub.client.subscribe.assert_called_with('test_topic')

    @patch('MyHome.MQTT.subscribe.producer.send')
    @patch('MyHome.MQTT.subscribe.publisher.pub')
    @patch('MyHome.MQTT.subscribe.db_conn.main')
    def test_on_message_server_topic(self, mock_db_main, mock_pub, mock_send):
        sub = Subscribe()
        sub.selected_topic = mqttEnum.TOPIC_PUB_SERVER.value
        mock_msg = MagicMock()
        mock_msg.payload.decode.return_value = json.dumps({
            "Light": {"sender": "ServerReserveDjango", "message": "On", "room": "room1", "destination": "room1"}
        })
        sub.on_message(None, None, mock_msg)
        assert mock_pub.called

    @patch('MyHome.MQTT.subscribe.producer.send')
    @patch('MyHome.MQTT.subscribe.publisher.pub')
    @patch('MyHome.MQTT.subscribe.db_conn.main')
    def test_on_message_switch_topic_server_sender(self, mock_db_main, mock_pub, mock_send):
        sub = Subscribe()
        sub.selected_topic = mqttEnum.TOPIC_SUB_SWITCH.value
        mock_msg = MagicMock()
        mock_msg.payload.decode.return_value = json.dumps({
            "sender": "Server", "message": "On", "room": "bathRoom1"
        })
        sub.on_message(None, None, mock_msg)
        assert mock_db_main.called

    @patch('MyHome.MQTT.subscribe.producer.send')
    @patch('MyHome.MQTT.subscribe.publisher.pub')
    @patch('MyHome.MQTT.subscribe.db_conn.main')
    def test_on_message_switch_topic_else_sender(self, mock_db_main, mock_pub, mock_send):
        sub = Subscribe()
        sub.selected_topic = mqttEnum.TOPIC_SUB_SWITCH.value
        mock_msg = MagicMock()
        mock_msg.payload.decode.return_value = json.dumps({
            "sender": "User", "message": "On", "room": "bathRoom1"
        })
        sub.on_message(None, None, mock_msg)
        assert mock_db_main.call_count == 2
        assert mock_pub.called

    @patch('MyHome.MQTT.subscribe.producer.send')
    def test_on_message_exception(self, mock_send):
        sub = Subscribe()
        sub.selected_topic = mqttEnum.TOPIC_PUB_SERVER.value
        mock_msg = MagicMock()
        mock_msg.payload.decode.side_effect = Exception("decode error")
        sub.on_message(None, None, mock_msg)
        assert mock_send.called
