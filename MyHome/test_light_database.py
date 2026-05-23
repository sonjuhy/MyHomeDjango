import pytest
from MyHome.models import Reserve, RoomLight
from MyHome.db.light_database import (
    get_all_reserve_list,
    set_reserve_result,
    get_all_light_list,
    get_light_by_name,
    get_all_reserve_list_sync,
    get_light_by_name_sync
)

@pytest.mark.django_db
class TestLightDatabase:
    def test_get_all_reserve_list(self):
        Reserve.objects.create(NAME_CHAR="test1")
        Reserve.objects.create(NAME_CHAR="test2")
        result = get_all_reserve_list()
        assert len(result) == 2
        assert result[0].NAME_CHAR == "test1"

    def test_get_all_reserve_list_sync(self):
        Reserve.objects.create(NAME_CHAR="test3")
        result = get_all_reserve_list_sync()
        assert len(result) == 1
        assert result[0].NAME_CHAR == "test3"

    def test_set_reserve_result(self):
        reserve = Reserve.objects.create(NAME_CHAR="test", ACTIVATED_CHAR="False")
        set_reserve_result(reserve.LIGHT_RESERVE_PK, "True")
        fetched = Reserve.objects.get(LIGHT_RESERVE_PK=reserve.LIGHT_RESERVE_PK)
        assert fetched.ACTIVATED_CHAR == "True"

    def test_get_all_light_list(self):
        RoomLight.objects.create(LIGHT_ROOM_PK="L1", STATE_CHAR="On")
        result = get_all_light_list()
        assert result.count() == 1
        assert result.first().STATE_CHAR == "On"

    def test_get_light_by_name(self):
        RoomLight.objects.create(LIGHT_ROOM_PK="L2", STATE_CHAR="Off")
        result = get_light_by_name("L2")
        assert result.LIGHT_ROOM_PK == "L2"
        assert result.STATE_CHAR == "Off"

    def test_get_light_by_name_sync(self):
        RoomLight.objects.create(LIGHT_ROOM_PK="L3", STATE_CHAR="On")
        result = get_light_by_name_sync("L3")
        assert result.LIGHT_ROOM_PK == "L3"
        assert result.STATE_CHAR == "On"
