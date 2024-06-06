import os
import shutil
import traceback

from django.db import transaction

from MyHome.kafka.kafka_producer import producer, get_kafka_data, kafka_topic
from MyHome.db.database_enum import File as modeFileEnum
import MyHome.db.file_database_connection as file_database


def get_default_public_path() -> list:
    """
    return default path of public cloud

    data order
        [0] : store path.
        [1] : trash path.
        [2] : thumbnail path.
        [3] : top path.

    Returns:
        4 len of list
    """
    db_conn = file_database.DBConnection()
    default_paths = db_conn.main_query(mode='default', data='public')
    return default_paths


def get_default_private_path() -> list:
    """
        return default path of private cloud

        data order
            [0] : store path.
            [1] : trash path.
            [2] : thumbnail path.
            [3] : top path.

        Returns:
            4 len of list
        """
    db_conn = file_database.DBConnection()
    default_paths = db_conn.main_query(mode='default', data='private')
    return default_paths


def file_move(uuid: str, file: str, path: str, action: str) -> int:  # file : file path, path : location to move file
    """
        return result of move file

        Returns:
            0 - success.
            -1 - not exist file.
            -2 - error while move file or update db.
        """
    mode = True  # public
    if 'private' in path:
        mode = False  # private
    under_bar = '__'
    name = file.split(under_bar)[-1]
    origin_path = file.replace(under_bar, os.path.sep)
    origin_location = path.replace(name, '').replace(under_bar, os.path.sep)

    # check file exist
    try:
        if action == 'delete' or action == 'move':
            if os.path.exists(origin_path) and os.path.exists(origin_location):
                if action == 'delete':  # move to trash folder
                    if mode:  # public
                        default_paths = get_default_public_path()  # store, trash, thumbnail, top
                        trash_path = default_paths[1].replace('__', os.path.sep)
                        if trash_path is False:
                            kafka_msg = '[file_move] trash folder is not exist : {}'.format(path)
                            producer.send(topic=kafka_topic['cloud'], value=get_kafka_data(False, 'cloud', kafka_msg))
                            return -1
                    else:  # private
                        default_paths = get_default_private_path()
                        trash_path = default_paths[1].replace('__', os.path.sep)
                        if trash_path is False:
                            kafka_msg = '[file_move] trash folder is not exist : {}'.format(path)
                            producer.send(topic=kafka_topic['cloud'], value=get_kafka_data(False, 'cloud', kafka_msg))
                            return -1
                kafka_msg = '[file_move] file move uuid : {uuid}, file : {file}, path : {path}, action : {action}'.format(
                    uuid=uuid, file=file, path=path, action=action)
                producer.send(topic=kafka_topic['cloud'], value=get_kafka_data(True, 'cloud', kafka_msg))
            else:
                kafka_msg = ('[file_move] file is not exist : path {path}, origin_path {origin_path}, origin_location {'
                             'origin_location}').format(path=path, origin_path=origin_path,
                                                        origin_location=origin_location)
                producer.send(topic=kafka_topic['cloud'], value=get_kafka_data(False, 'cloud', kafka_msg))
                return -1
        elif action == 'restore':
            if not os.path.exists(origin_path):
                kafka_msg = ('[file_move] restore file is not exist : path {path}, origin_path {origin_path}, '
                             'origin_location {origin_location}').format(path=path, origin_path=origin_path,
                                                                         origin_location=origin_location)
                producer.send(topic=kafka_topic['cloud'], value=get_kafka_data(False, 'cloud', kafka_msg))
                return -1
            if not os.path.exists(origin_location):
                if mode:
                    default_paths = get_default_public_path()  # store, trash, thumbnail, top
                    origin_path = default_paths[0].replace('__', os.path.sep)
                else:
                    default_paths = get_default_private_path()  # store, trash, thumbnail, top
                    origin_path = default_paths[0].replace('__', os.path.sep)

    except Exception as e:
        print(
            'file_move exist check error : path {path}, origin_path {origin_path}, origin_location {origin_location}'.format(
                path=path, origin_path=origin_path, origin_location=origin_location))
        kafka_msg = ('[file_move] file_move exist check error : path {path}, origin_path {origin_path}, '
                     'origin_location {origin_location} \n log {log}').format(path=path, origin_path=origin_path,
                                                                              origin_location=origin_location,
                                                                              log=traceback.format_exc())
        producer.send(topic=kafka_topic['cloud'], value=get_kafka_data(False, 'cloud', kafka_msg))
        return -1

    try:
        with transaction.atomic():
            db_conn = file_database.DBConnection()
            if action == 'delete':  # move to trash folder
                if mode:  # public folder
                    data = {'uuid': uuid, 'type': 'public', 'action': 'remove', 'destination': path.replace(name, '')}
                    db_conn.main_query(mode=modeFileEnum.DELETE_PUBLIC.value, data=data)
                else:
                    data = {'uuid': uuid, 'type': 'private', 'action': 'remove', 'destination': path.replace(name, '')}
                    db_conn.main_query(mode=modeFileEnum.DELETE_PRIVATE.value, data=data)
            elif action == 'restore':  # restore file from trash folder
                if mode:
                    data = {'uuid': uuid, 'type': 'public', 'action': 'restore', 'destination': path.replace(name, '')}
                    db_conn.main_query(mode=modeFileEnum.RESTORE_PUBLIC.value, data=data)
                    path = path.replace('trash', 'public')
                else:
                    data = {'uuid': uuid, 'type': 'private', 'action': 'restore', 'destination': path.replace(name, '')}
                    db_conn.main_query(mode=modeFileEnum.RESTORE_PRIVATE.value, data=data)
                    path = path.replace('trash', '')
            else:  # move to path
                data = {'uuid': uuid, 'path': file, 'destination': path.replace(name, '')}
                if mode:
                    db_conn.main_query(mode=modeFileEnum.MOVE_PUBLIC.value, data=data)
                else:
                    db_conn.main_query(mode=modeFileEnum.MOVE_PRIVATE.value, data=data)

            shutil.move(origin_path, origin_location + name)  # move file
            kafka_msg = '[file_move] db Update uuid : {uuid}, file : {file}, path : {path}, action : {action}'.format(
                uuid=uuid, file=file, path=path, action=action)
            producer.send(topic=kafka_topic['cloud'], value=get_kafka_data(True, 'cloud', kafka_msg))
            return 0
    except Exception as e:
        print('error : {}'.format(e))
        kafka_msg = '[file_move] error while db & move. msg : {}'.format(traceback.format_exc())
        producer.send(topic=kafka_topic['cloud'], value=get_kafka_data(False, 'cloud', kafka_msg))
        return -2


