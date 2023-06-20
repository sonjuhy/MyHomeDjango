from MyHome.models import FilePrivate, FilePublic


class DBConnection:
    def __init__(self):
        self.schema = None

    def main_query(self, mode, data):
        if mode == 'movePublic':
            self.schema = FilePublic
            self.update_query(data)  # uuid, type(public, private), action(move, remove, restore), path, destination
        elif mode == 'restorePublic' or mode == 'deletePublic':
            print('main_query deletePublic data : {}'.format(data))
            self.schema = FilePublic
            self.restore_remove_query(data)
        elif mode == 'movePrivate' or mode == 'restorePrivate':
            self.schema = FilePrivate
            self.restore_remove_query(data)
        elif mode == 'deletePrivate':
            self.schema = FilePrivate
            self.restore_remove_query(data)
        elif mode == 'delete':  # uuid, type(public,private)
            if data['type'] == 'private':
                self.schema = FilePrivate
            else:
                self.schema = FilePublic
            self.delete_query(data['uuid'])

    def update_query(self, data):  # uuid, path, destination
        paths = data['path'].split('\\')
        standard_path = ''
        for idx in range(0, len(paths)-1):
            standard_path += paths[idx]+'\\'
        print('update_query standard : {}'.format(standard_path))
        column = self.schema.objects.get(UUID_PK=data['uuid'])

        if column.TYPE_CHAR == 'dir':
            dir_columns = [column]
            dir_len = len(dir_columns)

            while dir_len > 0:
                for idx in range(0, dir_len):
                    location_char = dir_columns[0].PATH_CHAR + '\\'
                    columns = self.schema.objects.filter(LOCATION_CHAR=location_char)

                    origin_col = dir_columns.pop(0)
                    path = origin_col.PATH_CHAR.replace(standard_path, data['destination'])
                    location = origin_col.LOCATION_CHAR.replace(standard_path, data['destination'])
                    origin_col.PATH_CHAR = path
                    origin_col.LOCATION_CHAR = location
                    origin_col.save()

                    for col in columns:
                        if col.TYPE_CHAR == 'dir':
                            dir_columns.append(col)
                        col.PATH_CHAR = col.PATH_CHAR.replace(standard_path, data['destination'])
                        col.LOCATION_CHAR = col.LOCATION_CHAR.replace(standard_path, data['destination'])
                        col.save()
                dir_len = len(dir_columns)
                print('update_query dir len : {}'.format(dir_len))
        else:
            path = column.PATH_CHAR
            print('update_query path in file : {}'.format(path))
            column.PATH_CHAR = path.replace(standard_path, data['destination'])
            location = column.LOCATION_CHAR
            column.LOCATION_CHAR = location.replace(standard_path, data['destination'])
            column.save()

    def restore_remove_query(self, data):
        column = self.schema.objects.get(UUID_PK=data['uuid'])
        if column.TYPE_CHAR == 'dir':
            dir_columns = [column]
            dir_len = len(dir_columns)
            while dir_len > 0:
                # remove folder db info
                self.move_query(dir_columns[0].UUID_PK, data['type'], data['action'])

                for idx in range(0, dir_len):
                    path_char = dir_columns.pop(0).PATH_CHAR
                    columns = self.schema.objects.filter(LOCATION_CHAR=path_char + '\\')
                    for col in columns:
                        if col.TYPE_CHAR == 'dir':
                            dir_columns.append(col)
                        self.move_query(col.UUID_PK, data['type'], data['action'])
                dir_len = len(dir_columns)
        else:
            self.move_query(column.UUID_PK, data['type'], data['action'])

    def move_query(self, uuid, mode_type, action):
        origin_column = self.schema.objects.get(UUID_PK=uuid)
        if action == 'remove':
            origin_column.DELETE_STATUS_INT = 1
            if mode_type == 'private':
                tmp_location = origin_column.LOCATION_CHAR
                tmp_location = tmp_location[0:tmp_location.find('User_') + 7] + '_trash' + tmp_location[tmp_location.find('User_') + 7:]
                origin_column.LOCATION_CHAR = tmp_location
                tmp_path = origin_column.PATH_CHAR
                tmp_path = tmp_path[0:tmp_path.find('User_') + 7] + '_trash' + tmp_path[tmp_path.find('User_') + 7:]
                origin_column.PATH_CHAR = tmp_path
            else:
                origin_column.LOCATION_CHAR = origin_column.LOCATION_CHAR.replace('public', 'trash')
                origin_column.PATH_CHAR = origin_column.PATH_CHAR.replace('public', 'trash')
        else:  # restore
            origin_column.DELETE_STATUS_INT = 0
            if mode_type == 'private':
                origin_column.LOCATION_CHAR = origin_column.LOCATION_CHAR.replace('_trash', '')
                origin_column.PATH_CHAR = origin_column.PATH_CHAR.replace('_trash', '')
            else:
                origin_column.LOCATION_CHAR = origin_column.LOCATION_CHAR.replace('trash', 'public')
                origin_column.PATH_CHAR = origin_column.PATH_CHAR.replace('trash', 'public')
        origin_column.save()

    def delete_query(self, uuid):
        column = self.schema.objects.get(UUID_PK=uuid)
        delete_result = column.delete()
        print('delete_query result : {}'.format(delete_result))
