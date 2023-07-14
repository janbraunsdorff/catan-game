# developent cards
# longest streets -> https://stackoverflow.com/questions/64737143/is-there-a-networkx-algorithm-to-find-the-longest-path-from-a-source-to-a-target b
# most knights
from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Tuple

if TYPE_CHECKING:
    from catan.player import Player

import catan.board.types as T
from catan.board.place import get_buildings_of_player


def count_settelment_points(G: T.Board, player: Player) -> int:
    buildings = get_buildings_of_player(
        G=G, player=player, connection_type=T.EDGE_TYPE.SETTELMENT_OWNERSHIP
    )

    return len(buildings)


def count_city_points(G: T.Board, player: Player) -> int:
    buildings = get_buildings_of_player(
        G=G, player=player, connection_type=T.EDGE_TYPE.CITY_ONWERSHIP
    )

    return len(buildings) * 2
