from unittest.mock import patch

import catan.board.types as T
from catan.board.developments import trade_developement
from catan.board.graph import BoardBuilder
from catan.board.place import add_building
from catan.board.victory_points import (
    count_city_points,
    count_development_cards,
    count_settelment_points,
    highest_knights,
)


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


def test_no_knights(player_blue):
    board = (
        BoardBuilder().create_board_of_size([1, 2, 1]).with_player(player_blue).build()
    )

    assert highest_knights(board, player_blue) == 0


@patch("catan.board.developments.check_cards")
@patch("catan.board.developments.check_ressources_for_development")
@patch("catan.board.developments.remove_ressource_from_player")
def test_one_knights(check_cards, check_ressource, remove, player_blue):
    board = (
        BoardBuilder().create_board_of_size([1, 2, 1]).with_player(player_blue).build()
    )

    remove = lambda x: True

    remove.return_value = True

    trade_developement(board, player_blue, T.DEVELOPMENT_CARDS.KNIGHT)

    assert highest_knights(board, player_blue) == 0


@patch("catan.board.developments.remove_ressource_from_player")
@patch("catan.board.developments.check_ressources_for_development")
@patch("catan.board.developments.check_cards")
def test_two_knights(remove, check, check1, player_blue):
    board = (
        BoardBuilder().create_board_of_size([1, 2, 1]).with_player(player_blue).build()
    )

    remove.return_value = True

    trade_developement(board, player_blue, T.DEVELOPMENT_CARDS.KNIGHT)
    trade_developement(board, player_blue, T.DEVELOPMENT_CARDS.KNIGHT)

    assert highest_knights(board, player_blue) == 0


@patch("catan.board.developments.remove_ressource_from_player")
@patch("catan.board.developments.check_ressources_for_development")
@patch("catan.board.developments.check_cards")
def test_three_knights(remove, check, check1, player_blue):
    board = (
        BoardBuilder().create_board_of_size([1, 2, 1]).with_player(player_blue).build()
    )
    remove.return_value = True

    trade_developement(board, player_blue, T.DEVELOPMENT_CARDS.KNIGHT)
    trade_developement(board, player_blue, T.DEVELOPMENT_CARDS.KNIGHT)
    trade_developement(board, player_blue, T.DEVELOPMENT_CARDS.KNIGHT)

    assert highest_knights(board, player_blue) == 2


@patch("catan.board.developments.remove_ressource_from_player")
@patch("catan.board.developments.check_ressources_for_development")
@patch("catan.board.developments.check_cards")
def test_three_knights_other_too(remove, check, check1, player_blue, player_red):
    board = (
        BoardBuilder()
        .create_board_of_size([1, 2, 1])
        .with_player(player_blue)
        .with_player(player_red)
        .build()
    )
    remove.return_value = True

    trade_developement(board, player_blue, T.DEVELOPMENT_CARDS.KNIGHT)
    trade_developement(board, player_blue, T.DEVELOPMENT_CARDS.KNIGHT)
    trade_developement(board, player_blue, T.DEVELOPMENT_CARDS.KNIGHT)

    trade_developement(board, player_red, T.DEVELOPMENT_CARDS.KNIGHT)
    trade_developement(board, player_red, T.DEVELOPMENT_CARDS.KNIGHT)
    trade_developement(board, player_red, T.DEVELOPMENT_CARDS.KNIGHT)

    assert highest_knights(board, player_blue) == 0


@patch("catan.board.developments.remove_ressource_from_player")
@patch("catan.board.developments.check_ressources_for_development")
@patch("catan.board.developments.check_cards")
def test_three_knights_other_more(remove, check, check1, player_blue, player_red):
    board = (
        BoardBuilder()
        .create_board_of_size([1, 2, 1])
        .with_player(player_blue)
        .with_player(player_red)
        .build()
    )
    remove.return_value = True

    trade_developement(board, player_blue, T.DEVELOPMENT_CARDS.KNIGHT)
    trade_developement(board, player_blue, T.DEVELOPMENT_CARDS.KNIGHT)
    trade_developement(board, player_blue, T.DEVELOPMENT_CARDS.KNIGHT)

    trade_developement(board, player_red, T.DEVELOPMENT_CARDS.KNIGHT)
    trade_developement(board, player_red, T.DEVELOPMENT_CARDS.KNIGHT)
    trade_developement(board, player_red, T.DEVELOPMENT_CARDS.KNIGHT)
    trade_developement(board, player_red, T.DEVELOPMENT_CARDS.KNIGHT)

    assert highest_knights(board, player_blue) == 0


