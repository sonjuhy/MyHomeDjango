from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore

from MyHome.Kafka.lightReserve import job


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'iot_reserve_job_store')

    # @scheduler.scheduled_job('interval', seconds=50, name = 'expiry_check')
    @scheduler.scheduled_job('cron', hour=0, name='iot_reserve_check')
    def auto_check():
        job.job_refresh(scheduler)

    # scheduler.start()
    job.job_refresh(scheduler)
    print('operator scheduler start')

