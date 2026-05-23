import pytest
from unittest.mock import patch, MagicMock
from core.models import RoomLight, Reserve, LightRecord
from core.db.database_enum import Default as modeEnum
from core.db.iot_database_connection import db_insert, db_update, db_select, main

@pytest.mark.django_db
class TestIotDatabaseConnection:
    def test_db_insert(self):
        db_insert("12:00", "room1", "On", "2023-10-01", "user1")
        record = LightRecord.objects.get(ROOM_CHAR="room1")
        assert record.DO_CHAR == "On"
        assert record.USER_CHAR == "user1"

    def test_db_update_control_state(self):
        RoomLight.objects.create(LIGHT_ROOM_PK="room1", STATE_CHAR="Off")
        db_update("control", "room1", "State", ["On"])
        assert RoomLight.objects.get(LIGHT_ROOM_PK="room1").STATE_CHAR == "On"

    def test_db_update_control_connect(self):
        RoomLight.objects.create(LIGHT_ROOM_PK="room2", STATE_CHAR="Off", CONNECT_CHAR="dis")
        db_update("control", "room2", "Connect", ["On", "connected"])
        room = RoomLight.objects.get(LIGHT_ROOM_PK="room2")
        assert room.STATE_CHAR == "On"
        assert room.CONNECT_CHAR == "connected"

    def test_db_update_reserve_do(self):
        reserve = Reserve.objects.create(NAME_CHAR="r1", DO_CHAR="Off")
        db_update("reserve", reserve.LIGHT_RESERVE_PK, "Do", ["On"])
        assert Reserve.objects.get(LIGHT_RESERVE_PK=reserve.LIGHT_RESERVE_PK).DO_CHAR == "On"

    def test_db_update_reserve_activated(self):
        reserve = Reserve.objects.create(NAME_CHAR="r2", ACTIVATED_CHAR="False")
        db_update("reserve", reserve.LIGHT_RESERVE_PK, "Activated", ["True"])
        assert Reserve.objects.get(LIGHT_RESERVE_PK=reserve.LIGHT_RESERVE_PK).ACTIVATED_CHAR == "True"

    def test_db_select(self):
        Reserve.objects.create(NAME_CHAR="res")
        RoomLight.objects.create(LIGHT_ROOM_PK="room")
        assert db_select("Reserve").count() == 1
        assert db_select("Room").count() == 1
        assert db_select("Unknown").count() == 0

    def test_main_update_light(self):
        RoomLight.objects.create(LIGHT_ROOM_PK="room1", STATE_CHAR="Off")
        main(modeEnum.UPDATE_LIGHT.value, {"room": "room1", "message": "On"})
        assert RoomLight.objects.get(LIGHT_ROOM_PK="room1").STATE_CHAR == "On"
        main(modeEnum.UPDATE_LIGHT.value, {"room": "room1", "message": "Invalid"})

    def test_main_update_conn_status(self):
        RoomLight.objects.create(LIGHT_ROOM_PK="room1", STATE_CHAR="Off", CONNECT_CHAR="dis")
        main(modeEnum.UPDATE_CONN_STATUS.value, {"room": "room1", "message": "On", "status": "conn"})
        room = RoomLight.objects.get(LIGHT_ROOM_PK="room1")
        assert room.CONNECT_CHAR == "conn"

    def test_main_get_light_list(self):
        RoomLight.objects.create(LIGHT_ROOM_PK="room1", STATE_CHAR="Off")
        res = main(modeEnum.GET_LIGHT_LIST.value, None)
        assert res.count() == 1

    @patch("core.db.iot_database_connection.datetime")
    def test_main_save_light_record(self, mock_dt):
        mock_now = MagicMock()
        mock_now.year = 2023
        mock_now.month = 10
        mock_now.day = 1
        mock_now.hour = 12
        mock_now.minute = 30
        mock_dt.now.return_value = mock_now
        
        main(modeEnum.SAVE_LIGHT_RECORD.value, {"room": "room1", "message": "On", "sender": "user1"})
        rec = LightRecord.objects.get(ROOM_CHAR="room1")
        assert rec.TIME_CHAR == "12:30"
        assert rec.DAY_CHAR == "2023-10-1"

    def test_main_get_reserve_list(self):
        Reserve.objects.create(NAME_CHAR="r1")
        res = main(modeEnum.GET_RESERVE_LIST.value, None)
        assert res.count() == 1

    def test_main_update_reserve(self):
        reserve = Reserve.objects.create(NAME_CHAR="r1", DO_CHAR="Off")
        data = [["pk", reserve.LIGHT_RESERVE_PK], ["Do", "On"]]
        main(modeEnum.UPDATE_RESERVE.value, data)
        assert Reserve.objects.get(LIGHT_RESERVE_PK=reserve.LIGHT_RESERVE_PK).DO_CHAR == "On"

    def test_main_update_reserve_activate(self):
        reserve = Reserve.objects.create(NAME_CHAR="r1", ACTIVATED_CHAR="False")
        data = [["pk", reserve.LIGHT_RESERVE_PK], ["Activated", "True"]]
        main(modeEnum.UPDATE_RESERVE_ACTIVATE.value, data)
        assert Reserve.objects.get(LIGHT_RESERVE_PK=reserve.LIGHT_RESERVE_PK).ACTIVATED_CHAR == "True"

    def test_main_default(self):
        res = main("unknown_mode", {})
        assert res is None
