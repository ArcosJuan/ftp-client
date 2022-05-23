from enum import IntEnum
from enum import auto

class FTPOption(IntEnum):
    CHANGE_DIRECTORY = auto()
    LIST_DIRECTORY = auto()
    MAKE_DIRECTORY = auto()
    REMOVE_DIRECTORY = auto()
    SIZE = auto()
    RENAME = auto()
    DELETE = auto()


    def __str__(self) -> str:
        """ Returns a string which represents the option.
        """

        return self.name.replace('_', ' ').capitalize()
