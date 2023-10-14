from MyHome.models import Reserve, RoomLight


def get_all_reserve_list():
    reserve_list = Reserve.objects.all()
    return reserve_list


def get_all_light_list():
    light_list = RoomLight.objects.all()
    return light_list

