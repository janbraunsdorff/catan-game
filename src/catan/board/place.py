from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Tuple

if TYPE_CHECKING:
    from catan.player import Player  # pragma: no cover

import catan.board.types as T
from catan.board.ressources import (
    get_ressources_of_player_dict,
    remove_ressource_from_player,
)


class PlaceNotAllowed(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)


def add_building(
    G: T.Board,
    player: Player,
    index: int,
    building: T.BUILDING,
    founding: bool = False,
) -> None:
    check_building(
        G=G,
        player=player,
        index=index,
        building=building,
        founding=founding,
        raise_on_error=True,
    )

    G.nodes[index]["building_type"] = building

    if building == T.BUILDING.CITY:
        G.add_edge(player.color, index, type=T.EDGE_TYPE.CITY_ONWERSHIP)
        remove_ressource_from_player(G, player, T.RESSOURCE.Grain)
        remove_ressource_from_player(G, player, T.RESSOURCE.Grain)
        remove_ressource_from_player(G, player, T.RESSOURCE.Ore)
        remove_ressource_from_player(G, player, T.RESSOURCE.Ore)
        remove_ressource_from_player(G, player, T.RESSOURCE.Ore)

    elif building == T.BUILDING.SETTELMENT:
        G.add_edge(player.color, index, type=T.EDGE_TYPE.SETTELMENT_OWNERSHIP)
        if not founding:
            remove_ressource_from_player(G, player, T.RESSOURCE.Brick)
            remove_ressource_from_player(G, player, T.RESSOURCE.Wool)
            remove_ressource_from_player(G, player, T.RESSOURCE.Lumber)
            remove_ressource_from_player(G, player, T.RESSOURCE.Grain)


def check_building(
    G: T.Board,
    player: Player,
    index: int,
    building: T.BUILDING,
    founding: bool,
    raise_on_error: bool,
) -> bool:
    try:
        _pass_or_raise_number_of_buildings(G=G, player=player, building=building)
        _pass_or_raise_node_type_to_place(G=G, index=index)

        if building == T.BUILDING.SETTELMENT:
            _pass_or_raise_can_place_settelment(G=G, index=index)
            _pass_or_raise_has_enough_ressources_for_settelment(
                G=G, player=player, founding=founding
            )
            _pass_or_raise_buldings_are_to_close(G=G, index=index)
            _pass_or_raise_building_not_connected_to_street(
                G=G, player=player, index=index, founding=founding
            )

        if building == T.BUILDING.CITY:
            _pass_or_raise_can_place_city(G=G, player=player, index=index)
            _pass_or_raise_has_enough_ressources_for_city(G=G, player=player)
    except PlaceNotAllowed as e:
        if raise_on_error:
            raise e
        return False

    return True


def add_connection(
    G: T.Board, player: Player, node_u: int, node_v: int, building: T.CONNECTION
) -> None:
    # TODO check numer of streets alreay placed
    # check if edge and empty road
    edge = G.edges[node_u, node_v]
    if edge["type"] != T.EDGE_TYPE.STREET:
        raise PlaceNotAllowed("Connection is not a street")

    if edge["street_type"] != T.CONNECTION.MISSING:
        raise PlaceNotAllowed("A street alreay exists")

    ressources = get_ressources_of_player_dict(G, player)
    if T.RESSOURCE.Brick not in ressources or T.RESSOURCE.Lumber not in ressources:
        raise PlaceNotAllowed("Player has not enough resources")

    # next to building
    is_connected = False
    for node in [node_u, node_v]:
        n = G.nodes[node]

        connecetd_to_building = (
            get_ownership_of_node(G, node) == player.color
            and n["building_type"] != T.BUILDING.MISSING
        )
        connected_to_street = (
            len(_get_souring_streets_of_street(G=G, player=player, node=node)) > 0
        )

        is_connected |= connected_to_street or connecetd_to_building

    if not is_connected:
        raise PlaceNotAllowed("No Street or Building is connected")

    G.edges[node_u, node_v]["owner"] = player.color
    G.edges[node_u, node_v]["street_type"] = building

    remove_ressource_from_player(G, player, T.RESSOURCE.Brick)
    remove_ressource_from_player(G, player, T.RESSOURCE.Lumber)


def get_buildings_of_player(
    G: T.Board, player: Player, connection_type: T.EDGE_TYPE
) -> List[Dict]:
    edges = G.edges(player.color, data=True)
    return [val for x, y, val in edges if val["type"] == connection_type]


def get_ownership_of_node(G: T.Board, node_index: int) -> str:
    edges = G.edges(node_index, data=True)
    a = [
        u
        for u, v, x in edges
        if x["type"] == T.EDGE_TYPE.CITY_ONWERSHIP
        or x["type"] == T.EDGE_TYPE.SETTELMENT_OWNERSHIP
    ]
    b = [
        v
        for u, v, x in edges
        if x["type"] == T.EDGE_TYPE.CITY_ONWERSHIP
        or x["type"] == T.EDGE_TYPE.SETTELMENT_OWNERSHIP
    ]

    a.extend(b)

    players = [x for x in a if G.nodes[x]["type"] == T.NODE_TYPE.PLAYER]
    if len(players) == 0:
        return ""

    return players[0]


