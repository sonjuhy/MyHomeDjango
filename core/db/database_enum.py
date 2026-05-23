from enum import Enum


class Default(Enum):
    GET_LIGHT_LIST = "LightList"
    GET_RESERVE_LIST = "ReserveList"
    SAVE_LIGHT_RECORD = "LightRecordInsert"
    UPDATE_LIGHT = "LightUpdate"
    UPDATE_CONN_STATUS = "ConnectUpdate"
    UPDATE_RESERVE = "ReserveUpdate"
    UPDATE_RESERVE_ACTIVATE = "ReserveActivateUpdate"


class File(Enum):
    MOVE_PUBLIC = "movePublic"
    RESTORE_PUBLIC = "restorePublic"
    DELETE_PUBLIC = "deletePublic"
    MOVE_PRIVATE = "movePrivate"
    RESTORE_PRIVATE = "restorePrivate"
    DELETE_PRIVATE = "deletePrivate"
    DELETE_COMMUNAL = "delete"
    GET_DEFAULT_PATH = "default"


class FileDataType(Enum):
    TYPE = "type"
    UUID = "uuid"
    DESTINATION = "destination"
