from enum import Enum
from typing import Dict, List, Tuple

from networkx import Graph


class NODE_TYPES(Enum):
    Missing = 0
    Mountains = 1
    Hills = 2
    Forest = 3
    Fields = 4
    Pasture = 5
    Desert = 6


class PORTS(Enum):
    Any = 1
    Grain = 2
    Ore = 3
    Wool = 4
    Brick = 5
    Lumber = 6


class RESSOURCES(Enum):
    Grain = 2
    Ore = 3
    Wool = 4
    Brick = 5
    Lumber = 6


class ROBBERS(Enum):
    Normal = 1
    See = 3


class ROADS(Enum):
    Missing = 1
    Placed = 2
    Boat = 3


class BUILDINGS(Enum):
    Missing = 1
    Settelment = 2
    City = 3


Coor = Tuple[float, float]
Board = Graph


class COLOR(Enum):
    RED = 1
    BLUE = 2
    WHITE = 3
    ORANGE = 4
