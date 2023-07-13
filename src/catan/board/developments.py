from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from catan.player import Player  # pragma: no cover


from uuid import uuid4

import catan.board.types as T  # pragma: no cover


def add_development_cards(G: T.Board) -> T.Board:
    for _ in range(14):
        G.add_node(
            str(uuid4()),
            type=T.NODE_TYPE.DEVELOPEMENT,
            development_type=T.DEVELOPMENT_CARDS.KNIGHT,
        )

    for _ in range(5):
        G.add_node(
            str(uuid4()),
            type=T.NODE_TYPE.DEVELOPEMENT,
            development_type=T.DEVELOPMENT_CARDS.VICTORY_POINTS,
        )

    for _ in range(2):
        G.add_node(
            str(uuid4()),
            type=T.NODE_TYPE.DEVELOPEMENT,
            development_type=T.DEVELOPMENT_CARDS.STREET_BUILDING,
        )
    for _ in range(2):
        G.add_node(
            str(uuid4()),
            type=T.NODE_TYPE.DEVELOPEMENT,
            development_type=T.DEVELOPMENT_CARDS.INVENTION,
        )
    for _ in range(2):
        G.add_node(
            str(uuid4()),
            type=T.NODE_TYPE.DEVELOPEMENT,
            development_type=T.DEVELOPMENT_CARDS.MONOPOL,
        )

    return G


def trade_developement(G: T.Board, player: Player, card: T.DEVELOPMENT_CARDS):
    # check ressources
    # if card  = None -> random
    # else check if card is aviable -> add
    pass
