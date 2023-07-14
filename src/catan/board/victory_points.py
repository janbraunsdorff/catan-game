# developent cards
# longest streets -> https://stackoverflow.com/questions/64737143/is-there-a-networkx-algorithm-to-find-the-longest-path-from-a-source-to-a-target b
from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Tuple

if TYPE_CHECKING:
    from catan.player import Player

import catan.board.types as T
from catan.board.developments import get_knights_of_player
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


def highest_knights(G: T.Board, player: Player) -> int:
    players = [x for x, y in G.nodes(data=True) if y["type"] == T.NODE_TYPE.PLAYER]

    players_knights = [0]
    for x in [y for y in players if y != player.color]:
        players_knights.append(get_knights_of_player(G, x))

    knights = get_knights_of_player(G, player)

    return 2 if knights >= 3 and knights > max(players_knights) else 0
