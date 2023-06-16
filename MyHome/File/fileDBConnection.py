from MyHome.models import FilePrivate, FilePrivateTrash, FilePublicTrash, FilePublic


class DBConnection:
    def __init__(self):
        self.schema = None

    def main_query(self, mode, data):
        if mode == 'movePublic':
            self.schema = FilePublic
            self.update_query(data)  # uuid, type(public, private), action(move, remove, restore), path, destination
        elif mode == 'restorePublic':
            self.schema = FilePublicTrash
            self.restore_remove_query(data)  # uuid, type(public, private), action(move, remove, restore)
        elif mode == 'deletePublic':
            print('main_query deletePublic data : {}'.format(data))
            self.schema = FilePublic
            self.restore_remove_query(data)
        elif mode == 'movePrivate':
            self.schema = FilePrivate
            self.update_query(data)
        elif mode == 'restorePrivate':
            self.schema = FilePrivateTrash
            self.restore_remove_query(data)
        elif mode == 'deletePrivate':
            self.schema = FilePrivate
            self.restore_remove_query(data)
        elif mode == 'delete':  # uuid, type(public,private)
            if data['type'] == 'private':
                self.schema = FilePrivateTrash
            else:
                self.schema = FilePublicTrash
            self.delete_query(data['uuid'])

    def update_query(self, data):  # uuid, path, destination
        column = self.schema.objects.get(UUID_PK=data['uuid'])
        if column.TYPE_CHAR == 'dir':
            dir_columns = [column]
            dir_len = len(dir_columns)

            for idx in range(0, dir_len):
                location_char = dir_columns.pop(0).LOCATION_CHAR
                columns = self.schema.objects.filter(LOCATION_CHAR=location_char)
                for col in columns:
                    if column.TYPE_CHAR == 'dir':
                        dir_columns.append(col)
                    path = col.PATH_CHAR
                    path.replace(data['path'], data['destination'])
                    col.PATH_CHAR = path
                    col.LOCATION_CHAR = data['destination']
                column.save()
        else:
            path = column.PATH_CHAR
            path.replace(data['path'], data['destination'])
            column.PATH_CHAR = path
            column.LOCATION_CHAR = data['destination']
            column.save()

    def restore_remove_query(self, data):
        column = self.schema.objects.get(UUID_PK=data['uuid'])
        if column.TYPE_CHAR == 'dir':
            dir_columns = [column]
            dir_len = len(dir_columns)
            while dir_len > 0:
                # remove folder db info
                if data['type'] == 'public':
                    if data['action'] == 'remove':
                        destination_schema = FilePublicTrash
                    elif data['action'] == 'restore':
                        destination_schema = FilePublic
                else:
                    if data['action'] == 'remove':
                        destination_schema = FilePrivateTrash
                    elif data['action'] == 'restore':
                        destination_schema = FilePrivate
                self.move_query(dir_columns[0].UUID_PK, data['type'], destination_schema)

                for idx in range(0, dir_len):
                    path_char = dir_columns.pop(0).PATH_CHAR
                    columns = self.schema.objects.filter(LOCATION_CHAR=path_char+'\\')
                    for col in columns:
                        if col.TYPE_CHAR == 'dir':
                            dir_columns.append(col)
                        self.move_query(col.UUID_PK, data['type'], destination_schema)
                dir_len = len(dir_columns)
        else:
            if data['type'] == 'public':
                if data['action'] == 'remove':
                    self.move_query(column.UUID_PK, data['type'], FilePublicTrash)
                elif data['action'] == 'restore':
                    self.move_query(column.UUID_PK, data['type'], FilePublic)
            else:
                if data['action'] == 'remove':
                    self.move_query(column.UUID_PK, data['type'], FilePrivateTrash)
                elif data['action'] == 'restore':
                    self.move_query(column.UUID_PK, data['type'], FilePrivate)

    def move_query(self, uuid, mode_type, destination_schema):
        origin_column = self.schema.objects.get(UUID_PK=uuid)
        destination_column = destination_schema()
        if mode_type == 'private':
            destination_column.OWNER_CHAR = origin_column.OWNER_CHAR
        destination_column.UUID_PK = origin_column.UUID_PK
        destination_column.PATH_CHAR = origin_column.PATH_CHAR
        destination_column.NAME_CHAR = origin_column.NAME_CHAR
        destination_column.TYPE_CHAR = origin_column.TYPE_CHAR
        destination_column.SIZE_FLOAT = origin_column.SIZE_FLOAT
        destination_column.LOCATION_CHAR = origin_column.LOCATION_CHAR
        destination_column.STATE_INT = origin_column.STATE_INT
        destination_column.save()
        delete_result = origin_column.delete()
        print('move_query delete result : {}'.format(delete_result))

    def delete_query(self, uuid):
        column = self.schema.objects.get(UUID_PK=uuid)
        column.delete()

