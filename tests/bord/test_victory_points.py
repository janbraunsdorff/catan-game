from unittest.mock import patch

import networkx as nx

import catan.board.types as T
from catan.board.developments import trade_developement
from catan.board.graph import BoardBuilder
from catan.board.place import add_building, add_connection
from catan.board.victory_points import (
    count_city_points,
    count_connected_nodes,
    count_development_cards,
    count_nodes_of_player,
    count_settelment_points,
    get_longest_road_victory_points,
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


def test_connected_streets_one():
    G = nx.Graph()
    G.add_edge(1, 2)

    assert count_connected_nodes(G, []) == 1


def test_connected_streets_zero():
    G = nx.Graph()

    assert count_connected_nodes(G, []) == 0


def test_connected_streets_three():
    G = nx.Graph()

    G.add_edge(1, 2)
    G.add_edge(2, 3)
    G.add_edge(3, 4)

    assert count_connected_nodes(G, []) == 3


def test_connected_streets_foure_dist():
    G = nx.Graph()

    G.add_edge(1, 2)
    G.add_edge(1, 6)

    G.add_edge(2, 3)
    G.add_edge(3, 4)
    G.add_edge(4, 5)

    assert count_connected_nodes(G, []) == 5


def test_connected_streets_foure_short_cut():
    G = nx.Graph()

    G.add_edge(1, 2)
    G.add_edge(1, 4)

    G.add_edge(2, 3)
    G.add_edge(3, 4)
    G.add_edge(4, 5)
    G.add_edge(1, 6)

    assert count_connected_nodes(G, []) == 5


def test_connected_streets_foure_cicle():
    G = nx.Graph()

    G.add_edge(1, 2)
    G.add_edge(2, 3)
    G.add_edge(3, 4)
    G.add_edge(4, 5)
    G.add_edge(5, 6)
    G.add_edge(6, 1)

    assert count_connected_nodes(G, []) == 6


def test_connected_streets_foure_advanced():
    G = nx.Graph()

    G.add_edge(1, 3)
    G.add_edge(3, 5)
    G.add_edge(4, 6)
    G.add_edge(4, 7)
    G.add_edge(5, 8)
    G.add_edge(5, 7)
    G.add_edge(6, 9)
    G.add_edge(7, 10)
    G.add_edge(8, 11)
    G.add_edge(9, 12)
    G.add_edge(10, 12)
    G.add_edge(10, 13)
    G.add_edge(13, 11)

    assert count_connected_nodes(G, []) == 12


def test_connected_two_circulars():
    G = nx.Graph()

    G.add_edge(1, 2)
    G.add_edge(2, 3)
    G.add_edge(3, 4)
    G.add_edge(4, 5)
    G.add_edge(5, 6)
    G.add_edge(6, 3)
    G.add_edge(7, 3)
    G.add_edge(7, 1)

    assert count_connected_nodes(G, []) == 8


def test_connected_two_circulars_arms():
    G = nx.Graph()

    G.add_edge(1, 2)
    G.add_edge(2, 3)
    G.add_edge(3, 4)
    G.add_edge(4, 5)
    G.add_edge(5, 6)
    G.add_edge(6, 3)
    G.add_edge(7, 3)
    G.add_edge(7, 1)

    G.add_edge(2, 9)
    G.add_edge(10, 5)
    G.add_edge(10, 11)

    assert count_connected_nodes(G, []) == 10


@patch(
    "catan.board.place.get_ressources_of_player_dict",
    return_value={
        T.RESSOURCE.Brick: 100,
        T.RESSOURCE.Lumber: 100,
        T.RESSOURCE.Wool: 100,
        T.RESSOURCE.Grain: 100,
    },
)
@patch("catan.board.place.remove_ressource_from_player")
def test_connected_roads_on_boards(player_blue, player_red):
    board = (
        BoardBuilder()
        .create_board_of_size([3, 4, 5, 4, 3])
        .with_player(player_blue)
        .with_player(player_red)
        .build()
    )

    add_building(board, player_blue, 100, T.BUILDING.SETTELMENT, founding=True)
    add_connection(board, player_blue, 100, 104, T.CONNECTION.ROAD)

    count = count_nodes_of_player(board, player_blue)
    assert count == 1


@patch(
    "catan.board.place.get_ressources_of_player_dict",
    return_value={
        T.RESSOURCE.Brick: 100,
        T.RESSOURCE.Lumber: 100,
        T.RESSOURCE.Wool: 100,
        T.RESSOURCE.Grain: 100,
    },
)
@patch("catan.board.place.remove_ressource_from_player")
def test_connected_roads_on_boards_2(player_blue, player_red):
    board = (
        BoardBuilder()
        .create_board_of_size([3, 4, 5, 4, 3])
        .with_player(player_blue)
        .with_player(player_red)
        .build()
    )

    add_building(board, player_blue, 100, T.BUILDING.SETTELMENT, founding=True)
    add_connection(board, player_blue, 100, 104, T.CONNECTION.ROAD)
    add_connection(board, player_blue, 103, 100, T.CONNECTION.ROAD)

    count = count_nodes_of_player(board, player_blue)
    assert count == 2


@patch(
    "catan.board.place.get_ressources_of_player_dict",
    return_value={
        T.RESSOURCE.Brick: 100,
        T.RESSOURCE.Lumber: 100,
        T.RESSOURCE.Wool: 100,
        T.RESSOURCE.Grain: 100,
    },
)
@patch("catan.board.place.remove_ressource_from_player")
def test_connected_roads_on_boards_3(player_blue, player_red):
    board = (
        BoardBuilder()
        .create_board_of_size([3, 4, 5, 4, 3])
        .with_player(player_blue)
        .with_player(player_red)
        .build()
    )

    add_building(board, player_blue, 100, T.BUILDING.SETTELMENT, founding=True)
    add_connection(board, player_blue, 100, 104, T.CONNECTION.ROAD)
    add_connection(board, player_blue, 104, 108, T.CONNECTION.ROAD)
    add_connection(board, player_blue, 108, 112, T.CONNECTION.ROAD)
    add_building(board, player_blue, 112, T.BUILDING.SETTELMENT, founding=True)
    add_connection(board, player_blue, 117, 112, T.CONNECTION.ROAD)
    add_connection(board, player_blue, 117, 123, T.CONNECTION.ROAD)

    count = count_nodes_of_player(board, player_blue)
    assert count == 5


@patch(
    "catan.board.place.get_ressources_of_player_dict",
    return_value={
        T.RESSOURCE.Brick: 100,
        T.RESSOURCE.Lumber: 100,
        T.RESSOURCE.Wool: 100,
        T.RESSOURCE.Grain: 100,
    },
)
@patch("catan.board.place.remove_ressource_from_player")
def test_connected_roads_on_boards_two_spots(player_blue, player_red):
    board = (
        BoardBuilder()
        .create_board_of_size([3, 4, 5, 4, 3])
        .with_player(player_blue)
        .with_player(player_red)
        .build()
    )

    add_building(board, player_blue, 100, T.BUILDING.SETTELMENT, founding=True)
    add_connection(board, player_blue, 100, 104, T.CONNECTION.ROAD)
    add_connection(board, player_blue, 104, 108, T.CONNECTION.ROAD)
    add_connection(board, player_blue, 108, 112, T.CONNECTION.ROAD)

    add_building(board, player_blue, 135, T.BUILDING.SETTELMENT, founding=True)
    add_connection(board, player_blue, 135, 130, T.CONNECTION.ROAD)
    add_connection(board, player_blue, 130, 124, T.CONNECTION.ROAD)

    count = count_nodes_of_player(board, player_blue)
    assert count == 3


@patch(
    "catan.board.place.get_ressources_of_player_dict",
    return_value={
        T.RESSOURCE.Brick: 100,
        T.RESSOURCE.Lumber: 100,
        T.RESSOURCE.Wool: 100,
        T.RESSOURCE.Grain: 100,
    },
)
@patch("catan.board.place.remove_ressource_from_player")
def test_connected_roads_on_boards_interrupt_by_settelment(
    _, __, player_blue, player_red
):
    board = (
        BoardBuilder()
        .create_board_of_size([3, 4, 5, 4, 3])
        .with_player(player_blue)
        .with_player(player_red)
        .build()
    )

    add_building(board, player_blue, 100, T.BUILDING.SETTELMENT, founding=True)
    add_connection(board, player_blue, 100, 104, T.CONNECTION.ROAD)
    add_connection(board, player_blue, 104, 108, T.CONNECTION.ROAD)
    add_connection(board, player_blue, 108, 112, T.CONNECTION.ROAD)
    add_connection(board, player_blue, 112, 117, T.CONNECTION.ROAD)
    add_connection(board, player_blue, 117, 122, T.CONNECTION.ROAD)
    add_connection(board, player_blue, 122, 128, T.CONNECTION.ROAD)

    add_building(board, player_red, 122, T.BUILDING.SETTELMENT, founding=True)

    count = count_nodes_of_player(board, player_blue)
    assert count == 5


@patch(
    "catan.board.place.get_ressources_of_player_dict",
    return_value={
        T.RESSOURCE.Brick: 100,
        T.RESSOURCE.Lumber: 100,
        T.RESSOURCE.Wool: 100,
        T.RESSOURCE.Grain: 100,
    },
)
@patch("catan.board.place.remove_ressource_from_player")
def test_connected_roads_on_boards_interrupt_by_street(_, __, player_blue, player_red):
    board = (
        BoardBuilder()
        .create_board_of_size([3, 4, 5, 4, 3])
        .with_player(player_blue)
        .with_player(player_red)
        .build()
    )

    add_building(board, player_blue, 100, T.BUILDING.SETTELMENT, founding=True)
    add_connection(board, player_blue, 100, 104, T.CONNECTION.ROAD)
    add_connection(board, player_blue, 104, 108, T.CONNECTION.ROAD)
    add_connection(board, player_blue, 108, 112, T.CONNECTION.ROAD)

    add_building(board, player_blue, 129, T.BUILDING.SETTELMENT, founding=True)
    add_connection(board, player_blue, 129, 123, T.CONNECTION.ROAD)
    add_connection(board, player_blue, 123, 117, T.CONNECTION.ROAD)

    add_building(board, player_red, 116, T.BUILDING.SETTELMENT, founding=True)
    add_connection(board, player_red, 116, 122, T.CONNECTION.ROAD)
    add_connection(board, player_red, 122, 117, T.CONNECTION.ROAD)
    add_connection(board, player_red, 117, 112, T.CONNECTION.ROAD)
    add_connection(board, player_red, 116, 111, T.CONNECTION.ROAD)

    assert count_nodes_of_player(board, player_blue) == 3
    assert count_nodes_of_player(board, player_red) == 4


@patch(
    "catan.board.place.get_ressources_of_player_dict",
    return_value={
        T.RESSOURCE.Brick: 100,
        T.RESSOURCE.Lumber: 100,
        T.RESSOURCE.Wool: 100,
        T.RESSOURCE.Grain: 100,
    },
)
@patch("catan.board.place.remove_ressource_from_player")
def test_longest_road_both_to_short(_, __, player_blue, player_red):
    board = (
        BoardBuilder()
        .create_board_of_size([3, 4, 5, 4, 3])
        .with_player(player_blue)
        .with_player(player_red)
        .build()
    )

    add_building(board, player_blue, 100, T.BUILDING.SETTELMENT, founding=True)
    add_connection(board, player_blue, 100, 104, T.CONNECTION.ROAD)
    add_connection(board, player_blue, 104, 108, T.CONNECTION.ROAD)
    add_connection(board, player_blue, 108, 112, T.CONNECTION.ROAD)

    add_building(board, player_blue, 129, T.BUILDING.SETTELMENT, founding=True)
    add_connection(board, player_blue, 129, 123, T.CONNECTION.ROAD)
    add_connection(board, player_blue, 123, 117, T.CONNECTION.ROAD)

    add_building(board, player_red, 116, T.BUILDING.SETTELMENT, founding=True)
    add_connection(board, player_red, 116, 122, T.CONNECTION.ROAD)
    add_connection(board, player_red, 122, 117, T.CONNECTION.ROAD)
    add_connection(board, player_red, 117, 112, T.CONNECTION.ROAD)
    add_connection(board, player_red, 116, 111, T.CONNECTION.ROAD)

    assert get_longest_road_victory_points(board, player_blue) == 0
    assert get_longest_road_victory_points(board, player_red) == 0


@patch(
    "catan.board.place.get_ressources_of_player_dict",
    return_value={
        T.RESSOURCE.Brick: 100,
        T.RESSOURCE.Lumber: 100,
        T.RESSOURCE.Wool: 100,
        T.RESSOURCE.Grain: 100,
    },
)
@patch("catan.board.place.remove_ressource_from_player")
def test_longest_road_for_red_5(_, __, player_blue, player_red):
    board = (
        BoardBuilder()
        .create_board_of_size([3, 4, 5, 4, 3])
        .with_player(player_blue)
        .with_player(player_red)
        .build()
    )

    add_building(board, player_blue, 100, T.BUILDING.SETTELMENT, founding=True)
    add_connection(board, player_blue, 100, 104, T.CONNECTION.ROAD)
    add_connection(board, player_blue, 104, 108, T.CONNECTION.ROAD)
    add_connection(board, player_blue, 108, 112, T.CONNECTION.ROAD)

    add_building(board, player_blue, 129, T.BUILDING.SETTELMENT, founding=True)
    add_connection(board, player_blue, 129, 123, T.CONNECTION.ROAD)
    add_connection(board, player_blue, 123, 117, T.CONNECTION.ROAD)

    add_building(board, player_red, 116, T.BUILDING.SETTELMENT, founding=True)
    add_connection(board, player_red, 116, 122, T.CONNECTION.ROAD)
    add_connection(board, player_red, 122, 117, T.CONNECTION.ROAD)
    add_connection(board, player_red, 117, 112, T.CONNECTION.ROAD)
    add_connection(board, player_red, 116, 111, T.CONNECTION.ROAD)
    add_connection(board, player_red, 111, 107, T.CONNECTION.ROAD)
    add_connection(board, player_red, 107, 103, T.CONNECTION.ROAD)

    assert get_longest_road_victory_points(board, player_blue) == 0
    assert get_longest_road_victory_points(board, player_red) == 2


@patch(
    "catan.board.place.get_ressources_of_player_dict",
    return_value={
        T.RESSOURCE.Brick: 100,
        T.RESSOURCE.Lumber: 100,
        T.RESSOURCE.Wool: 100,
        T.RESSOURCE.Grain: 100,
    },
)
@patch("catan.board.place.remove_ressource_from_player")
def test_longest_road_for_both_5(_, __, player_blue, player_red):
    board = (
        BoardBuilder()
        .create_board_of_size([3, 4, 5, 4, 3])
        .with_player(player_blue)
        .with_player(player_red)
        .build()
    )

    add_building(board, player_blue, 100, T.BUILDING.SETTELMENT, founding=True)
    add_connection(board, player_blue, 100, 104, T.CONNECTION.ROAD)
    add_connection(board, player_blue, 104, 108, T.CONNECTION.ROAD)
    add_connection(board, player_blue, 108, 112, T.CONNECTION.ROAD)
    add_connection(board, player_blue, 108, 113, T.CONNECTION.ROAD)
    add_connection(board, player_blue, 113, 109, T.CONNECTION.ROAD)
    add_connection(board, player_blue, 109, 105, T.CONNECTION.ROAD)
    add_connection(board, player_blue, 105, 102, T.CONNECTION.ROAD)

    add_building(board, player_red, 116, T.BUILDING.SETTELMENT, founding=True)
    add_connection(board, player_red, 116, 122, T.CONNECTION.ROAD)
    add_connection(board, player_red, 122, 117, T.CONNECTION.ROAD)
    add_connection(board, player_red, 117, 112, T.CONNECTION.ROAD)
    add_connection(board, player_red, 116, 111, T.CONNECTION.ROAD)
    add_connection(board, player_red, 111, 107, T.CONNECTION.ROAD)
    add_connection(board, player_red, 107, 103, T.CONNECTION.ROAD)

    assert get_longest_road_victory_points(board, player_blue) == 0
    assert get_longest_road_victory_points(board, player_red) == 0
