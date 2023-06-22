from abc import ABC

import catan.board.types as T
from catan.board.place import add_building, add_connection


class Player(ABC):
    def __init__(self, color: T.COLOR) -> None:
        super().__init__()
        self._color: T.COLOR = color

    @property
    def color(self) -> T.COLOR:
        return self._color

    def place_settelment(self, G: T.Board, index: int):
        add_building(G, self, index, T.BUILDING.SETTELMENT)

    def place_city(self, G: T.Board, index: int):
        add_building(G, self, index, T.BUILDING.City)

    def place_street(self, G: T.Board, index: int):
        add_connection(G, self, index, T.CONNECTION.Road)
