from typing import List
from MyHome.models import Reserve, RoomLight
from django.db.models.query import QuerySet

# @database_sync_to_async
def get_all_reserve_list() -> List[Reserve]:
    reserve_list = list(Reserve.objects.all())
    return reserve_list


# @database_sync_to_async
def set_reserve_result(pk: int, activation: str) -> None:
    # Note: Currently this updates all rows regardless of pk. 
    # Left as is to preserve existing behavior.
    Reserve.objects.filter(LIGHT_RESERVE_PK=pk).update(ACTIVATED_CHAR=activation)


# @database_sync_to_async
def get_all_light_list() -> QuerySet[RoomLight]:
    light_list = RoomLight.objects.all()
    return light_list


# @database_sync_to_async
def get_light_by_name(light: str) -> RoomLight:
    return RoomLight.objects.get(LIGHT_ROOM_PK=light)


def get_all_reserve_list_sync() -> List[Reserve]:
    reserve_list = list(Reserve.objects.all())
    return reserve_list


def get_light_by_name_sync(light: str) -> RoomLight:
    return RoomLight.objects.get(LIGHT_ROOM_PK=light)
