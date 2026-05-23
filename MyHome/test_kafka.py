import pytest
import json
from unittest.mock import patch, MagicMock

from MyHome.kafka.kafka_producer import get_kafka_data
from MyHome.kafka.kafka_consumer import listen, run, kafka_cloud_producer
from MyHome.kafka.kafka_enum import KafkaEnum as kafkaEnum
from MyHome.kafka.light_reserve import job
from MyHome.models import Reserve, RoomLight


class TestKafkaProducer:
    def test_get_kafka_data(self):
        res = get_kafka_data(True, 'test_service', 'test_content')
        assert res['type'] is True
        assert res['service'] == 'test_service'
        assert res['content'] == 'test_content'


@pytest.mark.django_db
class TestKafkaConsumer:
    @patch('MyHome.kafka.kafka_consumer.KafkaConsumer')
    @patch('MyHome.kafka.kafka_consumer.publisher.pub')
    def test_listen_iot_topic(self, mock_pub, mock_consumer):
        # mock message
        mock_msg = MagicMock()
        mock_msg.topic = kafkaEnum.TOPIC_IOT.value
        mock_msg.value.decode.return_value = json.dumps({"Light": {"sender": "s", "message": "m", "room": "r", "destination": "d"}})
        
        # mock consumer iteration
        mock_instance = MagicMock()
        mock_instance.__iter__.return_value = [mock_msg]
        mock_consumer.return_value = mock_instance

        # Because `listen` runs `while True`, we have to raise an Exception to break out after one loop or mock `while True` logic.
        # Actually `listen` has `while True:` -> `for message in consumer:`
        # We can break the loop by having the consumer iterator raise StopIteration? No, `for` catches it, then loops again.
        # So let's mock consumer.commit to raise an exception after first call to break the `while True` loop.
        mock_instance.commit.side_effect = [None, StopIteration("Stop Loop")]

        try:
            listen(kafkaEnum.TOPIC_IOT.value)
        except StopIteration:
            pass

        assert mock_pub.called

    @patch('MyHome.kafka.kafka_consumer.KafkaConsumer')
    @patch('MyHome.file.file_move.file_move')
    def test_listen_cloud_topic_move(self, mock_file_move, mock_consumer):
        mock_msg = MagicMock()
        mock_msg.topic = kafkaEnum.TOPIC_CLOUD.value
        mock_msg.value.decode.return_value = json.dumps({"purpose": "move", "uuid": "u", "file": "f", "path": "p", "action": "a"})
        
        mock_instance = MagicMock()
        mock_instance.__iter__.return_value = [mock_msg]
        mock_consumer.return_value = mock_instance
        mock_instance.commit.side_effect = [None, StopIteration("Stop Loop")]
        
        mock_file_move.return_value = 0

        try:
            listen(kafkaEnum.TOPIC_CLOUD.value)
        except StopIteration:
            pass

        assert mock_file_move.called

    @patch('MyHome.kafka.kafka_consumer.KafkaConsumer')
    @patch('MyHome.file.file_move.file_delete')
    def test_listen_cloud_topic_delete(self, mock_file_delete, mock_consumer):
        mock_msg = MagicMock()
        mock_msg.topic = kafkaEnum.TOPIC_CLOUD.value
        mock_msg.value.decode.return_value = json.dumps({"purpose": "delete", "uuid": "u", "file": "f", "path": "p", "action": "a"})
        
        mock_instance = MagicMock()
        mock_instance.__iter__.return_value = [mock_msg]
        mock_consumer.return_value = mock_instance
        mock_instance.commit.side_effect = [None, StopIteration("Stop Loop")]
        
        mock_file_delete.return_value = -1

        try:
            listen(kafkaEnum.TOPIC_CLOUD.value)
        except StopIteration:
            pass

        assert mock_file_delete.called

    @patch('MyHome.kafka.kafka_consumer.KafkaConsumer')
    @patch('MyHome.schedule.main_scheduler.MainScheduler')
    @patch('MyHome.kafka.light_reserve.job.job_refresh')
    def test_listen_reserve_topic(self, mock_job_refresh, mock_main_scheduler, mock_consumer):
        mock_msg = MagicMock()
        mock_msg.topic = kafkaEnum.TOPIC_RESERVE.value
        mock_msg.value.decode.return_value = "dummy"
        
        mock_instance = MagicMock()
        mock_instance.__iter__.return_value = [mock_msg]
        mock_consumer.return_value = mock_instance
        mock_instance.commit.side_effect = [None, StopIteration("Stop Loop")]

        try:
            listen(kafkaEnum.TOPIC_RESERVE.value)
        except StopIteration:
            pass

        assert mock_main_scheduler.called
        assert mock_job_refresh.called

    @patch('MyHome.kafka.kafka_consumer.KafkaConsumer')
    @patch('MyHome.kafka.kafka_consumer.set_reserve_result')
    def test_listen_reserve_update_topic(self, mock_set_reserve, mock_consumer):
        mock_msg = MagicMock()
        mock_msg.topic = kafkaEnum.TOPIC_RESERVE_UPDATE.value
        mock_msg.value.decode.return_value = json.dumps({"pk": 1, "activation": "True"})
        
        mock_instance = MagicMock()
        mock_instance.__iter__.return_value = [mock_msg]
        mock_consumer.return_value = mock_instance
        mock_instance.commit.side_effect = [None, StopIteration("Stop Loop")]

        try:
            listen(kafkaEnum.TOPIC_RESERVE_UPDATE.value)
        except StopIteration:
            pass

        mock_set_reserve.assert_called_with(pk=1, activation="True")

    @patch('threading.Thread')
    def test_run(self, mock_thread):
        mock_instance = MagicMock()
        mock_thread.return_value = mock_instance
        run('test_topic')
        assert mock_thread.called
        assert mock_instance.start.called

    @patch('MyHome.kafka.kafka_consumer.KafkaProducer')
    def test_kafka_cloud_producer(self, mock_producer):
        mock_instance = MagicMock()
        mock_producer.return_value = mock_instance
        kafka_cloud_producer("test_msg")
        assert mock_instance.send.called
        assert mock_instance.flush.called


