import pytest
from MyHome.models import RoomLight, Reserve, LightRecord, FileDefaultPathTb, FilePrivate, FilePrivateTrashTb, FilePublic, FilePublicTrashTb

@pytest.mark.django_db
class TestMyHomeModels:
    def test_room_light_crud(self):
        # Create
        light = RoomLight.objects.create(
            LIGHT_ROOM_PK="room1_light1",
            STATE_CHAR="On",
            ROOMKOR_CHAR="거실",
            CATEGORY_CHAR="메인조명",
            CONNECT_CHAR="connected"
        )
        assert light.LIGHT_ROOM_PK == "room1_light1"
        assert light.STATE_CHAR == "On"

        # Read
        fetched = RoomLight.objects.get(LIGHT_ROOM_PK="room1_light1")
        assert fetched.ROOMKOR_CHAR == "거실"

        # Update
        fetched.STATE_CHAR = "Off"
        fetched.save()
        assert RoomLight.objects.get(LIGHT_ROOM_PK="room1_light1").STATE_CHAR == "Off"

        # Delete
        fetched.delete()
        with pytest.raises(RoomLight.DoesNotExist):
            RoomLight.objects.get(LIGHT_ROOM_PK="room1_light1")

    def test_reserve_crud(self):
        reserve = Reserve.objects.create(
            NAME_CHAR="아침기상",
            ROOM_CHAR="room1",
            ROOMKOR_CHAR="침실",
            TIME_CHAR="07:00",
            DO_CHAR="On",
            DAY_CHAR="Mon,Tue",
            ACTIVATED_CHAR="True",
            REITERATION_CHAR="True",
            HOLIDAY_TINYINT=0
        )
        assert reserve.LIGHT_RESERVE_PK is not None
        assert reserve.NAME_CHAR == "아침기상"

        fetched = Reserve.objects.get(LIGHT_RESERVE_PK=reserve.LIGHT_RESERVE_PK)
        fetched.TIME_CHAR = "08:00"
        fetched.save()
        assert Reserve.objects.get(LIGHT_RESERVE_PK=reserve.LIGHT_RESERVE_PK).TIME_CHAR == "08:00"

        fetched.delete()
        with pytest.raises(Reserve.DoesNotExist):
            Reserve.objects.get(LIGHT_RESERVE_PK=reserve.LIGHT_RESERVE_PK)

    def test_light_record_crud(self):
        record = LightRecord.objects.create(
            DAY_CHAR="2023-10-01",
            TIME_CHAR="12:00:00",
            ROOM_CHAR="room1",
            DO_CHAR="On",
            USER_CHAR="user1"
        )
        assert record.LIGHT_RECORD_PK is not None
        
        fetched = LightRecord.objects.get(LIGHT_RECORD_PK=record.LIGHT_RECORD_PK)
        assert fetched.ROOM_CHAR == "room1"

        fetched.delete()
        with pytest.raises(LightRecord.DoesNotExist):
            LightRecord.objects.get(LIGHT_RECORD_PK=record.LIGHT_RECORD_PK)

    def test_file_default_path_tb_crud(self):
        path = FileDefaultPathTb.objects.create(
            path_name="default",
            public_default_path_char="/public/",
            private_default_path_char="/private/"
        )
        assert path.id is not None
        
        fetched = FileDefaultPathTb.objects.get(id=path.id)
        assert fetched.path_name == "default"

        fetched.delete()
        with pytest.raises(FileDefaultPathTb.DoesNotExist):
            FileDefaultPathTb.objects.get(id=path.id)

    def test_file_private_crud(self):
        file_obj = FilePrivate.objects.create(
            UUID_CHAR="1234-uuid",
            PATH_CHAR="/private/1234",
            NAME_CHAR="test.txt",
            TYPE_CHAR="text/plain",
            SIZE_FLOAT=1024.0,
            OWNER_CHAR="user1",
            LOCATION_CHAR="local",
            STATE_INT=1,
            DELETE_STATUS_INT=0
        )
        assert file_obj.ID_PK is not None
        fetched = FilePrivate.objects.get(ID_PK=file_obj.ID_PK)
        assert fetched.NAME_CHAR == "test.txt"
        fetched.delete()
        with pytest.raises(FilePrivate.DoesNotExist):
            FilePrivate.objects.get(ID_PK=file_obj.ID_PK)

    def test_file_private_trash_tb_crud(self):
        trash = FilePrivateTrashTb.objects.create(
            uuid_char="1234-uuid",
            path_char="/private/trash/1234",
            origin_path_char="/private/1234",
            type_char="text/plain",
            name_char="test.txt",
            size_float=1024.0,
            owner_char="user1",
            location_char="local",
            state_int=0
        )
        assert trash.id_pk is not None
        fetched = FilePrivateTrashTb.objects.get(id_pk=trash.id_pk)
        assert fetched.origin_path_char == "/private/1234"
        fetched.delete()

    def test_file_public_crud(self):
        file_obj = FilePublic.objects.create(
            UUID_CHAR="5678-uuid",
            PATH_CHAR="/public/5678",
            NAME_CHAR="public.txt",
            TYPE_CHAR="text/plain",
            SIZE_FLOAT=2048.0,
            LOCATION_CHAR="local",
            STATE_INT=1,
            DELETE_STATUS_INT=0
        )
        assert file_obj.ID_PK is not None
        fetched = FilePublic.objects.get(ID_PK=file_obj.ID_PK)
        assert fetched.NAME_CHAR == "public.txt"
        fetched.delete()

    def test_file_public_trash_tb_crud(self):
        trash = FilePublicTrashTb.objects.create(
            uuid_char="5678-uuid",
            path_char="/public/trash/5678",
            origin_path_char="/public/5678",
            name_char="public.txt",
            type_char="text/plain",
            size_float=2048.0,
            location_char="local",
            state_int=0
        )
        assert trash.id_pk is not None
        fetched = FilePublicTrashTb.objects.get(id_pk=trash.id_pk)
        assert fetched.origin_path_char == "/public/5678"
        fetched.delete()
