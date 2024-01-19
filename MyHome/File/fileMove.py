import os
import shutil

from MyHome.Kafka.Kafka_Producer import producer, get_kafka_data, kafka_topic
import MyHome.File.fileDBConnection as fileDB


def get_default_public_path():
    db_conn = fileDB.DBConnection()
    default_paths = db_conn.main_query('default', 'public')
    return default_paths


def get_default_private_path():
    db_conn = fileDB.DBConnection()
    default_paths = db_conn.main_query('default', 'public')
    return default_paths


def file_move(uuid, file, path, action):
    mode = True  # public
    if 'private' in path:
        mode = False  # private
    under_bar = '__'
    origin_path = file.replace(under_bar, os.path.sep)
    origin_location = path.replace(under_bar, os.path.sep)
    name = file.split(under_bar)[-1]

    # check file exist
    try:
        if os.path.exists(origin_path) and os.path.exists(origin_location):
            if action == 'delete':  # move to trash folder
                print('file_move path : {}'.format(path))
                if mode:  # public
                    default_paths = get_default_public_path()  # store, trash, thumbnail, top
                    if os.path.exists(default_paths[1]) is False:
                        kafka_msg = '[file_move] trash folder is not exist : {}'.format(path)
                        producer.send(topic=kafka_topic['cloud'], value=get_kafka_data(False, 'cloud', kafka_msg))
                        return -1
                else:  # private
                    default_paths = get_default_private_path()
                    if os.path.exists(default_paths[1]) is False:
                        kafka_msg = '[file_move] trash folder is not exist : {}'.format(path)
                        producer.send(topic=kafka_topic['cloud'], value=get_kafka_data(False, 'cloud', kafka_msg))
                        return -1

            kafka_msg = '[file_move] file move uuid : {uuid}, file : {file}, path : {path}, action : {action}'.format(
                uuid=uuid, file=file, path=path, action=action)
            producer.send(topic=kafka_topic['cloud'], value=get_kafka_data(True, 'cloud', kafka_msg))
        else:
            kafka_msg = '[file_move] file is not exist : {}'.format(path)
            producer.send(topic=kafka_topic['cloud'], value=get_kafka_data(False, 'cloud', kafka_msg))
            return -1
    except Exception as e:
        print('file_move exist check error : {}'.format(e))
        kafka_msg = '[file_move] msg : {}'.format(e)
        producer.send(topic=kafka_topic['cloud'], value=get_kafka_data(False, 'cloud', kafka_msg))
        return -1

    try:
        db_conn = fileDB.DBConnection()
        if action == 'delete':  # move to trash folder
            if mode:  # public folder
                data = {'uuid': uuid, 'type': 'public', 'action': 'remove', 'destination': path}
                db_conn.main_query('deletePublic', data)
            else:
                data = {'uuid': uuid, 'type': 'private', 'action': 'remove', 'destination': path}
                db_conn.main_query('deletePrivate', data)
        elif action == 'restore':  # restore file from trash folder
            if mode:
                data = {'uuid': uuid, 'type': 'public', 'action': 'restore', 'destination': path}
                db_conn.main_query('restorePublic', data)
                path = path.replace('trash', 'public')
            else:
                data = {'uuid': uuid, 'type': 'private', 'action': 'restore', 'destination': path}
                db_conn.main_query('restorePrivate', data)
                path = path.replace('trash', '')
        else:  # move to path
            data = {'uuid': uuid, 'path': file, 'destination': path}
            if mode:
                db_conn.main_query('movePublic', data)
            else:
                db_conn.main_query('movePrivate', data)

        shutil.move(origin_path, origin_location+name)  # move file
        kafka_msg = '[file_move] DB Update uuid : {uuid}, file : {file}, path : {path}, action : {action}'.format(
            uuid=uuid, file=file, path=path, action=action)
        producer.send(topic=kafka_topic['cloud'], value=get_kafka_data(True, 'cloud', kafka_msg))
        return 0
    except Exception as e:
        print('error : {}'.format(e))
        kafka_msg = '[file_move] msg : {}'.format(e)
        producer.send(topic=kafka_topic['cloud'], value=get_kafka_data(False, 'cloud', kafka_msg))
        return -2


def file_delete(uuid, file):
    try:
        data = {'uuid': uuid, 'type': ''}
        db_conn = fileDB.DBConnection()
        db_conn.main_query('delete', data)

        under_bar = '__'
        origin_path = file.replace(under_bar, os.path.sep)

        if os.path.exists(origin_path):
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
        return -1