@pytest.mark.django_db
class TestLightReserveJob:
    @patch('MyHome.kafka.light_reserve.job.producer.send')
    def test_job_refresh(self, mock_send):
        mock_scheduler = MagicMock()
        mock_scheduler.get_jobs.return_value = [MagicMock(id='job1')]
        
        # We need mock data for get_reserves
        RoomLight.objects.create(LIGHT_ROOM_PK="room1", CATEGORY_CHAR="cat1")
        Reserve.objects.create(LIGHT_RESERVE_PK=1, ROOM_CHAR="room1", TIME_CHAR="23:59", REITERATION_CHAR="False", ACTIVATED_CHAR="False", DAY_CHAR="No data", HOLIDAY_TINYINT=0, DO_CHAR="On", NAME_CHAR="res1")
        
        # mock pytimekr
        with patch('pytimekr.pytimekr.holidays', return_value=[]):
            job.job_refresh(mock_scheduler)
        
        assert mock_scheduler.remove_job.called
        assert mock_scheduler.add_job.called
        assert mock_send.called

    @patch('MyHome.kafka.light_reserve.job.producer.send')
    @patch('MyHome.kafka.light_reserve.job.pub')
    def test_job_running(self, mock_pub, mock_send):
        reserve_mock = MagicMock()
        reserve_mock.LIGHT_RESERVE_PK = 1
        reserve_mock.ACTIVATED_CHAR = 'False'
        
        job.job_running('test_msg', reserve_mock)
        assert mock_pub.called
        assert mock_send.call_count == 2  # one for log, one for update
