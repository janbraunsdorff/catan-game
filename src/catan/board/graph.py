"""functions to create an Board wirj player

Examples:
---------

GameBuilder()
    .create_board_of_size([3,4,5,3,4])
    .with_port(...)
    .with_port(...)
    .with_player(...)
    .with_player(...)
    .with_player(...)
    .build()

"""

from typing import Dict, List, Self, Tuple
from uuid import uuid4

import networkx as nx

import catan.board.types as T
from catan.player import Player


class BoardBuilder:
    def __init__(self) -> None:
        self.board: T.Board = nx.Graph()

    def create_board_of_size(self, size: List[int]) -> Self:
        self.board = create_board(self.board, size)
        return self

    def with_player(self, player: Player) -> Self:
        self.board = add_player(self.board, player)
        return self

    def with_port(self, port_type: T.PORT_TYPE, buildings: Tuple[int, int]) -> Self:
        self.board = add_port(self.board, port_type=port_type, buildings=buildings)
        return self

    def build(self) -> T.Board:
        return self.board


def add_port(G: T.Board, port_type: T.PORT_TYPE, buildings: Tuple[int, int]) -> T.Board:
    if buildings[0] not in G or buildings[1] not in G:
        raise ValueError(f"No bulding found for idx {buildings[0]}")

    port_idx = str(uuid4())
    G.add_node(port_idx, type=T.NODE_TYPE.PORT, port_type=port_type)

    G.add_edge(
        port_idx,
        buildings[0],
        type=T.EDGE_TYPE.PORT_TO,
    )

    G.add_edge(
        port_idx,
        buildings[1],
        type=T.EDGE_TYPE.PORT_TO,
    )
    return G


def add_player(G: T.Board, player: Player) -> T.Board:
    G.add_node(player.color, type=T.NODE_TYPE.PLAYER)
    return G


def get_player_node_by_color(G: T.Board, player: Player) -> Tuple[str, dict]:
    color = player.color
    return color, G.nodes[color]


def create_board(G: T.Board, size: List[int]) -> T.Board:
    """Create a simple and empty board containing tiles, buildings places, steeet places and tile providing build places

    Parameters
    ----------
    size : List[int]
        Size of the board

    Returns
    -------
    T.Board
        Board as Networkx Graph
    """
    G, buildings, tile_building = create_tiles(G=G, board_size=size)
    corr_to_index = create_empty_buildings(
        G=G, buildings=buildings, tile_building=tile_building
    )
    create_empty_streets(G=G, tile_building=tile_building, corr_to_index=corr_to_index)

    return G


def create_tiles(
    G: T.Board,
    board_size: List[int],
    step_x: float = 10.0,
    step_y: float = 2.88675134595,
) -> Tuple[T.Board, List[T.Coor], Dict[int, List[T.Coor]]]:
    """create a geometry disturbation of an catan born with a given size. Start index is 1

    Parameters
    ----------
    G : T.Board
        Refference to an existing graph
    board_size : List[int]
        Size of an board. e.g. `[3, 4, 5, 4, 3]`
    step_x : float, optional
        geometric step in x, by default 10.0
    step_y : float, optional
        gemetric step in 0.33 * y for, by default 2.88675134595

    Returns
    -------
    Tuple[T.Board, List[Coor], Dict[int, List[Coor]]]
        Graph, sorted list of building coordinates, mapping of tile to building coordinates
    """
    buildings: List[T.Coor] = []
    tile_building: Dict[int, List[T.Coor]] = {}

    cnt_tile = 1
    for idx, n_row in enumerate(board_size):
        first_shift = (max(board_size) - n_row) * (step_x * 0.5)

        for tile in range(n_row):
            y = step_y + (3 * step_y * idx)
            x = (tile * step_x) + first_shift

            # create tile
            G.add_nodes_from(
                [
                    (
                        cnt_tile,
                        {
                            "type": T.NODE_TYPE.TILE,
                            "node_type": T.TILE_TYPE.Missing,
                            "dice_value": -1,
                            "coor": (x, y),
                        },
                    )
                ]
            )

            # store position

            # calculate positions of building places
            buildings.append((x, round(y - (2 * step_y), 4)))
            buildings.append((round(x + step_x * 0.5, 4), round(y - (1 * step_y), 4)))
            buildings.append((round(x + step_x * 0.5, 4), round(y + (1 * step_y), 4)))
            buildings.append((x, round(y + (2 * step_y), 4)))
            buildings.append((round(x - step_x * 0.5, 4), round(y + (1 * step_y), 4)))
            buildings.append((round(x - step_x * 0.5, 4), round(y - (1 * step_y), 4)))

            # add buildings to tile
            tile_building[cnt_tile] = buildings[-6:]

            cnt_tile += 1

    buildings = list(set(buildings))
    buildings.sort(key=lambda x: (x[1], x[0]))

    return G, buildings, tile_building


def create_empty_buildings(
    G: T.Board, buildings: List[T.Coor], tile_building: Dict[int, List[T.Coor]]
) -> Dict[T.Coor, int]:
    """create building spaces for all tiles. starting index is 100

    Parameters
    ----------
    G : T.Board
        exiting grapg with empty tiles
    buildings : List[Coor]
        a list of ordered (by y,x) coordinates of each building placed in
    tile_building : Dict[int, List[Coor]]
        mapping of tile to building coordinates

    Returns
    -------
    Dict[Coor, int]
        Coordinates of each building
    """
    corr_to_index = {}
    cnt_buildings = 100
    for x in buildings:
        # create building
        G.add_nodes_from(
            [
                (
                    cnt_buildings,
                    {
                        "type": T.NODE_TYPE.BUILDING,
                        "bulding_type": T.BUILDING.MISSING,
                        "coor": x,
                    },
                )
            ]
        )

        # create provided connecrtions
        for tile, porvided in tile_building.items():
            if x in porvided:
                G.add_edge(
                    tile,
                    cnt_buildings,
                    label={
                        "type": T.EDGE_TYPE.PRODUCE_TO,
                        "corr": [tile, cnt_buildings],
                    },
                )

        corr_to_index[x] = cnt_buildings
        cnt_buildings += 1

    return corr_to_index


def create_empty_streets(
    G: T.Board, tile_building: Dict[int, List[T.Coor]], corr_to_index: Dict[T.Coor, int]
) -> None:
    # TODO: check if each edge exists once
    """create empy_streets between two building spaces

    Parameters
    ----------
    G : T.Board
        existing graph with tiles and building spaces
    tile_building : Dict[int, List[Coor]]
        mapping of tile to building coordinates
    corr_to_index : Dict[Coor, int]
        Coordinates of each building
    """
    street_index = [(0, 1), (0, 2), (1, 3), (2, 4), (5, 3), (5, 4)]
    for _, porvided in tile_building.items():
        porvided.sort(key=lambda x: (x[1], x[0]))
        for a, b in street_index:
            x = corr_to_index[porvided[a]]
            y = corr_to_index[porvided[b]]
            G.add_edge(
                x,
                y,
                label={
                    "type": T.EDGE_TYPE.STREET,
                    "street_type": T.CONNECTION.Missing,
                    "coor": [x, y],
                },
            )
