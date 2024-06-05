from MyHome.models import RoomLight, Reserve, LightRecord
from datetime import datetime
from .database_enum import Default as modeEnum


def db_insert(time: str, room: str, do: str, day: str, user: str) -> None:
    LightRecord.objects.create(TIME_CHAR=time, ROOM_CHAR=room, USER_CHAR=user, DO_CHAR=do, DAY_CHAR=day)


def db_update(mode: str, condition: str, column: str, data: list) -> None:
    if mode == 'control':
        room = RoomLight.objects.get(LIGHT_ROOM_PK=condition)
        if column == 'State':
            room.STATE_CHAR = data
        elif column == 'Connect':
            room.STATE_CHAR = data[0]  # message
            room.CONNECT_CHAR = data[1]  # status
        room.save()
    elif mode == 'reserve':
        reserve = Reserve.objects.get(LIGHT_RESERVE_PK=condition)
        if column == 'Do':
            reserve.DO_CHAR = data
        elif column == 'Activated':
            reserve.ACTIVATED_CHAR = data
        reserve.save()


def db_select(table: str) -> any:
    if table == 'Reserve':
        return Reserve.objects.all()
    elif table == 'Room':
        return RoomLight.objects.all()


def main(mode: str, data: dict):
    if mode == modeEnum.UPDATE_LIGHT.value:
        if data['message'] == 'On' or data['message'] == 'Off':
            db_update(mode='control', condition=data['room'], column='State', data=[data['message']])
    elif mode == modeEnum.UPDATE_CONN_STATUS.value:
        data_list = [data['message'], data['status']]
        db_update(mode='control', condition=data['room'], column='Connect', data=data_list)  # need to compare data content
    elif mode == modeEnum.GET_LIGHT_LIST.value:
        return db_select(table='Room')
    elif mode == modeEnum.SAVE_LIGHT_RECORD.value:
        now = datetime.now()
        date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
        hour = str(now.hour) + ':' + str(now.minute)
        db_insert(time=hour, room=data['room'], do=data['message'], day=date, user=data['sender'])
    elif mode == modeEnum.GET_RESERVE_LIST.value:
        return db_select(table='Reserve')
    elif mode == modeEnum.UPDATE_RESERVE.value:
        db_update(mode='reserve', condition=data[0][1], column='Do', data=[data[1][1]])
    elif mode == modeEnum.UPDATE_RESERVE_ACTIVATE.value:
        db_update(mode='reserve', condition=data[0][1], column='Activated', data=[data[1][1]])
