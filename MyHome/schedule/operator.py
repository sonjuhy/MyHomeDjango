from MyHome.kafka.light_reserve import job


def scheduler_start():
    from .main_scheduler import MainScheduler
    main_scheduler = MainScheduler()
    scheduler = main_scheduler.get_scheduler()

    # @scheduler.scheduled_job('interval', seconds=5, name='expiry_check')
    @scheduler.scheduled_job('cron', hour=0, name='iot_reserve_check', id='iot_reserve_check')
    def auto_check():
        job.job_refresh(scheduler)
        if scheduler.state == 0:
            scheduler.start()

    if scheduler.state == 0:
        scheduler.start()
        job.job_refresh(scheduler)

