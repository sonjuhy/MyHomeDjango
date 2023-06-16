from django.db import models

# Create your models here.


class RoomLight(models.Model):
    LIGHT_ROOM_PK = models.CharField(max_length=20, primary_key=True)
    STATE_CHAR = models.CharField(max_length=10)
    ROOMKOR_CHAR = models.CharField(max_length=20)
    CATEGORY_CHAR = models.CharField(max_length=100)
    CONNECT_CHAR = models.CharField(max_length=25)
    
    class Meta:
        managed = False
        db_table = 'LIGHT_ROOM_TB'


class Reserve(models.Model):
    LIGHT_RESERVE_PK = models.IntegerField(primary_key=True)
    NAME_CHAR = models.CharField(max_length=32)
    NAMEKOR_CHAR = models.CharField(max_length=32)
    TIME_CHAR = models.CharField(max_length=32)
    ROOM_CHAR = models.CharField(max_length=32)
    DO_CHAR = models.CharField(max_length=16)
    DAY_CHAR = models.CharField(max_length=25)
    ACTIVATED_CHAR = models.CharField(max_length=20)
    REITERATION_CHAR = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'LIGHT_RESERVE_TB'


class LightRecord(models.Model):
    LIGHT_RECORD_ID = models.AutoField(primary_key=True, db_index=True, verbose_name='LIGHT_RECORD_PK')
    DAY_CHAR = models.CharField(max_length=32)
    TIME_CHAR = models.CharField(max_length=32)
    ROOM_CHAR = models.CharField(max_length=64)
    DO_CHAR = models.CharField(max_length=16)
    USER_CHAR = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'LIGHT_RECORD_TB'


class FilePrivate(models.Model):
    UUID_PK = models.CharField(primary_key=True, db_index=False, verbose_name='UUID_PK', max_length=200)
    PATH_CHAR = models.CharField(max_length=200)
    NAME_CHAR = models.CharField(max_length=100)
    TYPE_CHAR = models.CharField(max_length=45)
    SIZE_FLOAT = models.FloatField()
    OWNER_CHAR = models.CharField(max_length=45)
    LOCATION_CHAR = models.CharField(max_length=200)
    STATE_INT = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'FILE_PRIVATE_TB'


class FilePrivateTrash(models.Model):
    UUID_PK = models.CharField(primary_key=True, db_index=False, verbose_name='UUID_PK', max_length=200)
    PATH_CHAR = models.CharField(max_length=200)
    NAME_CHAR = models.CharField(max_length=100)
    TYPE_CHAR = models.CharField(max_length=45)
    SIZE_FLOAT = models.FloatField()
    OWNER_CHAR = models.CharField(max_length=45)
    LOCATION_CHAR = models.CharField(max_length=200)
    STATE_INT = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'FILE_PRIVATE_TRASH_TB'


class FilePublic(models.Model):
    UUID_PK = models.CharField(primary_key=True, db_index=False, verbose_name='UUID_PK', max_length=200)
    PATH_CHAR = models.CharField(max_length=200)
    NAME_CHAR = models.CharField(max_length=100)
    TYPE_CHAR = models.CharField(max_length=45)
    SIZE_FLOAT = models.FloatField()
    LOCATION_CHAR = models.CharField(max_length=200)
    STATE_INT = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'FILE_PUBLIC_TB'


class FilePublicTrash(models.Model):
    UUID_PK = models.CharField(primary_key=True, db_index=False, verbose_name='UUID_PK', max_length=200)
    PATH_CHAR = models.CharField(max_length=200)
    NAME_CHAR = models.CharField(max_length=100)
    TYPE_CHAR = models.CharField(max_length=45)
    SIZE_FLOAT = models.FloatField()
    LOCATION_CHAR = models.CharField(max_length=200)
    STATE_INT = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'FILE_PUBLIC_TRASH_TB'