def _get_souring_streets_of_street(G: T.Board, player: Player, node: int):
    edges = [
        (u, v, x)
        for u, v, x in G.edges(node, data=True)
        if x["type"] == T.EDGE_TYPE.STREET and x["owner"] == player.color
    ]
    return edges


def _pass_or_raise_building_not_connected_to_street(
    G: T.Board, player: Player, index: int, founding: bool
):
    if founding:
        return
    edges = G.edges(index, data=True)
    streets = [
        s
        for f, t, s in edges
        if s["type"] == T.EDGE_TYPE.STREET
        and s["street_type"] == T.CONNECTION.ROAD
        and s["owner"] == player.color
    ]

    if len(streets) == 0:
        raise PlaceNotAllowed("Building connects not to an road")


def _pass_or_raise_buldings_are_to_close(G: T.Board, index: int):
    edges = G.edges(index, data=True)

    neighbour_a = [t for f, t, x in edges if x["type"] == T.EDGE_TYPE.STREET]

    neighbour_b = [t for f, t, x in edges if x["type"] == T.EDGE_TYPE.STREET]

    neighbour_a.extend(neighbour_b)
    neighbours = list(set(neighbour_a))

    for n in neighbours:
        if G.nodes[n]["building_type"] != T.BUILDING.MISSING:
            raise PlaceNotAllowed("Building too close to another")


def _pass_or_raise_number_of_buildings(
    G: T.Board, building: T.BUILDING, player: Player
):
    building_config: Dict[T.BUILDING, Tuple[T.EDGE_TYPE, int]] = {
        T.BUILDING.CITY: (T.EDGE_TYPE.CITY_ONWERSHIP, 4),
        T.BUILDING.SETTELMENT: (T.EDGE_TYPE.SETTELMENT_OWNERSHIP, 5),
    }

    connection_type, max_num = building_config[building]

    buildings = get_buildings_of_player(
        G=G, player=player, connection_type=connection_type
    )
    if len(buildings) >= max_num:
        raise PlaceNotAllowed(f"Too many {building} already exits")


def _pass_or_raise_has_enough_ressources_for_settelment(
    G: T.Board, player: Player, founding: bool
):
    if founding:
        return
    ressources = get_ressources_of_player_dict(G=G, player=player)
    currently_avible = set(ressources.keys())

    requiretemtns = set(
        [T.RESSOURCE.Brick, T.RESSOURCE.Wool, T.RESSOURCE.Grain, T.RESSOURCE.Lumber]
    )

    remaining = requiretemtns - currently_avible

    if len(remaining) >= 1:
        raise PlaceNotAllowed(
            f"Not enough resources. Player {player.color} as only {ressources}. Missing {remaining}"
        )


def _pass_or_raise_has_enough_ressources_for_city(G: T.Board, player: Player):
    ressources = get_ressources_of_player_dict(G=G, player=player)
    error = PlaceNotAllowed(
        f"Not enough resources. Player {player.color} as only {ressources}"
    )

    if T.RESSOURCE.Grain not in ressources or T.RESSOURCE.Ore not in ressources:
        raise error

    if ressources[T.RESSOURCE.Grain] < 2:
        raise error

    if ressources[T.RESSOURCE.Ore] < 3:
        raise error


def _pass_or_raise_can_place_settelment(G: T.Board, index: int):
    node = G.nodes[index]

    if node["building_type"] != T.BUILDING.MISSING:
        raise PlaceNotAllowed(
            f"Can not place building to an already build node. Current buiding type {node['building_type']}"
        )


def _pass_or_raise_can_place_city(G: T.Board, player: Player, index: int):
    node = G.nodes[index]
    if node["building_type"] != T.BUILDING.SETTELMENT:
        raise PlaceNotAllowed(
            f"Can not upgrade settlement. Target Node is not any settelment, got: {node['building_type']}"
        )

    edges = G.edges(index, data=True)
    owner = [
        y for x, y, val in edges if val["type"] == T.EDGE_TYPE.SETTELMENT_OWNERSHIP
    ][0]

    if owner != player.color:
        raise PlaceNotAllowed(
            f"Can not upgrade settlement. Target settelment is of player '{owner}'. You are '{player.color}'"
        )


def _pass_or_raise_node_type_to_place(G: T.Board, index: int):
    if index not in G:
        raise PlaceNotAllowed(f"Node with index {index} not exits")

    node = G.nodes[index]
    if node["type"] != T.NODE_TYPE.BUILDING:
        raise PlaceNotAllowed(
            f"Can not place building to node of type { node['type']}. Allowd is only NODE_TYPE.BUILDING"
        )
