from django.db import models


# Create your models here.


class RoomLight(models.Model):
    LIGHT_ROOM_PK = models.CharField(max_length=20, primary_key=True)
    STATE_CHAR = models.CharField(max_length=10)
    ROOMKOR_CHAR = models.CharField(max_length=20)
    CATEGORY_CHAR = models.CharField(max_length=100)
    CONNECT_CHAR = models.CharField(max_length=25)

    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'LIGHT_ROOM_TB'


class Reserve(models.Model):
    LIGHT_RESERVE_PK = models.AutoField(db_column='LIGHT_RESERVE_PK', primary_key=True)  # Field name made lowercase.
    NAME_CHAR = models.CharField(db_column='NAME_CHAR', max_length=32, blank=True,
                                 null=True)  # Field name made lowercase.
    ROOM_CHAR = models.CharField(db_column='ROOM_CHAR', max_length=32, blank=True,
                                 null=True)  # Field name made lowercase.
    ROOMKOR_CHAR = models.CharField(db_column='ROOMKOR_CHAR', max_length=32, blank=True,
                                    null=True)  # Field name made lowercase.
    TIME_CHAR = models.CharField(db_column='TIME_CHAR', max_length=32, blank=True,
                                 null=True)  # Field name made lowercase.
    DO_CHAR = models.CharField(db_column='DO_CHAR', max_length=16, blank=True, null=True)  # Field name made lowercase.
    DAY_CHAR = models.CharField(db_column='DAY_CHAR', max_length=25, blank=True,
                                null=True)  # Field name made lowercase.
    ACTIVATED_CHAR = models.CharField(db_column='ACTIVATED_CHAR', max_length=20, blank=True,
                                      null=True)  # Field name made lowercase.
    REITERATION_CHAR = models.CharField(db_column='REITERATION_CHAR', max_length=20, blank=True,
                                        null=True)  # Field name made lowercase.
    HOLIDAY_TINYINT = models.IntegerField(db_column='HOLIDAY_TINYINT', blank=True,
                                          null=True)  # Field name made lowercase.
    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'LIGHT_RESERVE_TB'


class LightRecord(models.Model):
    LIGHT_RECORD_PK = models.AutoField(primary_key=True, db_index=True, verbose_name='LIGHT_RECORD_PK')
    DAY_CHAR = models.CharField(max_length=32)
    TIME_CHAR = models.CharField(max_length=32)
    ROOM_CHAR = models.CharField(max_length=64)
    DO_CHAR = models.CharField(max_length=16)
    USER_CHAR = models.CharField(max_length=128)

    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'LIGHT_RECORD_TB'


