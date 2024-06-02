from MyHome.models import RoomLight, Reserve, LightRecord
from datetime import datetime
from .DatabaseEnum import Default as modeEnum


def insert(time, room, do, day, user):
    LightRecord.objects.create(TIME_CHAR=time, ROOM_CHAR=room, USER_CHAR=user, DO_CHAR=do, DAY_CHAR=day)


def update(mode, condition, column, data):
    if mode == 'control':
        room = RoomLight.objects.get(LIGHT_ROOM_PK=condition)
        if column == 'State':
            room.STATE_CHAR = data
        elif column == 'Connect':
            room.STATE_CHAR = data['message']
            room.CONNECT_CHAR = data['status']
        room.save()
    elif mode == 'reserve':
        reserve = Reserve.objects.get(LIGHT_RESERVE_PK=condition)
        if column == 'Do':
            reserve.DO_CHAR = data
        elif column == 'Activated':
            reserve.ACTIVATED_CHAR = data
        reserve.save()


def select(table):
    if table == 'Reserve':
        return Reserve.objects.all()
    elif table == 'Room':
        return RoomLight.objects.all()


def main(mode, data):
    if mode == modeEnum.UPDATE_LIGHT:
        if data['message'] == 'On' or data['message'] == 'Off':
            update('control', data['room'], 'State', data['message'])
    elif mode == modeEnum.UPDATE_CONN_STATUS:
        update('control', data['room'], 'Connect', data)  # need to compare data content
    elif mode == modeEnum.GET_LIGHT_LIST:
        return select('Room')
    elif mode == modeEnum.SAVE_LIGHT_RECORD:
        now = datetime.now()
        date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
        hour = str(now.hour) + ':' + str(now.minute)
        insert(hour, data['room'], data['message'], date, data['sender'])
    elif mode == modeEnum.GET_RESERVE_LIST:
        return select('Reserve')
    elif mode == modeEnum.UPDATE_RESERVE:
        update('reserve', data[0][1], 'Do', data[1][1])
    elif mode == modeEnum.UPDATE_RESERVE_ACTIVATE:
        update('reserve', data[0][1], 'Activated', data[1][1])
