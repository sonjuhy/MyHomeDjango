import pytest
import os
from unittest.mock import patch, MagicMock
from task_scheduler.apps import TaskSchedulerConfig

class TestTaskSchedulerApps:
    @patch('task_scheduler.apps.os.environ.get')
    @patch('task_scheduler.schedule.operator.scheduler_start')
    def test_ready(self, mock_scheduler, mock_env_get):
        mock_env_get.return_value = 'not_true'
        import task_scheduler
        app_config = TaskSchedulerConfig('task_scheduler', task_scheduler)
        app_config.ready()
        assert mock_scheduler.called
