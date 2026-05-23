import pytest
from file_manager.file.file_json import json_parsing, json_encoding
import json

class TestFileJson:
    def test_json_parsing_success(self):
        msg = json.dumps({
            'purpose': 'p1',
            'uuid': 'u1',
            'file': 'f1',
            'path': 'path1',
            'action': 'a1'
        })
        res = json_parsing(msg)
        assert res['purpose'] == 'p1'
        assert res['uuid'] == 'u1'
        assert res['action'] == 'a1'

    def test_json_parsing_error(self):
        res = json_parsing("invalid json")
        assert res['purpose'] == 'error'
        assert res['uuid'] == 'error'

    def test_json_encoding(self):
        res = json_encoding("success")
        assert json.loads(res)['result'] == "success"
