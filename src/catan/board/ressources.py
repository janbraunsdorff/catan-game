from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from catan.player import Player

from typing import List
from uuid import uuid4

import catan.board.types as T
from catan.board.graph import get_player_node_by_color


def add_ressource_to_player(
    G: T.Board, player: Player, ressource: T.RESSOURCES
) -> T.Board:
    idx, data = get_player_node_by_color(G, player)
    ressource_id = str(uuid4())

    G.add_node(ressource_id, type="ressource", ressource=ressource)
    G.add_edge(idx, ressource_id, type="ressource_ownership")

    return G


def add_ressources_to_player(
    G: T.Board, player, ressources: List[T.RESSOURCES]
) -> T.Board:
    for ressource in ressources:
        G = add_ressource_to_player(G, player, ressource)
    return G


def get_ressources_of_player_list(G: T.Board, player: Player) -> List[T.RESSOURCES]:
    idx, data = get_player_node_by_color(G, player)
    edges = G.edges(idx, data=True)

    ressource_nodes = [r for _, r, x in edges if x["type"] == "ressource_ownership"]
    ressources = [G.nodes[rn]["ressource"] for rn in ressource_nodes]

    return ressources


def remove_ressource_from_player(
    G: T.Board, player: Player, ressource: T.RESSOURCES
) -> T.Board:
    idx, data = get_player_node_by_color(G, player)
    edges = G.edges(idx, data=True)

    ressource_nodes = [
        (u, v)
        for u, v, x in edges
        if x["type"] == "ressource_ownership" and G.nodes[v]["ressource"] == ressource
    ]

    if len(ressource_nodes) <= 0:
        raise ValueError("Ressource not available to remove")

    resource_node = ressource_nodes[0][1]
    plyaer_node = ressource_nodes[0][0]

    G.remove_edge(plyaer_node, resource_node)
    G.remove_node(resource_node)

    return G
