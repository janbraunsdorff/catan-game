from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from catan.player import Player  # pragma: no cover

from collections import Counter
from typing import Dict, List
from uuid import uuid4

import catan.board.types as T
from catan.board.graph import get_player_node_by_color

field_to_ressource: Dict[T.TILE_TYPE, T.RESSOURCE] = {
    T.TILE_TYPE.Desert: T.RESSOURCE.No,
    T.TILE_TYPE.Fields: T.RESSOURCE.Grain,
    T.TILE_TYPE.Forest: T.RESSOURCE.Lumber,
    T.TILE_TYPE.Hills: T.RESSOURCE.Brick,
    T.TILE_TYPE.Mountains: T.RESSOURCE.Ore,
    T.TILE_TYPE.Pasture: T.RESSOURCE.Wool,
}


def add_ressource_to_player(
    G: T.Board, player: Player, ressource: T.RESSOURCE
) -> T.Board:
    idx, data = get_player_node_by_color(G, player)
    ressource_id = str(uuid4())

    G.add_node(ressource_id, type=T.NODE_TYPE.RESSOURCE, ressource=ressource)
    G.add_edge(idx, ressource_id, type=T.EDGE_TYPE.RESSOURCE_OWNERSHIP, owner=idx)

    return G


def add_ressource_to_player_id(
    G: T.Board, player_idx: str, ressource: T.RESSOURCE
) -> T.Board:
    ressource_id = str(uuid4())

    G.add_node(ressource_id, type=T.NODE_TYPE.RESSOURCE, ressource=ressource)
    G.add_edge(
        player_idx, ressource_id, type=T.EDGE_TYPE.RESSOURCE_OWNERSHIP, owner=player_idx
    )

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
                and G.nodes[node_a]["building_type"] != T.BUILDING.MISSING
                and G.has_edge(node_a, player.color)
            ):
                return True

            if (
                G.nodes[node_b]["type"] == T.NODE_TYPE.BUILDING
                and G.nodes[node_b]["building_type"] != T.BUILDING.MISSING
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


def _check_player_ressouerces(
    G: T.Board, player: Player, ressource: List[T.RESSOURCE], raise_on_error=False
) -> bool:
    ressources_player = get_ressources_of_player_dict(G, player)
    ressource_dict = {k: x for k, x in Counter(ressource).items()}

    for k in ressource_dict.keys():
        if ressource_dict[k] > ressources_player.get(k, 0):
            if raise_on_error:
                raise ValueError("Not enough resources")
            return False

    return True


def player_trate(
    G: T.Board,
    player_a: Player,
    player_b: Player,
    ressource_a: List[T.RESSOURCE],
    ressource_b: List[T.RESSOURCE],
    raise_on_error=False,
):
    if not _check_player_ressouerces(
        G, player_a, ressource_a, raise_on_error=raise_on_error
    ):
        return False

    if not _check_player_ressouerces(
        G, player_b, ressource_b, raise_on_error=raise_on_error
    ):
        return False

    for ressource in ressource_a:
        remove_ressource_from_player(G, player_a, ressource)
        add_ressource_to_player(G, player_b, ressource)

    for ressource in ressource_b:
        remove_ressource_from_player(G, player_b, ressource)
        add_ressource_to_player(G, player_a, ressource)

    return True


def add_ressource_after_dice_roll(G: T.Board, dice_value: int):
    thrown_fileds = [
        x
        for x, y in G.nodes(data=True)
        if y["type"] == T.NODE_TYPE.TILE and y["dice_value"] == dice_value
    ]

    for field in thrown_fileds:
        ressource_type = G.nodes[field]["node_type"]

        get_ressources = [
            max(t, n)
            for t, n, y in G.edges(field, data=True)
            if y["type"] == T.EDGE_TYPE.PRODUCE_TO
        ]

        players = []
        for r in get_ressources:
            if G.nodes[r]["building_type"] == T.BUILDING.SETTELMENT:
                ownership = [
                    n
                    for r, n, y in G.edges(r, data=True)
                    if y["type"] == T.EDGE_TYPE.SETTELMENT_OWNERSHIP
                ][0]
                players.append(ownership)

            if G.nodes[r]["building_type"] == T.BUILDING.CITY:
                ownership = [
                    n
                    for r, n, y in G.edges(r, data=True)
                    if y["type"] == T.EDGE_TYPE.CITY_ONWERSHIP
                ][0]
                players.append(ownership)
                players.append(ownership)

        for player in players:
            add_ressource_to_player_id(G, player, field_to_ressource[ressource_type])
