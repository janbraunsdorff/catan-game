import catan.board.types as T
from catan.player import Player


class HumanPlayer(Player):
    def __init__(self, color: T.COLOR) -> None:
        super().__init__(color=color)
