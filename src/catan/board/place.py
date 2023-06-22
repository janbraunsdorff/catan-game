from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Tuple

if TYPE_CHECKING:
    from catan.player import Player

import catan.board.types as T


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
    _pass_or_raise_number_of_buildings(G=G, player=player, building=building)

    if building == T.BUILDING.SETTELMENT:
        _pass_or_raise_can_place_settelment(G=G, index=index)

    if building == T.BUILDING.CITY:
        _pass_or_raise_can_place_city(G=G, player=player, index=index)
    # if city, settelment must be placed first
    # player must own ressources if not founding
    # next bulding must be at least corssroads away

    # update node
    # add between node an player
    raise NotImplementedError()


def add_connection(
    G: T.Board, player: Player, index: int, building: T.CONNECTION
) -> None:
    raise NotImplementedError()


def get_buildings_of_player(
    G: T.Board, player: Player, connection_type: T.EDGE_TYPE
) -> List[Dict]:
    edges = G.edges(player.color, data=True)
    return [val for x, y, val in edges if val["type"] == connection_type]


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


def _pass_or_raise_can_place_settelment(G: T.Board, index: int):
    if index not in G:
        raise PlaceNotAllowed(f"Node with index {index} not exits")

    node = G.nodes[index]
    if node["type"] != T.NODE_TYPE.BUILDING:
        raise PlaceNotAllowed(
            f"Can not place building to node of type { node['type']}. Allowd is only NODE_TYPE.BUILDING"
        )
    if node["bulding_type"] != T.BUILDING.MISSING:
        raise PlaceNotAllowed(
            f"Can not place building to an already build node. Current buiding type {node['bulding_type']}"
        )


def _pass_or_raise_can_place_city(G: T.Board, player: Player, index: int):
    if index not in G:
        raise PlaceNotAllowed(f"Node with index {index} not exits")

    node = G.nodes[index]
    if node["type"] != T.NODE_TYPE.BUILDING:
        raise PlaceNotAllowed(
            f"Can not place building to node of type { node['type']}. Allowd is only NODE_TYPE.BUILDING"
        )

    if node["bulding_type"] != T.BUILDING.SETTELMENT:
        raise PlaceNotAllowed(
            f"Can not upgrade settlement. Target Node is not any settelment, got: {node['bulding_type']}"
        )

    edges = G.edges(index, data=True)
    owner = [
        y for x, y, val in edges if val["type"] == T.EDGE_TYPE.SETTELMENT_OWNERSHIP
    ][0]

    if owner != player.color.value:
        raise PlaceNotAllowed(
            f"Can not upgrade settlement. Target settelment is of player '{owner}'. You are '{player.color.value}'"
        )
