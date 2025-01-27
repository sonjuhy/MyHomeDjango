from MyHome.models import Reserve, RoomLight

from channels.db import database_sync_to_async


# @database_sync_to_async
def get_all_reserve_list() -> list:
    reserve_list = list(Reserve.objects.all())
    return reserve_list


# @database_sync_to_async
def set_reserve_result(pk, activation):
    Reserve.objects.update(ACTIVATED_CHAR=activation)


# @database_sync_to_async
def get_all_light_list():
    light_list = RoomLight.objects.all()
    return light_list


# @database_sync_to_async
def get_light_by_name(light):
    return RoomLight.objects.get(LIGHT_ROOM_PK=light)


def get_all_reserve_list_sync() -> list:
    reserve_list = list(Reserve.objects.all())
    return reserve_list


def get_light_by_name_sync(light):
    return RoomLight.objects.get(LIGHT_ROOM_PK=light)

