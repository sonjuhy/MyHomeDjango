from MyHome.models import Reserve, RoomLight


def get_all_reserve_list():
    reserve_list = Reserve.objects.all()
    return reserve_list


def set_reserve_result(pk, activation):
    Reserve.objects.update(ACTIVATED_CHAR=activation)


def get_all_light_list():
    light_list = RoomLight.objects.all()
    return light_list


def get_light_by_name(light):
    return RoomLight.objects.get(LIGHT_ROOM_PK=light)

