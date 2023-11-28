from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore

from MyHome.Kafka.lightReserve import job


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)

    @scheduler.scheduled_job('cron', hour=0, name='cloud_reserve_check')
    # @scheduler.scheduled_job('interval', seconds=50, name = 'expiry_check')
    def auto_check():
        job.job_refresh()

    scheduler.start()

