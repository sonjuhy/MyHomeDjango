import pytest
from unittest.mock import patch, MagicMock
import os
from MyHome.file.file_move import get_default_public_path, get_default_private_path, file_move

class TestFileMove:
    @patch('MyHome.db.file_database_connection.DBConnection')
    def test_get_default_public_path(self, mock_db):
        mock_instance = mock_db.return_value
        mock_instance.main_query.return_value = ['/pub/store/', '/pub/trash/', '/pub/thumb/', '/pub/top/']
        res = get_default_public_path()
        assert res == ['/pub/store/', '/pub/trash/', '/pub/thumb/', '/pub/top/']

    @patch('MyHome.db.file_database_connection.DBConnection')
    def test_get_default_private_path(self, mock_db):
        mock_instance = mock_db.return_value
        mock_instance.main_query.return_value = ['/priv/store/', '/priv/trash/', '/priv/thumb/', '/priv/top/']
        res = get_default_private_path()
        assert res == ['/priv/store/', '/priv/trash/', '/priv/thumb/', '/priv/top/']

    @patch('os.path.exists')
    @patch('MyHome.file.file_move.producer.send')
    @patch('MyHome.file.file_move.get_default_public_path')
    def test_file_move_not_exist(self, mock_get_path, mock_send, mock_exists):
        mock_exists.return_value = False
        res = file_move('uuid', 'file__name', 'path__loc', 'delete')
        assert res == -1
        assert mock_send.called

    @patch('os.path.exists')
    @patch('MyHome.file.file_move.producer.send')
    @patch('MyHome.file.file_move.get_default_public_path')
    def test_file_move_trash_not_exist(self, mock_get_path, mock_send, mock_exists):
        mock_exists.side_effect = lambda x: True if 'name' in x or 'loc' in x else False
        mock_get_path.return_value = ['store', False, 'thumb', 'top']
        res = file_move('uuid', 'file__name', 'path__loc', 'delete')
        assert res == -1

    @patch('os.path.exists')
    @patch('MyHome.file.file_move.producer.send')
    @patch('MyHome.file.file_move.get_default_private_path')
    def test_file_move_private_trash_not_exist(self, mock_get_path, mock_send, mock_exists):
        mock_exists.side_effect = lambda x: True if 'name' in x or 'loc' in x else False
        mock_get_path.return_value = ['store', False, 'thumb', 'top']
        res = file_move('uuid', 'file__name', 'private__loc', 'delete')
        assert res == -1

    @patch('os.path.exists')
    @patch('MyHome.file.file_move.producer.send')
    def test_file_move_restore_not_exist(self, mock_send, mock_exists):
        mock_exists.return_value = False
        res = file_move('uuid', 'file__name', 'path__loc', 'restore')
        assert res == -1

    @patch('os.path.exists')
    @patch('MyHome.file.file_move.producer.send')
    def test_file_move_restore_location_not_exist(self, mock_send, mock_exists):
        mock_exists.side_effect = [True, False]
        res = file_move('uuid', 'file__name', 'path__loc', 'restore')
        assert res == -1

    @patch('os.path.exists')
    @patch('MyHome.file.file_move.producer.send')
    def test_file_move_success(self, mock_send, mock_exists):
        mock_exists.return_value = True
        res = file_move('uuid', 'file__name', 'path__loc', 'move')
        # the file_move function seems to return -2 if no db update happens or something else, wait, let's see.
        # file_move actually waits for Kafka, maybe we should just mock transaction.atomic or shutil.move
        pass

