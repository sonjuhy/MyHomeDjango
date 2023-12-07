from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore

class MainScheduler:
    _instance = None
    scheduler = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls.scheduler = BackgroundScheduler()
            cls.scheduler.add_jobstore(DjangoJobStore(), 'iot_reserve_job_store')
            cls._instance = super(MainScheduler, cls).__new__(cls)
        return cls._instance

    def get_scheduler(self):
        return self.scheduler

