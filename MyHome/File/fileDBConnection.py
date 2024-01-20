import os
import uuid

from MyHome.models import FilePrivate, FilePublic, FilePublicTrashTb, FilePrivateTrashTb, FileDefaultPathTb


class DBConnection:
    def __init__(self):
        self.schema = None

    def main_query(self, mode, data):
        if mode == 'movePublic':
            self.schema = FilePublic
            self.move_query(data)

        elif mode == 'restorePublic':
            self.schema = FilePublicTrashTb
            self.restore_from_trash_query(data)

        elif mode == 'deletePublic':
            self.schema = FilePublic
            self.remove_to_trash_query(data)

        elif mode == 'movePrivate':
            self.schema = FilePrivate
            self.move_query(data)

        elif mode == 'restorePrivate':
            self.schema = FilePrivateTrashTb
            self.restore_from_trash_query(data)

        elif mode == 'deletePrivate':
            self.schema = FilePrivate
            self.remove_to_trash_query(data)

        elif mode == 'delete':  # uuid, type(public,private)
            if data['type'] == 'private':
                self.schema = FilePrivate
            else:
                self.schema = FilePublic
            self.delete_query(data['uuid'])

        elif mode == 'default':
            self.schema = FileDefaultPathTb
            return self.get_default_path(mode=data)

    def get_default_path(self, mode):
        store_path = self.schema.objects.get(path_name='store')
        trash_path = self.schema.objects.get(path_name='trash')
        thumbnail_path = self.schema.objects.get(path_name='thumbnail')
        top_path = self.schema.objects.get(path_name='top')
        data = []
        if mode == 'private':
            data.append(store_path.private_default_path_char)
            data.append(trash_path.private_default_path_char)
            data.append(thumbnail_path.private_default_path_char)
            data.append(top_path.private_default_path_char)
        else:
            data.append(store_path.public_default_path_char)
            data.append(trash_path.public_default_path_char)
            data.append(thumbnail_path.public_default_path_char)
            data.append(top_path.public_default_path_char)
        return data

    def remove_to_trash_query(self, data):
        column = self.schema.objects.get(UUID_CHAR=data['uuid'])
        under_bar = '__'
        if column.TYPE_CHAR == 'dir':
            root_dto = FilePublicTrashTb(
                uuid_char=uuid.uuid3(uuid.NAMESPACE_DNS, data['destination'].replace(under_bar, os.path.sep)+column.NAME_CHAR),
                path_char=data['destination']+column.NAME_CHAR,
                origin_path_char=column.PATH_CHAR,
                name_char=column.NAME_CHAR,
                type_char='dir',
                size_float=0,
                location_char=data['destination'],
                state_int=0
            )
            root_dto.save()
            for (root, dirs, files) in os.walk(column.PATH_CHAR):
                # root(object) : files root folder path
                # dirs(len) : dirs under root folder
                # files(len) : dirs under root file
                under_bar_root = root.replace(os.path.sep, under_bar)
                for tmp_dir in dirs:
                    tmp_path = (root + tmp_dir).replace(os.path.sep, under_bar)
                    dir_info = self.schema.objects.get(PATH_CHAR=tmp_path)
                    origin_path = dir_info.PATH_CHAR

                    uuid_str = uuid.uuid3(uuid.NAMESPACE_DNS, tmp_path)
                    path_str = tmp_path
                    name_str = tmp_dir
                    type_str = 'dir'
                    size_float = 0
                    location_str = data['destination']
                    state_int = 0

                    if data['type'] == 'public':
                        new_trash_dto = FilePublicTrashTb(
                            uuid_char=uuid_str,
                            path_char=path_str,
                            origin_path_char=origin_path,
                            name_char=name_str,
                            type_char=type_str,
                            size_float=size_float,
                            location_char=location_str,
                            state_int=state_int
                        )
                        new_trash_dto.save()
                    else:
                        owner = dir_info.OWNER_CHAR
                        new_trash_dto = FilePrivateTrashTb(
                            uuid_char=uuid_str,
                            path_char=path_str,
                            origin_path_char=origin_path,
                            name_char=name_str,
                            type_char=type_str,
                            size_float=size_float,
                            owner_char=owner,
                            location_char=location_str,
                            state_int=state_int
                        )
                        new_trash_dto.save()

                    dir_info.delete()

                for tmp_file in files:
                    tmp_path = (under_bar_root + tmp_file).replace(os.path.sep, under_bar)
                    file_info = self.schema.objects.get(PATH_CHAR=tmp_path)
                    origin_path = file_info.PATH_CHAR

                    uuid_str = uuid.uuid3(uuid.NAMESPACE_DNS, tmp_path)
                    path_str = tmp_path
                    name_str = tmp_file
                    type_str = os.path.splitext(tmp_file)[1].lstrip('.')
                    # size_float = os.path.getsize(origin_path.replace(under_bar, os.path.sep))
                    size_float = file_info.SIZE_FLOAT
                    location_str = data['destination']
                    state_int = 0

                    if data['type'] == 'public':
                        new_trash_dto = FilePublicTrashTb(
                            uuid_char=uuid_str,
                            path_char=path_str,
                            origin_path_char=origin_path,
                            name_char=name_str,
                            type_char=type_str,
                            size_float=size_float,
                            location_char=location_str,
                            state_int=state_int
                        )
                        new_trash_dto.save()
                    else:
                        owner = file_info.OWNER_CHAR
                        new_trash_dto = FilePrivateTrashTb(
                            uuid_char=uuid_str,
                            path_char=path_str,
                            origin_path_char=origin_path,
                            name_char=name_str,
                            type_char=type_str,
                            size_float=size_float,
                            owner_char=owner,
                            location_char=location_str,
                            state_int=state_int
                        )
                        new_trash_dto.save()
                    file_info.delete()
        else:
            tmp_path = data['destination']+column.NAME_CHAR
            origin_path = tmp_path.replace(under_bar, os.path.sep)

            uuid_str = uuid.uuid3(uuid.NAMESPACE_DNS, tmp_path)
            path_str = tmp_path
            name_str = column.NAME_CHAR
            type_str = column.TYPE_CHAR
            size_float = column.SIZE_FLOAT
            location_str = data['destination']
            state_int = 0

            if data['type'] == 'public':
                new_trash_dto = FilePublicTrashTb(
                    uuid_char=uuid_str,
                    path_char=path_str,
                    origin_path_char=origin_path,
                    name_char=name_str,
                    type_char=type_str,
                    size_float=size_float,
                    location_char=location_str,
                    state_int=state_int
                )
                new_trash_dto.save()
            else:
                owner = column.OWNER_CHAR
                new_trash_dto = FilePrivateTrashTb(
                    uuid_char=uuid_str,
                    path_char=path_str,
                    origin_path_char=origin_path,
                    name_char=name_str,
                    type_char=type_str,
                    size_float=size_float,
                    owner_char=owner,
                    location_char=location_str,
                    state_int=state_int
                )
                new_trash_dto.save()
        column.delete()

    def restore_from_trash_query(self, data):
        column = self.schema.objects.get(UUID_CHAR=data['uuid'])
        under_bar = '__'
        if column.TYPE_CHAR == 'dir':
            # 1. 루트 폴더 산하에 있는걸 찾는다. findByLocation(path)
            # 2. 폴더들은 따로 저장한다.
            # 3. 끝나면 폴더들을 루트로 잡고 다시 찾는다.
            dirs = self.schema.objects.get(LOCATION_CHAR=column.PATH_CHAR)
            dir_list = []
            for dir_info in dirs:
                dir_list.append(dir_info)

            while len(dir_list) > 0:
                list_size = len(dir_list)
                for i in range(list_size):
                    dir_info = dir_list.pop(0)  # root folder

                    tmp_path = dir_info.PATH_CHAR
                    origin_path = dir_info.ORIGIN_PATH_CHAR

                    uuid_str = uuid.uuid3(uuid.NAMESPACE_DNS, tmp_path)
                    path_str = origin_path
                    name_str = dir_info.NAME_CHAR

                    location_str = ''
                    tmp_locations = origin_path.slite(under_bar)
                    for point in range(len(tmp_locations) - 1):
                        location_str += tmp_locations[point] + under_bar

                    if dir_info.TYPE_CHAR == 'dir':
                        dir_list.append(dir_info)
                        tmp_dir_list = self.schema.objects.get(LOCATION_CHAR=dir_info.PATH_CHAR)
                        for tmp_dir in tmp_dir_list:
                            dir_list.append(tmp_dir)

                        type_str = 'dir'
                        size_float = 0
                        state_int = 0

                        if data['type'] == 'public':
                            new_public_dto = FilePublic(
                                UUID_CHAR=uuid_str,
                                PATH_CHAR=path_str,
                                NAME_CHAR=name_str,
                                TYPE_CHAR=type_str,
                                SIZE_FLOAT=size_float,
                                LOCATION_CHAR=location_str,
                                STATE_INT=state_int,
                                DELETE_STATUS_INT=0
                            )
                            new_public_dto.save()
                        else:
                            owner = dir_info.OWNER_CHAR
                            new_private_dto = FilePrivate(
                                UUID_CHAR=uuid_str,
                                PATH_CHAR=path_str,
                                NAME_CHAR=name_str,
                                TYPE_CHAR=type_str,
                                SIZE_FLOAT=size_float,
                                OWNER_CHAR=owner,
                                LOCATION_CHAR=location_str,
                                STATE_INT=state_int,
                                DELETE_STATUS_INT=0
                            )
                            new_private_dto.save()
                    else:
                        type_str = dir_info.TYPE_CHAR
                        size_float = dir_info.size_float
                        state_int = 0

                        if data['type'] == 'public':
                            new_public_dto = FilePublic(
                                uuid_char=uuid_str,
                                path_char=path_str,
                                origin_path_char=origin_path,
                                name_char=name_str,
                                type_char=type_str,
                                size_float=size_float,
                                location_char=location_str,
                                state_int=state_int
                            )
                            new_public_dto.save()
                        else:
                            owner = dir_info.OWNER_CHAR
                            new_private_dto = FilePrivate(
                                uuid_char=uuid_str,
                                path_char=path_str,
                                origin_path_char=origin_path,
                                name_char=name_str,
                                type_char=type_str,
                                size_float=size_float,
                                owner_char=owner,
                                location_char=location_str,
                                state_int=state_int
                            )
                            new_private_dto.save()
        else:
            tmp_path = column.PATH_CHAR
            origin_path = column.ORIGIN_PATH_CHAR

            uuid_str = uuid.uuid3(uuid.NAMESPACE_DNS, tmp_path)
            path_str = origin_path
            name_str = column.NAME_CHAR

            location_str = ''
            tmp_locations = origin_path.slite(under_bar)
            for point in range(len(tmp_locations) - 1):
                location_str += tmp_locations[point] + under_bar
            type_str = column.TYPE_CHAR
            size_float = column.size_float
            state_int = 0

            if data['type'] == 'public':
                new_public_dto = FilePublic(
                    uuid_char=uuid_str,
                    path_char=path_str,
                    origin_path_char=origin_path,
                    name_char=name_str,
                    type_char=type_str,
                    size_float=size_float,
                    location_char=location_str,
                    state_int=state_int
                )
                new_public_dto.save()
            else:
                owner = column.OWNER_CHAR
                new_private_dto = FilePrivate(
                    uuid_char=uuid_str,
                    path_char=path_str,
                    origin_path_char=origin_path,
                    name_char=name_str,
                    type_char=type_str,
                    size_float=size_float,
                    owner_char=owner,
                    location_char=location_str,
                    state_int=state_int
                )
                new_private_dto.save()
        column.delete()

    def move_query(self, data):
        column = self.schema.objects.get(UUID_CHAR=data['uuid'])
        tmp_location = data['destination']
        column.PATH_CHAR = data['destination'] + column.NAME_CHAR
        column.LOCATION_CHAR = tmp_location
        column.UUID_CHAR = uuid.uuid3(uuid.NAMESPACE_DNS, data['path'])
        column.save()

    def delete_query(self, uuid_str):
        column = self.schema.objects.get(UUID_CHAR=uuid_str)
        delete_result = column.delete()
        print('delete_query result : {}'.format(delete_result))
