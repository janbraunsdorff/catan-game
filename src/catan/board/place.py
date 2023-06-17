from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from catan.player import Player


import catan.board.types as T


class PlaceNotAllowed(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def add_building(
    G: T.Board,
    player: Player,
    index: int,
    building: T.BUILDINGS,
    founding: bool = False,
) -> None:
    # not more than 4 settelment already exits
    # not more than 3 cities already exits
    # no exiting buiding from other players
    # if city, settelment must be placed first
    # player must own ressources if not founding
    # next bulding must be at least corssroads away

    # update node
    # add between node an player
    raise NotImplementedError()


def add_connection(G: T.Board, player: Player, index: int, building: T.ROADS) -> None:
    raise NotImplementedError()
