import pytest
from unittest.mock import patch, MagicMock

from MyHome.schedule.main_scheduler import MainScheduler
from MyHome.schedule.operator import scheduler_start

class TestSchedule:
    def test_main_scheduler_singleton(self):
        # We need to clear _instance in case it was created by other tests
        MainScheduler._instance = None
        s1 = MainScheduler()
        s2 = MainScheduler()
        assert s1 is s2
        assert s1.get_scheduler() is not None

    @patch('MyHome.schedule.operator.job.job_refresh')
    @patch('MyHome.schedule.main_scheduler.MainScheduler')
    def test_scheduler_start(self, mock_main_scheduler, mock_job_refresh):
        mock_instance = MagicMock()
        mock_scheduler = MagicMock()
        mock_scheduler.state = 0
        mock_instance.get_scheduler.return_value = mock_scheduler
        mock_main_scheduler.return_value = mock_instance

        scheduler_start()
        
        assert mock_scheduler.start.called
        assert mock_job_refresh.called
        assert mock_scheduler.scheduled_job.called
