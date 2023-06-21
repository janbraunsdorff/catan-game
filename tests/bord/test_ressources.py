import pytest

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
    assert (
        len([x for x, y in board.nodes(data=True) if y["type"] == T.NODE_TYPE.PLAYER])
        == 1
    )
    assert (
        len([x for x, y in board.nodes(data=True) if y["type"] == T.NODE_TYPE.TILE])
        == 4
    )

    board = R.add_ressource_to_player(board, player, T.RESSOURCE.Brick)

    assert len([x for x, y in board.nodes(data=True)]) == (len_before + 1)

    ressource = [
        (x, y) for x, y in board.nodes(data=True) if y["type"] == T.NODE_TYPE.RESSOURCE
    ]

    assert len(ressource) == 1
    assert ressource[0][1]["ressource"] == T.RESSOURCE.Brick


def test_add_multible_ressource():
    player = TestPlayer(T.COLOR.BLUE)
    board = BoardBuilder().create_board_of_size([1, 2, 1]).with_player(player).build()

    len_before = len([x for x, y in board.nodes(data=True)])
    assert (
        len([x for x, y in board.nodes(data=True) if y["type"] == T.NODE_TYPE.PLAYER])
        == 1
    )
    assert (
        len([x for x, y in board.nodes(data=True) if y["type"] == T.NODE_TYPE.TILE])
        == 4
    )

    board = R.add_ressources_to_player(
        board, player, [T.RESSOURCE.Brick, T.RESSOURCE.Wool]
    )

    assert len([x for x, y in board.nodes(data=True)]) == (len_before + 2)

    ressource = [
        (x, y) for x, y in board.nodes(data=True) if y["type"] == T.NODE_TYPE.RESSOURCE
    ]

    assert len(ressource) == 2
    assert T.RESSOURCE.Brick in [ressource[x][1]["ressource"] for x in range(2)]
    assert T.RESSOURCE.Wool in [ressource[x][1]["ressource"] for x in range(2)]


def test_add_one_ressource_for_two_player():
    player_b = TestPlayer(T.COLOR.ORANGE)
    player_a = TestPlayer(T.COLOR.BLUE)
    board = (
        BoardBuilder()
        .create_board_of_size([1, 2, 1])
        .with_player(player_b)
        .with_player(player_a)
        .build()
    )

    len_before = len([x for x, y in board.nodes(data=True)])
    assert (
        len([x for x, y in board.nodes(data=True) if y["type"] == T.NODE_TYPE.PLAYER])
        == 2
    )
    assert (
        len([x for x, y in board.nodes(data=True) if y["type"] == T.NODE_TYPE.TILE])
        == 4
    )

    board = R.add_ressource_to_player(board, player_a, T.RESSOURCE.Brick)
    board = R.add_ressource_to_player(board, player_b, T.RESSOURCE.Lumber)

    assert len([x for x, y in board.nodes(data=True)]) == (len_before + 2)

    resources = R.get_ressources_of_player_list(board, player_a)
    assert len(resources) == 1
    assert resources[0] == T.RESSOURCE.Brick

    resources = R.get_ressources_of_player_list(board, player_b)
    assert len(resources) == 1
    assert resources[0] == T.RESSOURCE.Lumber


def test_get_ressources_of_player_list():
    player = TestPlayer(T.COLOR.BLUE)
    board = BoardBuilder().create_board_of_size([1, 2, 1]).with_player(player).build()

    board = R.add_ressource_to_player(board, player, T.RESSOURCE.Brick)

    resources = R.get_ressources_of_player_list(board, player)

    assert len(resources) == 1
    assert resources[0] == T.RESSOURCE.Brick


def test_get_ressources_of_player_list_two():
    player = TestPlayer(T.COLOR.BLUE)
    board = BoardBuilder().create_board_of_size([1, 2, 1]).with_player(player).build()

    board = R.add_ressource_to_player(board, player, T.RESSOURCE.Brick)
    board = R.add_ressource_to_player(board, player, T.RESSOURCE.Brick)

    resources = R.get_ressources_of_player_list(board, player)

    assert len(resources) == 2
    assert resources[0] == T.RESSOURCE.Brick
    assert resources[1] == T.RESSOURCE.Brick


def test_remove_ressource_from_player():
    player = TestPlayer(T.COLOR.BLUE)
    board = BoardBuilder().create_board_of_size([1, 2, 1]).with_player(player).build()

    len_before = len([x for x, y in board.nodes(data=True)])

    board = R.add_ressource_to_player(board, player, T.RESSOURCE.Brick)
    board = R.remove_ressource_from_player(board, player, T.RESSOURCE.Brick)

    assert len([x for x, y in board.nodes(data=True)]) == len_before
    assert len(R.get_ressources_of_player_list(board, player)) == 0


def test_remove_ressource_from_player_missing_ressource():
    player = TestPlayer(T.COLOR.BLUE)
    board = BoardBuilder().create_board_of_size([1, 2, 1]).with_player(player).build()

    len_before = len([x for x, y in board.nodes(data=True)])

    with pytest.raises(ValueError) as e:
        board = R.remove_ressource_from_player(board, player, T.RESSOURCE.Brick)

    assert e.value.args[0] == "Ressource not available to remove"

    assert len([x for x, y in board.nodes(data=True)]) == len_before
    assert len(R.get_ressources_of_player_list(board, player)) == 0