@patch("catan.board.developments.remove_ressource_from_player")
@patch("catan.board.developments.check_ressources_for_development")
@patch("catan.board.developments.check_cards")
def test_four_knights_other_threee(remove, check, check1, player_blue, player_red):
    board = (
        BoardBuilder()
        .create_board_of_size([1, 2, 1])
        .with_player(player_blue)
        .with_player(player_red)
        .build()
    )
    remove.return_value = True

    trade_developement(board, player_blue, T.DEVELOPMENT_CARDS.KNIGHT)
    trade_developement(board, player_blue, T.DEVELOPMENT_CARDS.KNIGHT)
    trade_developement(board, player_blue, T.DEVELOPMENT_CARDS.KNIGHT)
    trade_developement(board, player_blue, T.DEVELOPMENT_CARDS.KNIGHT)

    trade_developement(board, player_red, T.DEVELOPMENT_CARDS.KNIGHT)
    trade_developement(board, player_red, T.DEVELOPMENT_CARDS.KNIGHT)
    trade_developement(board, player_red, T.DEVELOPMENT_CARDS.KNIGHT)

    assert highest_knights(board, player_blue) == 2


@patch("catan.board.developments.remove_ressource_from_player")
@patch("catan.board.developments.check_ressources_for_development")
@patch("catan.board.developments.check_cards")
def test_on_victory_development(remove, check, check1, player_blue, player_red):
    board = (
        BoardBuilder()
        .create_board_of_size([1, 2, 1])
        .with_player(player_blue)
        .with_player(player_red)
        .build()
    )
    remove.return_value = True

    assert count_development_cards(board, player_blue) == 0


@patch("catan.board.developments.remove_ressource_from_player")
@patch("catan.board.developments.check_ressources_for_development")
@patch("catan.board.developments.check_cards")
def test_one_victory_development(remove, check, check1, player_blue, player_red):
    board = (
        BoardBuilder()
        .create_board_of_size([1, 2, 1])
        .with_player(player_blue)
        .with_player(player_red)
        .build()
    )
    remove.return_value = True

    trade_developement(board, player_blue, T.DEVELOPMENT_CARDS.VICTORY_POINTS)

    assert count_development_cards(board, player_blue) == 1


@patch("catan.board.developments.remove_ressource_from_player")
@patch("catan.board.developments.check_ressources_for_development")
@patch("catan.board.developments.check_cards")
def test_two_victory_development(remove, check, check1, player_blue, player_red):
    board = (
        BoardBuilder()
        .create_board_of_size([1, 2, 1])
        .with_player(player_blue)
        .with_player(player_red)
        .build()
    )
    remove.return_value = True

    trade_developement(board, player_blue, T.DEVELOPMENT_CARDS.VICTORY_POINTS)
    trade_developement(board, player_blue, T.DEVELOPMENT_CARDS.VICTORY_POINTS)

    assert count_development_cards(board, player_blue) == 2


@patch("catan.board.developments.remove_ressource_from_player")
@patch("catan.board.developments.check_ressources_for_development")
@patch("catan.board.developments.check_cards")
def test_two_victory_development_one_other(
    remove, check, check1, player_blue, player_red
):
    board = (
        BoardBuilder()
        .create_board_of_size([1, 2, 1])
        .with_player(player_blue)
        .with_player(player_red)
        .build()
    )
    remove.return_value = True

    trade_developement(board, player_blue, T.DEVELOPMENT_CARDS.VICTORY_POINTS)
    trade_developement(board, player_blue, T.DEVELOPMENT_CARDS.VICTORY_POINTS)

    trade_developement(board, player_red, T.DEVELOPMENT_CARDS.VICTORY_POINTS)

    assert count_development_cards(board, player_blue) == 2
