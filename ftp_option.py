from enum import IntEnum
from enum import auto

class FTPOption(IntEnum):
    CHANGE_DIRECTORY = auto()
    LIST_DIRECTORY = auto()
    MAKE_DIRECTORY = auto()
    REMOVE_DIRECTORY = auto()
    FILE_SIZE = auto()
    RENAME_FILE = auto()
    DELETE_FILE = auto()
    DOWNLOAD_FILE = auto()
    UPLOAD_FILE = auto()


    def __str__(self) -> str:
        """ Returns a string which represents the option.
        """

        return self.name.replace('_', ' ').capitalize()
