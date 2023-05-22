from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .job import schedule_api, kafka_producer

def start():
    print("Starting scheduler")
    scheduler = BackgroundScheduler()
    # scheduler.add_job(schedule_api, 'cron', second=10)
    scheduler.add_job(kafka_producer, 'interval', seconds=10)
    scheduler.start()