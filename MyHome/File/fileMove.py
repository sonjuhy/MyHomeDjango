import os
import shutil

from MyHome.Kafka.Kafka_Producer import producer, get_kafka_data, kafka_topic

default_public_path = 'C:\\Users\\SonJunHyeok\\Desktop\\test\\'
default_private_path = 'C:\\Users\\SonJunHyeok\\Desktop\\test\\private'


def file_move(uuid, file, path, action):
    name = file.split('\\')[-1]

    try:
        files = os.listdir(path)
        if os.path.isdir(file):
            for f in files:
                if os.path.isdir(f):
                    if f is name:
                        kafka_msg = '[file_move] file is not exist : {}'.format(path)
                        producer.send(topic=kafka_topic['cloud'], value=get_kafka_data(False, 'cloud', kafka_msg))
                        return -1
        else:
            for f in files:
                if not os.path.isdir(f):
                    if f is name:
                        kafka_msg = '[file_move] file is not exist : {}'.format(path)
                        producer.send(topic=kafka_topic['cloud'], value=get_kafka_data(False, 'cloud', kafka_msg))
                        return -1
        if action == 'delete':
            print('file_move path : {}'.format(path))

        kafka_msg = '[file_move] file move uuid : {uuid}, file : {file}, path : {path}, action : {action}'.format(uuid=uuid, file=file, path=path, action=action)
        producer.send(topic=kafka_topic['cloud'], value=get_kafka_data(True, 'cloud', kafka_msg))
    except Exception as e:
        print('file_move exist check error : {}'.format(e))
        kafka_msg = '[file_move] msg : {}'.format(e)
        producer.send(topic=kafka_topic['cloud'], value=get_kafka_data(False, 'cloud', kafka_msg))
        return -1

    try:
        import MyHome.File.fileDBConnection as fileDB
        db_conn = fileDB.DBConnection()
        if action == 'delete':  # move to trash folder
            if 'private' not in path:  # public folder
                data = {'uuid': uuid, 'type': 'public', 'action': 'remove'}
                # fileDB.DBConnection.main_query('deletePublic', data)
                print('here! : {}'.format(data))
                db_conn.main_query('deletePublic', data)
            else:
                data = {'uuid': uuid, 'type': 'private', 'action': 'remove'}
                db_conn.main_query('deletePrivate', data)
        elif action == 'restore':  # restore file from trash folder
            if 'private' not in path:
                data = {'uuid': uuid, 'type': 'public', 'action': 'restore'}
                db_conn.main_query('restorePublic', data)
                path = path.replace('trash', 'public')
            else:
                data = {'uuid': uuid, 'type': 'private', 'action': 'restore'}
                db_conn.main_query('restorePrivate', data)
                path = path.replace('trash', '')
        else:  # move to path
            data = {'uuid': uuid, 'path': file, 'destination': path}
            if 'private' not in path:
                db_conn.main_query('movePublic', data)
            else:
                db_conn.main_query('movePrivate', data)
        shutil.move(file, path)
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
        import MyHome.File.fileDBConnection as fileDB
        data = {'uuid': uuid, 'type': ''}
        db_conn = fileDB.DBConnection()
        db_conn.main_query('delete', data)
        os.remove(file)
        kafka_msg = '[file_delete] file delete uuid : {uuid}, file : {file}'.format(uuid=uuid, file=file)
        producer.send(topic=kafka_topic['cloud'], value=get_kafka_data(True, 'cloud', kafka_msg))
        return 0
    except Exception as e:
        print('file_delete error : {}'.format(e))
        kafka_msg = '[file_delete] msg : {}'.format(e)
        producer.send(topic=kafka_topic['cloud'], value=get_kafka_data(False, 'cloud', kafka_msg))
        return -1

