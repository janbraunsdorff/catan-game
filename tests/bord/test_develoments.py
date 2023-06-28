from uuid import uuid4

import pytest

import catan.board.ressources as R
import catan.board.types as T
from catan.board.graph import BoardBuilder
from catan.player import Player


class TestPlayer(Player):
    def __init__(self, color: T.COLOR) -> None:
        super().__init__(color)


@pytest.mark.parametrize(
    "t,length",
    [
        (T.DEVELOPMENT_CARDS.MONOPOL, 2),
        (T.DEVELOPMENT_CARDS.STREET_BUILDING, 2),
        (T.DEVELOPMENT_CARDS.INVENTION, 2),
        (T.DEVELOPMENT_CARDS.KNIGHT, 14),
        (T.DEVELOPMENT_CARDS.VICTORY_POINTS, 5),
    ],
)
def test_add_developent(t, length):
    player = TestPlayer(T.COLOR.BLUE)

    G = BoardBuilder().create_board_of_size([1]).with_player(player).build()

    assert (
        len(
            [
                x
                for x, y in G.nodes(data=True)
                if y["type"] == T.NODE_TYPE.DEVELOPEMENT and y["development_type"] == t
            ]
        )
        == length
    )