def file_delete(uuid: str, file: str) -> int:
    """
        return result of delete file

        Returns:
            0 - success.
            -1 - not exist file.
            -2 - error while move file or update db.
    """
    try:
        with transaction.atomic():
            under_bar = '__'
            origin_path = file.replace(under_bar, os.path.sep)

            if os.path.exists(origin_path):
                data = {'uuid': uuid, 'type': ''}
                db_conn = file_database.DBConnection()
                db_conn.main_query(mode=modeFileEnum.DELETE_COMMUNAL.value, data=data)

                os.remove(origin_path)
                kafka_msg = '[file_delete] file delete uuid : {uuid}, file : {file}'.format(uuid=uuid, file=file)
                producer.send(topic=kafka_topic['cloud'], value=get_kafka_data(True, 'cloud', kafka_msg))
                return 0
            else:
                kafka_msg = "[file_delete] file doesn't exist"
                producer.send(topic=kafka_topic['cloud'], value=get_kafka_data(False, 'cloud', kafka_msg))
                return -1
    except Exception as e:
        print('file_delete error : {}'.format(e))
        kafka_msg = '[file_delete] msg : {}'.format(e)
        producer.send(topic=kafka_topic['cloud'], value=get_kafka_data(False, 'cloud', kafka_msg))
        return -2
