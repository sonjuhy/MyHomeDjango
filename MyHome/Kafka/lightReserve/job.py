import time
from datetime import datetime

from apscheduler.triggers.cron import CronTrigger

from MyHome.MQTT.publisher import pub
from MyHome.Kafka.Kafka_Producer import producer, get_kafka_data, kafka_topic

day_to_num = {
    '월': 0,
    '화': 1,
    '수': 2,
    '목': 3,
    '금': 4,
    '토': 5,
    '일': 6
}


def job_refresh(scheduler):
    try:
        if len(scheduler.get_jobs()) > 0:
            job_clear(scheduler)

        reserve_job_list = get_reserves()
        reserve_str = ''
        if len(reserve_job_list) != 0:
            for reserve_job in reserve_job_list:
                scheduler.add_job(
                    id=reserve_job['id'],
                    func=job_running,
                    args=(reserve_job['msg'], reserve_job['reserve']),
                    trigger=CronTrigger(hour=reserve_job['hour'], minute=reserve_job['minute']),
                    name=reserve_job['name'],
                    jobstore='iot_reserve_job_store',
                    replace_existing=True
                )
                reserve_str += reserve_job['name'] + ' : ' + reserve_job['msg'] + ', time : ' + reserve_job[
                    'hour'] + '-' + reserve_job['minute'] + '\n'
        else:
            reserve_str = 'no data'
        kafka_msg = '[job_refresh] reserve size : {size}, data : {data}'.format(size=len(reserve_job_list),
                                                                                data=reserve_str)
        producer.send(topic=kafka_topic['reserve'], value=get_kafka_data(True, 'reserve', kafka_msg))
        # print(kafka_msg)
    except Exception as e:
        kafka_msg = '[job_refresh] error msg : {}'.format(e) + ', time : ' + time.strftime('%Y-%m-%d %H:%M:%S')
        producer.send(topic=kafka_topic['reserve'], value=get_kafka_data(False, 'reserve', kafka_msg))
        # print(kafka_msg)


def job_running(msg, reserve):
    try:
        topic = 'MyHome/Light/Pub/Server'
        pub(topic, msg)
        kafka_msg = '[job_running] send pub topic : ' + topic + ', msg : ' + msg + ', time : ' + time.strftime(
            '%Y-%m-%d %H:%M:%S')
        producer.send(topic=kafka_topic['reserve'], value=get_kafka_data(True, 'reserve', kafka_msg))

        reserve_pk = reserve.LIGHT_RESERVE_PK
        activation = 'False'
        if reserve.ACTIVATED_CHAR == 'False':
            activation = 'True'

        from .lightDB import set_reserve_result
        set_reserve_result(pk=reserve_pk, activation=activation)
    except Exception as e:
        kafka_msg = '[job_running] error msg : {}'.format(e) + ', time : ' + time.strftime('%Y-%m-%d %H:%M:%S')
        producer.send(topic=kafka_topic['reserve'], value=get_kafka_data(False, 'reserve', kafka_msg))


def job_clear(sche):
    sche.remove_all_jobs()


def get_reserves():
    from .lightDB import get_all_light_list, get_all_reserve_list
    reserve_list = get_all_reserve_list()  # get all reserve data
    light_list = get_all_light_list()  # get all light data

    reserve_job_list = []
    for reserve in reserve_list:
        reserve_id = reserve.LIGHT_RESERVE_PK
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
                str_time = str(now_hour) + str(now_min)
                now_time = datetime.strptime(str_time, '%H%M')
                res_time = datetime.strptime(reserve_time, '%H:%M')
                if now_time > res_time:
                    continue
        if reiteration == 'True':
            today = time.localtime().tm_wday
            running_today = True
            for day in reserve_days:
                if today == day_to_num[day]:
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
        reserve_job = {
            'id': str(reserve_id),
            'msg': msg,
            'reserve': reserve,
            'hour': reserve_hour,
            'minute': reserve_min,
            'name': reserve.NAME_CHAR
        }
        reserve_job_list.append(reserve_job)
    return reserve_job_list


def set_msg(message, destination, room):
    # if change all refresh -> refresh some data, get data from kafka and make msg & return msg
    # msg sample : {"Light":{"sender":"Server","message":"OFF","destination":"living Room1","room":"living Room"}}
    tmp_dic = [('sender', 'ServerReserveDjango'), ('message', message), ('destination', destination), ('room', room)]
    from MyHome.MQTT.jsonParser import JSON_ENCODE_TOSERVER
    msg = JSON_ENCODE_TOSERVER(tmp_dic)
    return msg
