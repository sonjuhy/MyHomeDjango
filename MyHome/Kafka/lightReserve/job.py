import time
import datetime

from MyHome.MQTT.publisher import pub


def job_refresh(sche):
    print('job refresh')
    job_clear(sche)  # clear job schedule before exist
    from .lightDB import get_all_light_list, get_all_reserve_list
    reserve_list = get_all_reserve_list()  # get all reserve data
    light_list = get_all_light_list()  # get all light data

    for reserve in reserve_list:
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
                now_time = datetime.timedelta(hours=now_hour, minutes=now_min)
                res_time = datetime.timedelta(hours=reserve_time.splt(':')[0], minutes=reserve_time.splt(':')[1])
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
                break

        category = ''
        for light in light_list:
            if light.LIGHT_ROOM_PK == reserve_room:
                category = light.CATEGORY_CHAR
                break
        msg = set_msg(reserve.DO_CHAR, reserve_room, category)

        sche.every().day.at(reserve_time).do(pub, msg)
        sche.run_pending()


def job_clear(sche):
    sche.clear()


def set_msg(message, destination, room):
    # if change all refresh -> refresh some data, get data from kafka and make msg & return msg
    # msg sample : {"Light":{"sender":"Server","message":"OFF","destination":"living Room1","room":"living Room"}}
    tmp_dic = [('sender', 'ServerReserve'), ('message', message), ('destination', destination), ('room', room)]
    from MyHome.MQTT.jsonParser import JSON_ENCODE_TOSERVER
    msg = JSON_ENCODE_TOSERVER(tmp_dic)
    print('set_msg : ' + msg)
    return msg
