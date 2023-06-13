from enum import Enum
from typing import Dict, List, Tuple

import networkx as nx


class NODE_TYPES(Enum):
    Missing = 0
    Mountains = 1
    Hills = 2
    Forest = 3
    Fields = 4
    Pasture = 5
    Desert = 6


class PORTS(Enum):
    Any = 1
    Grain = 2
    Ore = 3
    Wool = 4
    Brick = 5
    Lumber = 6


class ROBBERS(Enum):
    Normal = 1
    See = 3


class ROADS(Enum):
    Missing = 1
    Placed = 2
    Boat = 3


class BUILDINGS(Enum):
    Missing = 1
    Settelment = 2
    City = 3


Coor = Tuple[float, float]


def create_board(size: List[int]) -> nx.Graph:
    """Create a simple and empty board containing tiles, buildings places, steeet places and tile providing build places

    Parameters
    ----------
    size : List[int]
        Size of the board

    Returns
    -------
    nx.Graph
        Board as Networkx Graph
    """
    G = nx.Graph()
    G, buildings, tile_building = create_tiles(G=G, board_size=size)
    corr_to_index = create_empty_buildings(
        G=G, buildings=buildings, tile_building=tile_building
    )
    create_empty_streets(G=G, tile_building=tile_building, corr_to_index=corr_to_index)

    return G


def create_tiles(
    G: nx.Graph,
    board_size: List[int],
    step_x: float = 10.0,
    step_y: float = 2.88675134595,
) -> Tuple[nx.Graph, List[Coor], Dict[int, List[Coor]]]:
    """create a geometry disturbation of an catan born with a given size

    Parameters
    ----------
    G : nx.Graph
        Refference to an existing graph
    board_size : List[int]
        Size of an board. e.g. `[3, 4, 5, 4, 3]`
    step_x : float, optional
        geometric step in x, by default 10.0
    step_y : float, optional
        gemetric step in 0.33 * y for, by default 2.88675134595

    Returns
    -------
    Tuple[nx.Graph, List[Coor], Dict[int, List[Coor]]]
        Graph, sorted list of building coordinates, mapping of tile to building coordinates
    """
    buildings: List[Coor] = []
    tile_building: Dict[int, List[Coor]] = {}

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
                            "type": "tile",
                            "node_type": NODE_TYPES.Missing,
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
    G: nx.Graph, buildings: List[Coor], tile_building: Dict[int, List[Coor]]
) -> Dict[Coor, int]:
    corr_to_index = {}
    cnt_buildings = 100
    for x in buildings:
        # create building
        G.add_nodes_from(
            [
                (
                    cnt_buildings,
                    {"type": "building", "bulding_type": BUILDINGS.Missing, "coor": x},
                )
            ]
        )

        # create provided connecrtions
        for tile, porvided in tile_building.items():
            if x in porvided:
                G.add_edge(
                    tile,
                    cnt_buildings,
                    label={"type": "produce_to", "corr": [tile, cnt_buildings]},
                )

        corr_to_index[x] = cnt_buildings
        cnt_buildings += 1

    return corr_to_index


def create_empty_streets(
    G: nx.Graph, tile_building: Dict[int, List[Coor]], corr_to_index: Dict[Coor, int]
) -> None:
    street_index = [(0, 1), (0, 2), (1, 3), (2, 4), (5, 3), (5, 4)]
    for _, porvided in tile_building.items():
        porvided.sort(key=lambda x: (x[1], x[0]))
        for a, b in street_index:
            x = corr_to_index[porvided[a]]
            y = corr_to_index[porvided[b]]
            G.add_edge(
                x,
                y,
                label={"type": "street", "street_type": ROADS.Missing, "coor": [x, y]},
            )
