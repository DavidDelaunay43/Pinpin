from enum import Enum, auto


class Root(Enum):
    
    DEST = auto()
    SOURCE = auto()


class State(Enum):
    
    EDIT = auto()
    PUBLISH = auto()
