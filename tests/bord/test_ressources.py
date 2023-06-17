import catan.board.ressources as R
import catan.board.types as T
from catan.board.graph import BoardBuilder
from catan.player import Player


class TestPlayer(Player):
    def __init__(self, color: T.COLOR) -> None:
        super().__init__(color)


def test_add_one_ressource():
    player = TestPlayer(T.COLOR.BLUE)
    board = BoardBuilder().create_board_of_size([1, 2, 1]).with_player(player).build()

    len_before = len([x for x, y in board.nodes(data=True)])
    assert len([x for x, y in board.nodes(data=True) if y["type"] == "player"]) == 1
    assert len([x for x, y in board.nodes(data=True) if y["type"] == "tile"]) == 4

    board = R.add_ressource_to_player(board, player, T.RESSOURCES.Brick)

    assert len([x for x, y in board.nodes(data=True)]) == (len_before + 1)

    ressource = [(x, y) for x, y in board.nodes(data=True) if y["type"] == "ressource"]

    assert len(ressource) == 1
    assert ressource[0][1]["ressource"] == T.RESSOURCES.Brick


def test_get_ressources_of_player_list():
    player = TestPlayer(T.COLOR.BLUE)
    board = BoardBuilder().create_board_of_size([1, 2, 1]).with_player(player).build()

    board = R.add_ressource_to_player(board, player, T.RESSOURCES.Brick)

    resources = R.get_ressources_of_player_list(board, player)

    assert len(resources) == 1
    assert resources[0] == T.RESSOURCES.Brick
