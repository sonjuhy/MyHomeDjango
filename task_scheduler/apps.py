import os
from django.apps import AppConfig
from django.conf import settings


class TaskSchedulerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'task_scheduler'

    def ready(self) -> None:
        if os.environ.get('RUN_main', None) != 'true':
            if settings.SCHEDULER_DEFAULT:
                from task_scheduler.schedule import operator
                operator.scheduler_start()
