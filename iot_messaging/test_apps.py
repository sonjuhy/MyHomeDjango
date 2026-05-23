import pytest
import os
from unittest.mock import patch, MagicMock
from iot_messaging.apps import IotMessagingConfig

class TestIotMessagingApps:
    @patch('iot_messaging.apps.os.environ.get')
    @patch('iot_messaging.MQTT.subscribe.Subscribe')
    @patch('iot_messaging.kafka.kafka_consumer.run')
    def test_ready(self, mock_run, mock_subscribe, mock_env_get):
        mock_env_get.return_value = 'not_true'
        import iot_messaging
        app_config = IotMessagingConfig('iot_messaging', iot_messaging)
        app_config.ready()
        assert mock_subscribe.called
        assert mock_run.called
