from django.db import connection
from MyHome.models import RoomLight, Reserve, LightRecord
from datetime import datetime


class Connection:
    def main(self, mode, data):
        if mode == 'LightUpdate':
            if data['message'] == 'On' or data['message'] == 'Off':
                self.update('control', data['room'], 'State', data['message'])
        elif mode == 'ConnectUpdate':
            self.update('control', data['room'], 'Connect', data)  # need to compare data content
        elif mode == 'LightList':
            return self.select('Room')
        elif mode == 'LightRecordInsert':
            now = datetime.now()
            date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
            hour = str(now.hour) + ':' + str(now.minute)
            self.insert(hour, data['room'], data['message'], date, data['sender'])
        elif mode == 'ReserveList':
            return self.select('Reserve')
        elif mode == 'ReserveUpdate':
            self.update('reserve', data[0][1], 'Do', data[1][1])
        elif mode == 'ReserveActivateUpdate':
            self.update('reserve', data[0][1], 'Activated', data[1][1])

    def insert(self, time, room, do, day, user):
        LightRecord.objects.create(TIME_CHAR=time, ROOM_CHAR=room, USER_CHAR=user, DO_CHAR=do, DAY_CHAR=day)

    def update(self, mode, condition, column, data):
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

    def select(self, table):
        if table == 'Reserve':
            return Reserve.objects.all()
        elif table == 'Room':
            return RoomLight.objects.all()
