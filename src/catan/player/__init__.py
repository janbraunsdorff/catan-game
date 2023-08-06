from abc import ABC
from typing import List

import catan.board.types as T
from catan.board.place import add_building, add_connection
from catan.board.ressources import get_ressources_of_player_list, player_has_port


class Player(ABC):
    def __init__(self, color: T.COLOR) -> None:
        super().__init__()
        self._color: T.COLOR = color

    @property
    def color(self) -> str:
        return self._color.value

    def get_ports(self, G: T.Board) -> List[T.PORT]:
        ports = []
        for p in T.PORT:
            if player_has_port(G, self, p):
                ports.append(p)
        return ports

    def get_ressources(self, G: T.Board) -> List[T.RESSOURCE]:
        return get_ressources_of_player_list(G, self)

    def place_settelment(self, G: T.Board, index: int):
        add_building(G, self, index, T.BUILDING.SETTELMENT)

    def place_city(self, G: T.Board, index: int):
        add_building(G, self, index, T.BUILDING.CITY)

    def place_street(self, G: T.Board, node_u: int, node_v: int):
        add_connection(G, self, node_u, node_v, T.CONNECTION.ROAD)
