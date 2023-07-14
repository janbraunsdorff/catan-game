from unittest.mock import patch

import catan.board.types as T
from catan.board.graph import BoardBuilder
from catan.board.place import add_building
from catan.board.victory_points import count_city_points, count_settelment_points


def test_count_settelement_1(player_blue):
    board = (
        BoardBuilder().create_board_of_size([1, 2, 1]).with_player(player_blue).build()
    )

    add_building(board, player_blue, 100, T.BUILDING.SETTELMENT, founding=True)

    assert count_settelment_points(board, player_blue) == 1


@patch("catan.board.place.remove_ressource_from_player")
@patch("catan.board.place.check_building")
def test_count_settelement_2(remoce, place, player_blue):
    board = (
        BoardBuilder().create_board_of_size([1, 2, 1]).with_player(player_blue).build()
    )

    add_building(board, player_blue, 100, T.BUILDING.SETTELMENT, founding=True)
    add_building(board, player_blue, 106, T.BUILDING.SETTELMENT, founding=True)

    add_building(board, player_blue, 109, T.BUILDING.CITY)

    assert count_settelment_points(board, player_blue) == 2


@patch("catan.board.place.remove_ressource_from_player")
@patch("catan.board.place.check_building")
def test_count_city_1(remoce, place, player_blue):
    board = (
        BoardBuilder().create_board_of_size([1, 2, 1]).with_player(player_blue).build()
    )

    add_building(board, player_blue, 106, T.BUILDING.SETTELMENT, founding=True)

    add_building(board, player_blue, 109, T.BUILDING.CITY)

    assert count_city_points(board, player_blue) == 2


@patch("catan.board.place.remove_ressource_from_player")
@patch("catan.board.place.check_building")
def test_count_city_2(remoce, place, player_blue):
    board = (
        BoardBuilder().create_board_of_size([1, 2, 1]).with_player(player_blue).build()
    )

    add_building(board, player_blue, 106, T.BUILDING.SETTELMENT, founding=True)

    add_building(board, player_blue, 109, T.BUILDING.CITY)
    add_building(board, player_blue, 108, T.BUILDING.CITY)

    assert count_city_points(board, player_blue) == 4
