import json


def json_parsing(msg: str) -> dict:
    try:
        json_object = json.loads(msg)
        dic = {'purpose': json_object['purpose'], 'uuid': json_object['uuid'], 'file': json_object['file'], 'path': json_object['path'], 'action': json_object['action']}
        return dic
    except Exception as e:
        print('parsing error : {}'.format(e))
        dic = {'purpose': 'error', 'uuid': 'error', 'file': 'error', 'path': 'error'}
        return dic


def json_encoding(result: str) -> str:
    json_object = {'result': result}
    return json.dumps(json_object)
