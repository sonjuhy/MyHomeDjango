import pytest
from unittest.mock import patch, MagicMock
from core.models import FilePublic, FilePrivate, FilePublicTrashTb, FilePrivateTrashTb, FileDefaultPathTb
from core.db.database_enum import File as modeEnum
from core.db.database_enum import FileDataType as dataType
from file_manager.db.file_database_connection import DBConnection
import uuid

@pytest.mark.django_db
class TestFileDatabaseConnection:
    def setup_method(self):
        self.conn = DBConnection()
        self.store = FileDefaultPathTb.objects.create(
            path_name='store', 
            public_default_path_char='/pub/store/', 
            private_default_path_char='/priv/store/'
        )
        self.trash = FileDefaultPathTb.objects.create(
            path_name='trash', 
            public_default_path_char='/pub/trash/', 
            private_default_path_char='/priv/trash/'
        )
        self.thumbnail = FileDefaultPathTb.objects.create(
            path_name='thumbnail', 
            public_default_path_char='/pub/thumb/', 
            private_default_path_char='/priv/thumb/'
        )
        self.top = FileDefaultPathTb.objects.create(
            path_name='top', 
            public_default_path_char='/pub/top/', 
            private_default_path_char='/priv/top/'
        )

    def test_get_default_path_public(self):
        res = self.conn.main_query(modeEnum.GET_DEFAULT_PATH.value, 'public')
        assert res == ['/pub/store/', '/pub/trash/', '/pub/thumb/', '/pub/top/']

    def test_get_default_path_private(self):
        res = self.conn.main_query(modeEnum.GET_DEFAULT_PATH.value, 'private')
        assert res == ['/priv/store/', '/priv/trash/', '/priv/thumb/', '/priv/top/']

    def test_move_query_public(self):
        file_obj = FilePublic.objects.create(UUID_CHAR='test-uuid', NAME_CHAR='test.txt', PATH_CHAR='/pub/store/test.txt')
        data = {dataType.UUID: 'test-uuid', dataType.DESTINATION: '/pub/store/new/', 'path': '/pub/store/new/test.txt'}
        self.conn.main_query(modeEnum.MOVE_PUBLIC.value, data)
        fetched = FilePublic.objects.get(NAME_CHAR='test.txt')
        assert fetched.LOCATION_CHAR == '/pub/store/new/'
        assert fetched.PATH_CHAR == '/pub/store/new/test.txt'

    def test_move_query_private(self):
        file_obj = FilePrivate.objects.create(UUID_CHAR='test-uuid-priv', NAME_CHAR='test.txt', PATH_CHAR='/priv/store/test.txt')
        data = {dataType.UUID: 'test-uuid-priv', dataType.DESTINATION: '/priv/store/new/', 'path': '/priv/store/new/test.txt'}
        self.conn.main_query(modeEnum.MOVE_PRIVATE.value, data)
        fetched = FilePrivate.objects.get(NAME_CHAR='test.txt')
        assert fetched.LOCATION_CHAR == '/priv/store/new/'
        assert fetched.PATH_CHAR == '/priv/store/new/test.txt'

    def test_remove_to_trash_query_public_file(self):
        file_obj = FilePublic.objects.create(UUID_CHAR='uuid-1', NAME_CHAR='f1.txt', TYPE_CHAR='file', PATH_CHAR='/pub/store/f1.txt', SIZE_FLOAT=10)
        data = {dataType.UUID: 'uuid-1', dataType.TYPE: 'public', dataType.DESTINATION: '/pub/trash/'}
        self.conn.main_query(modeEnum.DELETE_PUBLIC.value, data)
        assert FilePublic.objects.filter(UUID_CHAR='uuid-1').count() == 0
        assert FilePublicTrashTb.objects.filter(name_char='f1.txt').count() == 1

    def test_remove_to_trash_query_private_file(self):
        file_obj = FilePrivate.objects.create(UUID_CHAR='uuid-2', NAME_CHAR='f2.txt', TYPE_CHAR='file', PATH_CHAR='/priv/store/f2.txt', SIZE_FLOAT=10, OWNER_CHAR='u1')
        data = {dataType.UUID: 'uuid-2', dataType.TYPE: 'private', dataType.DESTINATION: '/priv/trash/'}
        self.conn.main_query(modeEnum.DELETE_PRIVATE.value, data)
        assert FilePrivate.objects.filter(UUID_CHAR='uuid-2').count() == 0
        assert FilePrivateTrashTb.objects.filter(name_char='f2.txt').count() == 1

    def test_remove_to_trash_query_public_dir(self):
        file_obj = FilePublic.objects.create(UUID_CHAR='uuid-3', NAME_CHAR='d1', TYPE_CHAR='dir', PATH_CHAR='/pub/store/d1')
        data = {dataType.UUID: 'uuid-3', dataType.TYPE: 'public', dataType.DESTINATION: '/pub/trash/'}
        self.conn.main_query(modeEnum.DELETE_PUBLIC.value, data)
        assert FilePublicTrashTb.objects.filter(name_char='d1').count() == 1

    def test_remove_to_trash_query_private_dir(self):
        file_obj = FilePrivate.objects.create(UUID_CHAR='uuid-4', NAME_CHAR='d2', TYPE_CHAR='dir', PATH_CHAR='/priv/store/d2', OWNER_CHAR='u1')
        data = {dataType.UUID: 'uuid-4', dataType.TYPE: 'private', dataType.DESTINATION: '/priv/trash/'}
        self.conn.main_query(modeEnum.DELETE_PRIVATE.value, data)
        assert FilePrivateTrashTb.objects.filter(name_char='d2').count() == 1

    def test_restore_from_trash_query_public_file(self):
        trash = FilePublicTrashTb.objects.create(uuid_char='uuid-5', path_char='/pub/trash/f3.txt', origin_path_char='/pub/store/f3.txt', name_char='f3.txt', type_char='file', size_float=10)
        data = {dataType.UUID: 'uuid-5', dataType.TYPE: 'public'}
        self.conn.main_query(modeEnum.RESTORE_PUBLIC.value, data)
        assert FilePublicTrashTb.objects.filter(uuid_char='uuid-5').count() == 0
        assert FilePublic.objects.filter(NAME_CHAR='f3.txt').count() == 1

    def test_restore_from_trash_query_private_file(self):
        trash = FilePrivateTrashTb.objects.create(uuid_char='uuid-6', path_char='/priv/trash/f4.txt', origin_path_char='/priv/store/f4.txt', name_char='f4.txt', type_char='file', size_float=10, owner_char='u1')
        data = {dataType.UUID: 'uuid-6', dataType.TYPE: 'private'}
        self.conn.main_query(modeEnum.RESTORE_PRIVATE.value, data)
        assert FilePrivateTrashTb.objects.filter(uuid_char='uuid-6').count() == 0
        assert FilePrivate.objects.filter(NAME_CHAR='f4.txt').count() == 1

    def test_restore_from_trash_query_public_dir(self):
        trash = FilePublicTrashTb.objects.create(uuid_char='uuid-7', path_char='/pub/trash/d3', origin_path_char='/pub/store/d3', name_char='d3', type_char='dir')
        data = {dataType.UUID: 'uuid-7', dataType.TYPE: 'public'}
        self.conn.main_query(modeEnum.RESTORE_PUBLIC.value, data)
        assert FilePublic.objects.filter(NAME_CHAR='d3').count() == 1

    def test_restore_from_trash_query_private_dir(self):
        trash = FilePrivateTrashTb.objects.create(uuid_char='uuid-8', path_char='/priv/trash/d4', origin_path_char='/priv/store/d4', name_char='d4', type_char='dir', owner_char='u1')
        data = {dataType.UUID: 'uuid-8', dataType.TYPE: 'private'}
        self.conn.main_query(modeEnum.RESTORE_PRIVATE.value, data)
        assert FilePrivate.objects.filter(NAME_CHAR='d4').count() == 1

    def test_delete_query_public(self):
        FilePublic.objects.create(UUID_CHAR='uuid-9', NAME_CHAR='f5.txt', TYPE_CHAR='file')
        data = {dataType.UUID: 'uuid-9', dataType.TYPE: 'public'}
        self.conn.main_query(modeEnum.DELETE_COMMUNAL.value, data)
        assert FilePublic.objects.filter(UUID_CHAR='uuid-9').count() == 0

    def test_delete_query_private(self):
        FilePrivate.objects.create(UUID_CHAR='uuid-10', NAME_CHAR='f6.txt', TYPE_CHAR='file')
        data = {dataType.UUID: 'uuid-10', dataType.TYPE: 'private'}
        self.conn.main_query(modeEnum.DELETE_COMMUNAL.value, data)
        assert FilePrivate.objects.filter(UUID_CHAR='uuid-10').count() == 0

    def test_main_query_invalid_mode(self):
        res = self.conn.main_query("UNKNOWN_MODE", {})
        assert res == []
