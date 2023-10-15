import time
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone

from MyHome.MQTT.publisher import pub


def job_refresh():
    print('job refresh')
    scheduler = BackgroundScheduler()
    scheduler.configure(timezone=timezone('Asia/Seoul'))

    from .lightDB import get_all_light_list, get_all_reserve_list
    reserve_list = get_all_reserve_list()  # get all reserve data
    light_list = get_all_light_list()  # get all light data

    for reserve in reserve_list:
        print('reserve name : ' + reserve.NAME_CHAR)
        reserve_room = reserve.ROOM_CHAR  # room name
        reserve_days = reserve.DAY_CHAR.split(',')  # split days
        reserve_time = reserve.TIME_CHAR  # time. type : 12:01
        reiteration = reserve.REITERATION_CHAR  # repeat every week. type : True or False
        activation = reserve.ACTIVATED_CHAR

        if reiteration == 'False':
            if activation == 'True':  # one time run & already activated
                continue
            elif activation == 'False':
                now_hour = time.localtime().tm_hour
                now_min = time.localtime().tm_min
                str_time = str(now_hour)+str(now_min)
                now_time = datetime.strptime(str_time, '%H%M')
                res_time = datetime.strptime(reserve_time, '%H:%M')
                if now_time > res_time:
                    continue
        if reiteration == 'True':
            today = time.localtime().tm_wday
            running_today = True
            for day in reserve_days:
                if today == day:
                    running_today = False
                    break
            if running_today:
                continue

        category = ''
        for light in light_list:
            if light.LIGHT_ROOM_PK == reserve_room:
                category = light.CATEGORY_CHAR
                break
        msg = set_msg(reserve.DO_CHAR, reserve_room, category)

        reserve_hour = reserve_time.split(':')[0]
        reserve_min = reserve_time.split(':')[1]
        scheduler.add_job(
            func=job_running,
            args=(msg, reserve),
            trigger=CronTrigger(hour=reserve_hour, minute=reserve_min),
            name=reserve.NAME_CHAR
        )
    scheduler.start()


def job_running(msg, reserve):
    topic = 'MyHome/Light/Pub/Server'
    pub(topic, msg)
    reserve_pk = reserve.LIGHT_RESERVE_PK
    activation = 'False'
    if reserve.ACTIVATED_CHAR == 'False':
        activation = 'True'

    from .lightDB import set_reserve_result
    set_reserve_result(pk=reserve_pk, activation=activation)


def job_clear(sche):
    sche.clear()


def set_msg(message, destination, room):
    # if change all refresh -> refresh some data, get data from kafka and make msg & return msg
    # msg sample : {"Light":{"sender":"Server","message":"OFF","destination":"living Room1","room":"living Room"}}
    tmp_dic = [('sender', 'ServerReserveDjango'), ('message', message), ('destination', destination), ('room', room)]
    from MyHome.MQTT.jsonParser import JSON_ENCODE_TOSERVER
    msg = JSON_ENCODE_TOSERVER(tmp_dic)
    print('set_msg : ' + msg)
    return msg
