from unittest.mock import patch

import pytest

import catan.board.types as T
from catan.board.graph import BoardBuilder
from catan.board.place import add_building
from catan.board.ressources import (
    add_ressource_after_dice_roll,
    get_ressources_of_player_list,
)
from catan.player import Player


@pytest.mark.parametrize(
    "field,ressource",
    [
        (T.TILE_TYPE.Fields, T.RESSOURCE.Grain),
        (T.TILE_TYPE.Mountains, T.RESSOURCE.Ore),
        (T.TILE_TYPE.Forest, T.RESSOURCE.Lumber),
        (T.TILE_TYPE.Hills, T.RESSOURCE.Brick),
        (T.TILE_TYPE.Pasture, T.RESSOURCE.Wool),
    ],
)
def test_add_dice_ressource(player_blue, field, ressource):
    board = (
        BoardBuilder().create_board_of_size([1, 2, 1]).with_player(player_blue).build()
    )

    tiles = [x for x, y in board.nodes(data=True) if y["type"] == T.NODE_TYPE.TILE]
    for tile, val, tile_type in zip(
        tiles,
        [1, 2, 3, 4],
        [
            field,
            T.TILE_TYPE.Desert,
            T.TILE_TYPE.Mountains,
            T.TILE_TYPE.Forest,
        ],
    ):
        board.nodes[tile]["dice_value"] = val
        board.nodes[tile]["node_type"] = tile_type

    add_building(board, player_blue, 100, T.BUILDING.SETTELMENT, founding=True)

    add_ressource_after_dice_roll(board, dice_value=1)

    ressources = get_ressources_of_player_list(board, player_blue)
    assert len(ressources) == 1
    assert ressources[0] == ressource


def test_add_dice_ressource_two_fields(player_blue):
    board = (
        BoardBuilder().create_board_of_size([1, 2, 1]).with_player(player_blue).build()
    )

    tiles = [x for x, y in board.nodes(data=True) if y["type"] == T.NODE_TYPE.TILE]
    for tile, val, tile_type in zip(
        tiles,
        [1, 2, 2, 4],
        [
            T.TILE_TYPE.Fields,
            T.TILE_TYPE.Pasture,
            T.TILE_TYPE.Mountains,
            T.TILE_TYPE.Forest,
        ],
    ):
        board.nodes[tile]["dice_value"] = val
        board.nodes[tile]["node_type"] = tile_type

    add_building(board, player_blue, 106, T.BUILDING.SETTELMENT, founding=True)

    add_ressource_after_dice_roll(board, dice_value=2)

    ressources = get_ressources_of_player_list(board, player_blue)
    assert len(ressources) == 2
    assert T.RESSOURCE.Wool in ressources
    assert T.RESSOURCE.Ore in ressources


def test_add_dice_ressource_two_players(player_blue, player_red):
    board = (
        BoardBuilder()
        .create_board_of_size([1, 2, 1])
        .with_player(player_blue)
        .with_player(player_red)
        .build()
    )

    tiles = [x for x, y in board.nodes(data=True) if y["type"] == T.NODE_TYPE.TILE]
    for tile, val, tile_type in zip(
        tiles,
        [1, 2, 2, 4],
        [
            T.TILE_TYPE.Fields,
            T.TILE_TYPE.Pasture,
            T.TILE_TYPE.Mountains,
            T.TILE_TYPE.Forest,
        ],
    ):
        board.nodes[tile]["dice_value"] = val
        board.nodes[tile]["node_type"] = tile_type

    add_building(board, player_blue, 106, T.BUILDING.SETTELMENT, founding=True)
    add_building(board, player_red, 112, T.BUILDING.SETTELMENT, founding=True)

    add_ressource_after_dice_roll(board, dice_value=2)

    ressources = get_ressources_of_player_list(board, player_blue)
    assert len(ressources) == 2
    assert T.RESSOURCE.Wool in ressources
    assert T.RESSOURCE.Ore in ressources

    ressources = get_ressources_of_player_list(board, player_red)
    assert len(ressources) == 1
    assert T.RESSOURCE.Ore in ressources


@patch("catan.board.place.remove_ressource_from_player")
@patch("catan.board.place.check_building")
@pytest.mark.parametrize(
    "field,ressource",
    [
        (T.TILE_TYPE.Fields, T.RESSOURCE.Grain),
        (T.TILE_TYPE.Mountains, T.RESSOURCE.Ore),
        (T.TILE_TYPE.Forest, T.RESSOURCE.Lumber),
        (T.TILE_TYPE.Hills, T.RESSOURCE.Brick),
        (T.TILE_TYPE.Pasture, T.RESSOURCE.Wool),
    ],
)
def test_add_dice_ressource_city(remove, check, player_blue, field, ressource):
    board = (
        BoardBuilder().create_board_of_size([1, 2, 1]).with_player(player_blue).build()
    )

    tiles = [x for x, y in board.nodes(data=True) if y["type"] == T.NODE_TYPE.TILE]
    for tile, val, tile_type in zip(
        tiles,
        [1, 2, 3, 4],
        [
            field,
            T.TILE_TYPE.Desert,
            T.TILE_TYPE.Mountains,
            T.TILE_TYPE.Forest,
        ],
    ):
        board.nodes[tile]["dice_value"] = val
        board.nodes[tile]["node_type"] = tile_type

    add_building(board, player_blue, 100, T.BUILDING.CITY, founding=True)

    add_ressource_after_dice_roll(board, dice_value=1)

    ressources = get_ressources_of_player_list(board, player_blue)
    assert len(ressources) == 2
    assert ressources[0] == ressource
    assert ressources[1] == ressource
