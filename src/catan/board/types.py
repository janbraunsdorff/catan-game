from enum import Enum
from typing import Dict, List, Tuple

from networkx import Graph


class TILE_TYPE(Enum):
    Missing = 0
    Mountains = 1
    Hills = 2
    Forest = 3
    Fields = 4
    Pasture = 5
    Desert = 6


class PORT(Enum):
    Any = 1
    Grain = 2
    Ore = 3
    Wool = 4
    Brick = 5
    Lumber = 6


class RESSOURCE(Enum):
    Grain = 2
    Ore = 3
    Wool = 4
    Brick = 5
    Lumber = 6


class ROBBER(Enum):
    Normal = 1
    See = 3


class CONNECTION(Enum):
    Missing = 1
    Road = 2
    Boat = 3


class BUILDING(Enum):
    MISSING = "missing"
    SETTELMENT = "settelement"
    CITY = "city"


Coor = Tuple[float, float]
Board = Graph


class COLOR(Enum):
    RED = "red"
    BLUE = "blue"
    WHITE = "white"
    ORANGE = "orange"


class EDGE_TYPE(Enum):
    PRODUCE_TO = "produce_to"
    PORT_TO = "port_to"
    STREET = "street"
    RESSOURCE_OWNERSHIP = "resource_ownership"
    SETTELMENT_OWNERSHIP = "settelment_ownership"
    CITY_ONWERSHIP = "city_ownership"


class NODE_TYPE(Enum):
    PLAYER = "player"
    TILE = "tile"
    BUILDING = "building"
    RESSOURCE = "resource"
    PORT = "port"


class PORT_TYPE(Enum):
    PORT_ANY = "port_3_any"
    PORT_WOOL = "port_wool"
    PORT_WOOD = "port_wood"
    PORT_GRAIN = "port_grain"
    PORT_ORE = "port_ore"
    PORT_BRICK = "port_brick"
