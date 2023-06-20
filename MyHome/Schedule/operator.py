import traceback
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)

    @scheduler.scheduled_job('cron', hour=23, name='cloud_check')
    # @scheduler.scheduled_job('interval', seconds=50, name = 'expiry_check')
    def auto_check():
        kafka_cloud_producer()

    scheduler.start()


def kafka_cloud_producer():
    from kafka import KafkaProducer
    from json import dumps

    producer = KafkaProducer(
        acks=1,
        compression_type='gzip',
        bootstrap_servers=['192.168.0.254:9092'],
        value_serializer=lambda x: dumps(x).encode('utf-8')
    )

    try:
        data = {'messages': 'check'}
        response = producer.send('cloud-topic', value=data).get()
        producer.flush()
        print(response)
    except:
        traceback.print_exc()
