from MyHome.models import Reserve, RoomLight


def get_all_reserve_list():
    reserve_list = Reserve.objects.all()
    return reserve_list


def set_reserve_result(pk, activation):
    Reserve.objects.filter(LIGHT_RESERVE_PK=pk).update(ACTIVATED_CHAR=activation)


def get_all_light_list():
    light_list = RoomLight.objects.all()
    return light_list
