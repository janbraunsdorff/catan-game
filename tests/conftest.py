import pytest

import catan.board.types as T
from catan.player import Player


class DemoPlayer(Player):
    def __init__(self, color: T.COLOR) -> None:
        super().__init__(color)


@pytest.fixture()
def player_red():
    return DemoPlayer(T.COLOR.RED)


@pytest.fixture()
def player_blue():
    return DemoPlayer(T.COLOR.BLUE)