class FileDefaultPathTb(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    path_name = models.CharField(db_column='PATH_NAME', max_length=45, blank=True, null=True)  # Field name made lowercase.
    public_default_path_char = models.CharField(db_column='PUBLIC_DEFAULT_PATH_CHAR', max_length=200, blank=True, null=True)  # Field name made lowercase.
    private_default_path_char = models.CharField(db_column='PRIVATE_DEFAULT_PATH_CHAR', max_length=200, blank=True, null=True)  # Field name made lowercase.

    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'FILE_DEFAULT_PATH_TB'


class FilePrivate(models.Model):
    ID_PK = models.AutoField(db_column='ID_PK', primary_key=True)  # Field name made lowercase.
    UUID_CHAR = models.CharField(db_column='UUID_CHAR', max_length=200, blank=True,
                                 null=True)  # Field name made lowercase.
    PATH_CHAR = models.CharField(db_column='PATH_CHAR', max_length=200, blank=True,
                                 null=True)  # Field name made lowercase.
    NAME_CHAR = models.CharField(db_column='NAME_CHAR', max_length=100, blank=True,
                                 null=True)  # Field name made lowercase.
    TYPE_CHAR = models.CharField(db_column='TYPE_CHAR', max_length=45, blank=True,
                                 null=True)  # Field name made lowercase.
    SIZE_FLOAT = models.FloatField(db_column='SIZE_FLOAT', blank=True, null=True)  # Field name made lowercase.
    OWNER_CHAR = models.CharField(db_column='OWNER_CHAR', max_length=45, blank=True,
                                  null=True)  # Field name made lowercase.
    LOCATION_CHAR = models.CharField(db_column='LOCATION_CHAR', max_length=200, blank=True,
                                     null=True)  # Field name made lowercase.
    STATE_INT = models.IntegerField(db_column='STATE_INT', blank=True, null=True)  # Field name made lowercase.
    DELETE_STATUS_INT = models.IntegerField(db_column='DELETE_STATUS_INT', blank=True,
                                            null=True)  # Field name made lowercase.

    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'FILE_PRIVATE_TB'


class FilePrivateTrashTb(models.Model):
    id_pk = models.AutoField(db_column='ID_PK', primary_key=True)  # Field name made lowercase.
    uuid_char = models.CharField(db_column='UUID_CHAR', max_length=200, blank=True, null=True)  # Field name made lowercase.
    path_char = models.CharField(db_column='PATH_CHAR', max_length=200, blank=True, null=True)  # Field name made lowercase.
    origin_path_char = models.CharField(db_column='ORIGIN_PATH_CHAR', max_length=200, blank=True, null=True)  # Field name made lowercase.
    type_char = models.CharField(db_column='TYPE_CHAR', max_length=45, blank=True, null=True)  # Field name made lowercase.
    name_char = models.CharField(db_column='NAME_CHAR', max_length=100, blank=True, null=True)  # Field name made lowercase.
    size_float = models.FloatField(db_column='SIZE_FLOAT', blank=True, null=True)  # Field name made lowercase.
    owner_char = models.CharField(db_column='OWNER_CHAR', max_length=45, blank=True, null=True)  # Field name made lowercase.
    location_char = models.CharField(db_column='LOCATION_CHAR', max_length=200, blank=True, null=True)  # Field name made lowercase.
    state_int = models.IntegerField(db_column='STATE_INT', blank=True, null=True)  # Field name made lowercase.

    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'FILE_PRIVATE_TRASH_TB'


class FilePublic(models.Model):
    ID_PK = models.AutoField(db_column='ID_PK', primary_key=True)  # Field name made lowercase.
    UUID_CHAR = models.CharField(db_column='UUID_CHAR', max_length=200, blank=True,
                                 null=True)  # Field name made lowercase.
    PATH_CHAR = models.TextField(db_column='PATH_CHAR', blank=True, null=True)  # Field name made lowercase.
    NAME_CHAR = models.TextField(db_column='NAME_CHAR', blank=True, null=True)  # Field name made lowercase.
    TYPE_CHAR = models.TextField(db_column='TYPE_CHAR', blank=True, null=True)  # Field name made lowercase.
    SIZE_FLOAT = models.FloatField(db_column='SIZE_FLOAT', blank=True, null=True)  # Field name made lowercase.
    LOCATION_CHAR = models.TextField(db_column='LOCATION_CHAR', blank=True, null=True)  # Field name made lowercase.
    STATE_INT = models.IntegerField(db_column='STATE_INT', blank=True, null=True)  # Field name made lowercase.
    DELETE_STATUS_INT = models.IntegerField(db_column='DELETE_STATUS_INT', blank=True,
                                            null=True)  # Field name made lowercase.

    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'FILE_PUBLIC_TB'


class FilePublicTrashTb(models.Model):
    id_pk = models.AutoField(db_column='ID_PK', primary_key=True)  # Field name made lowercase.
    uuid_char = models.CharField(db_column='UUID_CHAR', max_length=200, blank=True,
                                 null=True)  # Field name made lowercase.
    path_char = models.CharField(db_column='PATH_CHAR', max_length=200, blank=True,
                                 null=True)  # Field name made lowercase.
    origin_path_char = models.CharField(db_column='ORIGIN_PATH_CHAR', max_length=200, blank=True,
                                        null=True)  # Field name made lowercase.
    name_char = models.CharField(db_column='NAME_CHAR', max_length=100, blank=True,
                                 null=True)  # Field name made lowercase.
    type_char = models.CharField(db_column='TYPE_CHAR', max_length=45, blank=True,
                                 null=True)  # Field name made lowercase.
    size_float = models.FloatField(db_column='SIZE_FLOAT', blank=True, null=True)  # Field name made lowercase.
    location_char = models.CharField(db_column='LOCATION_CHAR', max_length=200, blank=True,
                                     null=True)  # Field name made lowercase.
    state_int = models.IntegerField(db_column='STATE_INT', blank=True, null=True)  # Field name made lowercase.

    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'FILE_PUBLIC_TRASH_TB'
