from enum import Enum
from typing import Dict, List, Tuple

import networkx as nx

from catan.board.graph import create_tiles
from catan.board.types import NODE_TYPES


def test_create_filed_1():
    G = nx.Graph()

    size = [1]

    G, buildings, tile_building = create_tiles(G=G, board_size=size)

    assert len(G.nodes()) == 1
    assert list(G.nodes(data=True))[0][1]["type"] == "tile"
    assert list(G.nodes(data=True))[0][1]["node_type"] == NODE_TYPES.Missing

    assert len(buildings) == 6
    assert len(tile_building) == 1


def test_create_filed_2():
    G = nx.Graph()

    size = [2]

    G, buildings, tile_building = create_tiles(G=G, board_size=size)

    assert len(G.nodes()) == 2
    assert list(G.nodes(data=True))[0][1]["type"] == "tile"
    assert list(G.nodes(data=True))[0][1]["node_type"] == NODE_TYPES.Missing

    assert list(G.nodes(data=True))[1][1]["type"] == "tile"
    assert list(G.nodes(data=True))[1][1]["node_type"] == NODE_TYPES.Missing

    assert len(buildings) == 10
    assert len(tile_building) == 2


def test_create_filed_2_3():
    G = nx.Graph()

    size = [2, 3]

    G, buildings, tile_building = create_tiles(G=G, board_size=size)

    assert len(G.nodes()) == sum(size)

    assert len(buildings) == 19
    assert len(tile_building) == sum(size)
