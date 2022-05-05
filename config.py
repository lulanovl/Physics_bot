from enum import Enum


db_file = "database.vdb"

class States(Enum):
    """
    Мы используем БД Vedis, в которой хранимые значения всегда строки,
    поэтому и тут будем использовать тоже строки (str)
    """
    START = "0"
    NAME = '1'
    CHOOSE = '2'
