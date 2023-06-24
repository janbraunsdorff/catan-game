from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from catan.player import Player  # pragma: no cover

from collections import Counter
from typing import Dict, List
from uuid import uuid4

import catan.board.types as T
from catan.board.graph import get_player_node_by_color


def add_ressource_to_player(
    G: T.Board, player: Player, ressource: T.RESSOURCE
) -> T.Board:
    idx, data = get_player_node_by_color(G, player)
    ressource_id = str(uuid4())

    G.add_node(ressource_id, type=T.NODE_TYPE.RESSOURCE, ressource=ressource)
    G.add_edge(idx, ressource_id, type=T.EDGE_TYPE.RESSOURCE_OWNERSHIP)

    return G


def add_ressources_to_player(
    G: T.Board, player, ressources: List[T.RESSOURCE]
) -> T.Board:
    for ressource in ressources:
        G = add_ressource_to_player(G, player, ressource)
    return G


def get_ressources_of_player_list(G: T.Board, player: Player) -> List[T.RESSOURCE]:
    idx, data = get_player_node_by_color(G, player)
    edges = G.edges(idx, data=True)

    ressource_nodes = [
        r for _, r, x in edges if x["type"] == T.EDGE_TYPE.RESSOURCE_OWNERSHIP
    ]
    ressources = [G.nodes[rn]["ressource"] for rn in ressource_nodes]

    return ressources


def get_ressources_of_player_dict(G: T.Board, player: Player) -> Dict[T.RESSOURCE, int]:
    ressources = get_ressources_of_player_list(G, player)
    return {k: x for k, x in Counter(ressources).items()}


def remove_ressource_from_player(
    G: T.Board, player: Player, ressource: T.RESSOURCE
) -> T.Board:
    idx, data = get_player_node_by_color(G, player)
    edges = G.edges(idx, data=True)

    ressource_nodes = [
        (u, v)
        for u, v, x in edges
        if x["type"] == T.EDGE_TYPE.RESSOURCE_OWNERSHIP
        and G.nodes[v]["ressource"] == ressource
    ]

    if len(ressource_nodes) <= 0:
        raise ValueError("Ressource not available to remove")

    resource_node = ressource_nodes[0][1]
    plyaer_node = ressource_nodes[0][0]

    G.remove_edge(plyaer_node, resource_node)
    G.remove_node(resource_node)

    return G


def port_trate_4_to_1():
    # check of number of resources
    pass


def post_trate_3_to_1():
    # check for port
    # check of number of resources
    pass


def port_trate_2_to_1():
    # check for port
    # check of number of resources
    pass


def player_trate():
    # check of number of resources player a
    # check of number of resources player b
    pass
