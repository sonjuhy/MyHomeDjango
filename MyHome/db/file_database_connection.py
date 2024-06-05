import uuid

from django.db.models.functions import Length
from .database_enum import File as modeEnum
from .database_enum import FileDataType as dataType
from MyHome.models import FilePrivate, FilePublic, FilePublicTrashTb, FilePrivateTrashTb, FileDefaultPathTb


class DBConnection:
    def __init__(self):
        self.schema = None
        self.public_type = 'public'
        self.private_type = 'private'
        self.dir_type = 'dir'

    def main_query(self, mode: str, data: any) -> list:
        if mode == modeEnum.MOVE_PUBLIC.value:
            self.schema = FilePublic
            self.move_query(data)

        elif mode == modeEnum.RESTORE_PUBLIC.value:
            self.schema = FilePublicTrashTb
            self.restore_from_trash_query(data)

        elif mode == modeEnum.DELETE_PUBLIC.value:
            self.schema = FilePublic
            self.remove_to_trash_query(data)

        elif mode == modeEnum.MOVE_PRIVATE.value:
            self.schema = FilePrivate
            self.move_query(data)

        elif mode == modeEnum.RESTORE_PRIVATE.value:
            self.schema = FilePrivateTrashTb
            self.restore_from_trash_query(data)

        elif mode == modeEnum.DELETE_PRIVATE.value:
            self.schema = FilePrivate
            self.remove_to_trash_query(data)

        elif mode == modeEnum.DELETE_COMMUNAL.value:  # uuid, type(public,private)
            if data[dataType.TYPE] == self.private_type:
                self.schema = FilePrivate
            else:
                self.schema = FilePublic
            self.delete_query(data[dataType.UUID])

        elif mode == modeEnum.GET_DEFAULT_PATH.value:
            self.schema = FileDefaultPathTb
            return self.get_default_path(mode=data)
        return []

    def get_default_path(self, mode) -> list:
        store_path = self.schema.objects.get(path_name='store')
        trash_path = self.schema.objects.get(path_name='trash')
        thumbnail_path = self.schema.objects.get(path_name='thumbnail')
        top_path = self.schema.objects.get(path_name='top')
        data = []
        if mode == self.private_type:
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

    def remove_to_trash_query(self, data) -> None:
        column = self.schema.objects.get(UUID_CHAR=data[dataType.UUID])

        if data[dataType.TYPE] == self.public_type:
            default_path = FileDefaultPathTb.objects.get(path_name='store').public_default_path_char
            default_trash = FileDefaultPathTb.objects.get(path_name='trash').public_default_path_char
        else:
            default_path = FileDefaultPathTb.objects.get(path_name='store').private_default_path_char
            default_trash = FileDefaultPathTb.objects.get(path_name='trash').private_default_path_char

        if column.TYPE_CHAR == self.dir_type:
            dirs = (self.schema.objects.filter(PATH_CHAR__contains=column.PATH_CHAR)
                        .annotate(path_len=Length('PATH_CHAR')).order_by('path_len'))

            for tmp_dir in dirs:
                tmp_path = tmp_dir.PATH_CHAR.replace(default_path, default_trash)
                uuid_str = uuid.uuid3(uuid.NAMESPACE_DNS, tmp_path)
                location_str = data[dataType.DESTINATION]
                if tmp_dir.TYPE_CHAR == self.dir_type:
                    name_str = tmp_dir.NAME_CHAR
                    type_str = self.dir_type
                    size_float = 0
                    state_int = 0

                    if data[dataType.TYPE] == self.public_type:
                        new_trash_dto = FilePublicTrashTb(
                            uuid_char=uuid_str,
                            path_char=tmp_path,
                            origin_path_char=tmp_dir.PATH_CHAR,
                            name_char=name_str,
                            type_char=type_str,
                            size_float=size_float,
                            location_char=location_str,
                            state_int=state_int
                        )
                        new_trash_dto.save()
                    else:
                        owner = tmp_dir.OWNER_CHAR
                        new_trash_dto = FilePrivateTrashTb(
                            uuid_char=uuid_str,
                            path_char=tmp_path,
                            origin_path_char=tmp_dir.PATH_CHAR,
                            name_char=name_str,
                            type_char=type_str,
                            size_float=size_float,
                            owner_char=owner,
                            location_char=location_str,
                            state_int=state_int
                        )
                        new_trash_dto.save()
                else:
                    name_str = tmp_dir.NAME_CHAR
                    type_str = tmp_dir.TYPE_CHAR
                    size_float = tmp_dir.SIZE_FLOAT
                    state_int = 0

                    if data[dataType.TYPE] == self.public_type:
                        new_trash_dto = FilePublicTrashTb(
                            uuid_char=uuid_str,
                            path_char=tmp_path,
                            origin_path_char=tmp_dir.PATH_CHAR,
                            name_char=name_str,
                            type_char=type_str,
                            size_float=size_float,
                            location_char=location_str,
                            state_int=state_int
                        )
                        new_trash_dto.save()
                    else:
                        owner = tmp_dir.OWNER_CHAR
                        new_trash_dto = FilePrivateTrashTb(
                            uuid_char=uuid_str,
                            path_char=tmp_path,
                            origin_path_char=tmp_dir.PATH_CHAR,
                            name_char=name_str,
                            type_char=type_str,
                            size_float=size_float,
                            owner_char=owner,
                            location_char=location_str,
                            state_int=state_int
                        )
                        new_trash_dto.save()
                tmp_dir.delete()
        else:
            tmp_path = data[dataType.DESTINATION]+column.NAME_CHAR
            origin_path = column.PATH_CHAR

            uuid_str = uuid.uuid3(uuid.NAMESPACE_DNS, tmp_path)
            path_str = tmp_path
            name_str = column.NAME_CHAR
            type_str = column.TYPE_CHAR
            size_float = column.SIZE_FLOAT
            location_str = data[dataType.DESTINATION]
            state_int = 0

            if data[dataType.TYPE] == self.public_type:
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

    def restore_from_trash_query(self, data) -> None:
        column = self.schema.objects.get(uuid_char=data[dataType.UUID])
        if column.type_char == self.dir_type:
            tmp_dirs = (self.schema.objects.filter(origin_path_char__contains=column.origin_path_char)
                        .annotate(path_len=Length('origin_path_char')).order_by('path_len'))
            for tmp_dir in tmp_dirs:
                uuid_str = uuid.uuid3(uuid.NAMESPACE_DNS, tmp_dir.origin_path_char)
                if tmp_dir.type_char == self.dir_type:
                    type_str = self.dir_type
                    size_float = 0
                    state_int = 0

                    if data[dataType.TYPE] == self.public_type:
                        new_public_dto = FilePublic(
                            UUID_CHAR=uuid_str,
                            PATH_CHAR=tmp_dir.origin_path_char,
                            NAME_CHAR=tmp_dir.name_char,
                            TYPE_CHAR=type_str,
                            SIZE_FLOAT=size_float,
                            LOCATION_CHAR=tmp_dir.origin_path_char.replace(tmp_dir.name_char, ''),
                            STATE_INT=state_int,
                            DELETE_STATUS_INT=0
                        )
                        new_public_dto.save()
                    else:
                        owner = tmp_dir.owner_char
                        new_private_dto = FilePrivate(
                            UUID_CHAR=uuid_str,
                            PATH_CHAR=tmp_dir.origin_path_char,
                            NAME_CHAR=tmp_dir.name_char,
                            TYPE_CHAR=type_str,
                            SIZE_FLOAT=size_float,
                            OWNER_CHAR=owner,
                            LOCATION_CHAR=tmp_dir.origin_path_char.replace(tmp_dir.name_char, ''),
                            STATE_INT=state_int,
                            DELETE_STATUS_INT=0
                        )
                        new_private_dto.save()
                else:
                    type_str = tmp_dir.type_char
                    size_float = tmp_dir.size_float
                    state_int = 0

                    if data[dataType.TYPE] == self.public_type:
                        new_public_dto = FilePublic(
                            UUID_CHAR=uuid_str,
                            PATH_CHAR=tmp_dir.origin_path_char,
                            NAME_CHAR=tmp_dir.name_char,
                            TYPE_CHAR=type_str,
                            SIZE_FLOAT=size_float,
                            LOCATION_CHAR=tmp_dir.origin_path_char.replace(tmp_dir.name_char, ''),
                            STATE_INT=state_int
                        )
                        new_public_dto.save()
                    else:
                        owner = tmp_dir.owner_char
                        new_private_dto = FilePrivate(
                            UUID_CHAR=uuid_str,
                            PATH_CHAR=tmp_dir.origin_path_char,
                            NAME_CHAR=tmp_dir.name_char,
                            TYPE_CHAR=type_str,
                            SIZE_FLOAT=size_float,
                            OWNER_CHAR=owner,
                            LOCATION_CHAR=tmp_dir.origin_path_char.replace(tmp_dir.name_char, ''),
                            STATE_INT=state_int
                        )
                        new_private_dto.save()
                tmp_dir.delete()
        else:
            tmp_path = column.path_char
            origin_path = column.origin_path_char

            uuid_str = uuid.uuid3(uuid.NAMESPACE_DNS, tmp_path)
            path_str = origin_path
            name_str = column.name_char

            location_str = origin_path.replace(name_str, '')
            type_str = column.type_char
            size_float = column.size_float
            state_int = 0

            if data[dataType.TYPE] == self.public_type:
                new_public_dto = FilePublic(
                    UUID_CHAR=uuid_str,
                    PATH_CHAR=path_str,
                    NAME_CHAR=name_str,
                    TYPE_CHAR=type_str,
                    SIZE_FLOAT=size_float,
                    LOCATION_CHAR=location_str,
                    STATE_INT=state_int
                )
                new_public_dto.save()
            else:
                owner = column.owner_char
                new_private_dto = FilePrivate(
                    UUID_CHAR=uuid_str,
                    PATH_CHAR=path_str,
                    NAME_CHAR=name_str,
                    TYPE_CHAR=type_str,
                    SIZE_FLOAT=size_float,
                    OWNER_CHAR=owner,
                    LOCATION_CHAR=location_str,
                    STATE_INT=state_int
                )
                new_private_dto.save()
        column.delete()

    def move_query(self, data) -> None:
        column = self.schema.objects.get(UUID_CHAR=data[dataType.UUID])
        tmp_location = data[dataType.DESTINATION]
        column.PATH_CHAR = data[dataType.DESTINATION] + column.NAME_CHAR
        column.LOCATION_CHAR = tmp_location
        column.UUID_CHAR = uuid.uuid3(uuid.NAMESPACE_DNS, data['path'])
        column.save()

    def delete_query(self, uuid_str) -> None:
        column = self.schema.objects.get(uuid_char=uuid_str)
        if column.type_char == self.dir_type:
            self.schema.objects.filter(path_char__contains=column.path_char).delete()
        else:
            delete_result = column.delete()
            print('delete_query result : {}'.format(delete_result))
