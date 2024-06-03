import json


# def JSON_Parser(object):  # payload to dictionary from switch
#     #print(object)
#     jsonObject = json.loads(object)
#     dic = {'sender': jsonObject['sender'], 'message': jsonObject['message'], 'room': jsonObject['room']}
#     return dic
#
#
# def JSON_Parser_android(object):  # payload to dictionary from android
#     jsonObject = json.loads(object)
#     dic = {'sender': jsonObject['Light']['sender'], 'message': jsonObject['Light']['message'],
#            'room': jsonObject['Light']['room'], 'destination': jsonObject['Light']['destination']}
#     return dic
#
#
# def JSON_Parser_Main(object):
#     json_object = json.loads(object)
#     if json_object[0] == 'Light':
#         dic = JSON_Parser_android(object)
#     else:
#         dic = JSON_Parser(object)
#     return dic


def json_parser_from_switch(msg):  # payload to dictionary from switch
    json_object = json.loads(msg)
    dic = {'sender': json_object['sender'], 'message': json_object['message'], 'room': json_object['room']}
    return dic


def json_parser_from_else(msg):  # payload to dictionary from else(android or server)
    json_object = json.loads(msg)
    dic = {'sender': json_object['Light']['sender'], 'message': json_object['Light']['message'],
           'room': json_object['Light']['room'], 'destination': json_object['Light']['destination']}
    return dic


def json_parser_from_job(msg):
    json_object = json.loads(msg)
    dic = {'pk': json_object['pk'], 'activation': json_object['activation']}
    return dic

# def JSON_ENCODE_TOSERVER(dic):  # dictionary to payload for send to server
#     object = {"Light": {"sender": dic[0][1], "message": dic[1][1], "room": dic[2][1], "destination": dic[3][1]}}
#     jsonObject = json.dumps(object)
#     return jsonObject
#
#
# def JSON_ENCODE(dic):  # dictionary to payload for send to android
#     object = {"sender": dic['sender'], "message": dic['message'], "room": dic['room']}
#     jsonObject = json.dumps(object)
#     return jsonObject
#
#
# def JSON_ENCODE_android(dic):  # dictionary to payload for send to switch (check status)
#     object = {"Light": {"sender": dic[0][1], "message": dic[1][1], "destination": dic[2][1]}}
#     jsonObject = json.dumps(object)
#     return jsonObject


def json_encode_to_switch(dic):  # before def : JSON_ENCODE_android
    # sender : sender who send this message, message : content about payload, destination : specific room name
    msg = {"Light": {"sender": dic['sender'], "message": dic['message'], "destination": dic['destination']}}
    json_object = json.dumps(msg)
    return json_object


def json_encode_to_android(dic):  # before def : JSON_ENCODE
    # sender : sender who send this message, message : content about payload, room : category
    msg = {"sender": dic['sender'], "message": dic['message'], "room": dic['room']}
    json_object = json.dumps(msg)
    return json_object


def json_encode_to_server(dic):  # before : def : JSON_ENCODE_TOSERVER
    # sender : sender who send this message, message : content about payload, room : category, destination : specific room name
    msg = {"Light": {"sender": dic['sender'], "message": dic['message'], "room": dic['room'], "destination": dic['destination']}}
    json_object = json.dumps(msg)
    return json_object
