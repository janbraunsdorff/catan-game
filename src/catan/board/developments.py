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
