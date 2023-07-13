import pytest

import catan.board.ressources as R
import catan.board.types as T
from catan.board.graph import BoardBuilder
from catan.player import Player


def test_add_one_ressource(player_blue):
    board = (
        BoardBuilder().create_board_of_size([1, 2, 1]).with_player(player_blue).build()
    )

    len_before = len([x for x, y in board.nodes(data=True)])
    assert (
        len([x for x, y in board.nodes(data=True) if y["type"] == T.NODE_TYPE.PLAYER])
        == 1
    )
    assert (
        len([x for x, y in board.nodes(data=True) if y["type"] == T.NODE_TYPE.TILE])
        == 4
    )

    board = R.add_ressource_to_player(board, player_blue, T.RESSOURCE.Brick)

    assert len([x for x, y in board.nodes(data=True)]) == (len_before + 1)

    ressource = [
        (x, y) for x, y in board.nodes(data=True) if y["type"] == T.NODE_TYPE.RESSOURCE
    ]

    assert len(ressource) == 1
    assert ressource[0][1]["ressource"] == T.RESSOURCE.Brick


def test_add_multible_ressource(player_blue):
    board = (
        BoardBuilder().create_board_of_size([1, 2, 1]).with_player(player_blue).build()
    )

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
        board, player_blue, [T.RESSOURCE.Brick, T.RESSOURCE.Wool]
    )

    assert len([x for x, y in board.nodes(data=True)]) == (len_before + 2)

    ressource = [
        (x, y) for x, y in board.nodes(data=True) if y["type"] == T.NODE_TYPE.RESSOURCE
    ]

    assert len(ressource) == 2
    assert T.RESSOURCE.Brick in [ressource[x][1]["ressource"] for x in range(2)]
    assert T.RESSOURCE.Wool in [ressource[x][1]["ressource"] for x in range(2)]


def test_add_one_ressource_for_two_player(player_blue, player_red):
    board = (
        BoardBuilder()
        .create_board_of_size([1, 2, 1])
        .with_player(player_blue)
        .with_player(player_red)
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

    board = R.add_ressource_to_player(board, player_red, T.RESSOURCE.Brick)
    board = R.add_ressource_to_player(board, player_blue, T.RESSOURCE.Lumber)

    assert len([x for x, y in board.nodes(data=True)]) == (len_before + 2)

    resources = R.get_ressources_of_player_list(board, player_red)
    assert len(resources) == 1
    assert resources[0] == T.RESSOURCE.Brick

    resources = R.get_ressources_of_player_list(board, player_blue)
    assert len(resources) == 1
    assert resources[0] == T.RESSOURCE.Lumber


def test_get_ressources_of_player_list(player_red):
    board = (
        BoardBuilder().create_board_of_size([1, 2, 1]).with_player(player_red).build()
    )

    board = R.add_ressource_to_player(board, player_red, T.RESSOURCE.Brick)

    resources = R.get_ressources_of_player_list(board, player_red)

    assert len(resources) == 1
    assert resources[0] == T.RESSOURCE.Brick


def test_get_ressources_of_player_list_two(player_red):
    board = (
        BoardBuilder().create_board_of_size([1, 2, 1]).with_player(player_red).build()
    )

    board = R.add_ressource_to_player(board, player_red, T.RESSOURCE.Brick)
    board = R.add_ressource_to_player(board, player_red, T.RESSOURCE.Brick)

    resources = R.get_ressources_of_player_list(board, player_red)

    assert len(resources) == 2
    assert resources[0] == T.RESSOURCE.Brick
    assert resources[1] == T.RESSOURCE.Brick


def test_remove_ressource_from_player(player_red):
    board = (
        BoardBuilder().create_board_of_size([1, 2, 1]).with_player(player_red).build()
    )

    len_before = len([x for x, y in board.nodes(data=True)])

    board = R.add_ressource_to_player(board, player_red, T.RESSOURCE.Brick)
    board = R.remove_ressource_from_player(board, player_red, T.RESSOURCE.Brick)

    assert len([x for x, y in board.nodes(data=True)]) == len_before
    assert len(R.get_ressources_of_player_list(board, player_red)) == 0


def test_remove_ressource_from_player_missing_ressource(player_red):
    board = (
        BoardBuilder().create_board_of_size([1, 2, 1]).with_player(player_red).build()
    )

    len_before = len([x for x, y in board.nodes(data=True)])

    with pytest.raises(ValueError) as e:
        board = R.remove_ressource_from_player(board, player_red, T.RESSOURCE.Brick)

    assert e.value.args[0] == "Ressource not available to remove"

    assert len([x for x, y in board.nodes(data=True)]) == len_before
    assert len(R.get_ressources_of_player_list(board, player_red)) == 0
