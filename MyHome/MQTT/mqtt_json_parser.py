import json


def json_parser_from_switch(msg: str) -> dict:  # payload to dictionary from switch
    json_object = json.loads(msg)
    dic = {'sender': json_object['sender'], 'message': json_object['message'], 'room': json_object['room']}
    return dic


def json_parser_from_else(msg: str) -> dict:  # payload to dictionary from else(android or server)
    json_object = json.loads(msg)
    dic = {'sender': json_object['Light']['sender'], 'message': json_object['Light']['message'],
           'room': json_object['Light']['room'], 'destination': json_object['Light']['destination']}
    return dic


def json_parser_from_job(msg: str) -> dict:
    json_object = json.loads(msg)
    dic = {'pk': json_object['pk'], 'activation': json_object['activation']}
    return dic


def json_encode_to_switch(dic: dict) -> str:
    # sender : sender who send this message, message : content about payload, destination : specific room name
    msg = {"Light": {"sender": dic['sender'], "message": dic['message'], "destination": dic['destination']}}
    json_object = json.dumps(msg)
    return json_object


def json_encode_to_android(dic: dict) -> str:
    # sender : sender who send this message, message : content about payload, room : category
    msg = {"sender": dic['sender'], "message": dic['message'], "room": dic['room']}
    json_object = json.dumps(msg)
    return json_object


def json_encode_to_server(dic: dict) -> str:
    # sender : sender who send this message, message : payload msg, room : category, destination : specific room name
    msg = {"Light": {"sender": dic['sender'], "message": dic['message'], "room": dic['room'], "destination": dic['destination']}}
    json_object = json.dumps(msg)
    return json_object
