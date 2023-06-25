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


def port_trate_4_to_1(
    G: T.Board,
    player: Player,
    ressource: T.RESSOURCE,
    output: T.RESSOURCE,
    raise_on_error: bool = False,
) -> bool:
    if not check_ressources(G, player, ressource, 4, raise_on_error=raise_on_error):
        return False

    for _ in range(4):
        remove_ressource_from_player(G, player, ressource)

    add_ressource_to_player(G, player, output)
    return True


def check_ressources(
    G: T.Board,
    player: Player,
    ressource: T.RESSOURCE,
    number: int,
    raise_on_error=False,
) -> bool:
    if get_ressources_of_player_dict(G, player)[ressource] >= number:
        return True

    if raise_on_error:
        raise ValueError(f"No enough ressource for {number}:1 trate")
    return False


def player_has_port(G: T.Board, player: Player, port: T.PORT):
    ports = [
        x
        for x, y in G.nodes(data=True)
        if y["type"] == T.NODE_TYPE.PORT and y["port_type"] == port
    ]

    for port in ports:
        for node_a, node_b in [
            (u, v)
            for u, v, x in G.edges(port, data=True)
            if x["type"] == T.EDGE_TYPE.PORT_TO
        ]:
            if (
                G.nodes[node_a]["type"] == T.NODE_TYPE.BUILDING
                and G.nodes[node_a]["bulding_type"] != T.BUILDING.MISSING
                and G.has_edge(node_a, player.color)
            ):
                return True

            if (
                G.nodes[node_b]["type"] == T.NODE_TYPE.BUILDING
                and G.nodes[node_b]["bulding_type"] != T.BUILDING.MISSING
                and G.has_edge(node_b, player.color)
            ):
                return True
    return False


def post_trate_3_to_1(
    G: T.Board,
    player: Player,
    ressource: T.RESSOURCE,
    output: T.RESSOURCE,
    raise_on_error: bool = False,
):
    if not player_has_port(G, player, T.PORT.Any):
        if raise_on_error:
            raise ValueError("Player has no 3:1 claimed")
        else:
            return False

    if not check_ressources(G, player, ressource, 3, raise_on_error=raise_on_error):
        return False

    for _ in range(3):
        remove_ressource_from_player(G, player, ressource)

    add_ressource_to_player(G, player, output)

    return True


def post_trate_2_to_1(
    G: T.Board,
    player: Player,
    ressource: T.RESSOURCE,
    output: T.RESSOURCE,
    raise_on_error: bool = False,
):
    ressource_to_port = {
        T.RESSOURCE.Brick: T.PORT.Brick,
        T.RESSOURCE.Lumber: T.PORT.Lumber,
        T.RESSOURCE.Wool: T.PORT.Wool,
        T.RESSOURCE.Ore: T.PORT.Ore,
        T.RESSOURCE.Grain: T.PORT.Grain,
    }

    if not player_has_port(G, player, ressource_to_port[ressource]):
        if raise_on_error:
            raise ValueError("Player has no 2:1 port claimed")
        else:
            return False

    if not check_ressources(G, player, ressource, 2, raise_on_error=raise_on_error):
        return False

    for _ in range(2):
        remove_ressource_from_player(G, player, ressource)

    add_ressource_to_player(G, player, output)

    return True


def player_trate():
    # check of number of resources player a
    # check of number of resources player b
    pass
