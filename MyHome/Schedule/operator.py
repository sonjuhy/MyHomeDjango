from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore

from MyHome.Kafka.lightReserve import job


def start():
    # scheduler = BackgroundScheduler()
    from .MainScheduler import MainScheduler
    main_scheduler = MainScheduler()
    scheduler = main_scheduler.get_scheduler()
    # scheduler.add_jobstore(DjangoJobStore(), 'iot_reserve_job_store')

    # @scheduler.scheduled_job('interval', seconds=50, name = 'expiry_check')
    @scheduler.scheduled_job('cron', hour=0, name='iot_reserve_check')
    def auto_check():
        job.job_refresh(scheduler)
        if scheduler.state == 0:
            scheduler.start()

    # scheduler.start()
    job.job_refresh(scheduler)
    if scheduler.state == 0:
        print('scheduler start')
        scheduler.start()
    print('operator scheduler start')

