# longest streets -> https://stackoverflow.com/questions/64737143/is-there-a-networkx-algorithm-to-find-the-longest-path-from-a-source-to-a-target b
from __future__ import annotations

from typing import TYPE_CHECKING, List, Self, Set, Tuple

if TYPE_CHECKING:
    from catan.player import Player  # pragma: no cover

from itertools import permutations

import networkx as nx

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


def count_development_cards(G: T.Board, player: Player) -> int:
    development_cards = [
        v
        for u, v, data in G.edges(data=True)
        if data["type"] == T.EDGE_TYPE.DEVELOPMENT_OWNERSHIP
        and data["owner"] == player.color
    ]

    counter = 0
    for development_card in development_cards:
        if (
            G.nodes[development_card]["development_type"]
            == T.DEVELOPMENT_CARDS.VICTORY_POINTS
        ):
            counter += 1

    return counter


# TODO: count


class Node:
    def __init__(self, value: int, length: int, leafes: List[Self]) -> None:
        self.value = value
        self.length = length
        self.leafes = leafes

    def get_longest_path(self) -> int:
        if len(self.leafes) == 0:
            return self.length
        return max([x.get_longest_path() for x in self.leafes])


def get_conected_nodes_to(
    edges: List[Tuple[int, int]], node: int
) -> Set[Tuple[int, int]]:
    possible_edges = filter(
        lambda x: x[0] == node or x[1] == node,
        edges,
    )
    possible_edges_set = set(possible_edges)
    return possible_edges_set


def get_conected_nodes_recursive(
    edges: List[Tuple[int, int]],
    start_node: int,
    depth: int,
    history: Set[Tuple[int, int]],
) -> Node:
    surrounding_nodes = get_conected_nodes_to(edges, start_node)
    surrounding_nodes -= history

    leafes = []
    if len(surrounding_nodes) > 0:
        for x in surrounding_nodes:
            further_node = x[0] if x[0] != start_node else x[1]
            hc = history.copy()
            hc.add(x)
            leafe = get_conected_nodes_recursive(
                edges, further_node, depth=depth + 1, history=hc
            )
            leafes.append(leafe)

    return Node(start_node, length=depth, leafes=leafes)


def count_connected_nodes(G: T.Board) -> int:
    edges = G.edges()
    edges = sorted(edges, key=lambda element: (element[0], element[1]))
    nodes = [x for x, y in edges]
    nodes.extend([y for x, y in edges])

    nodes = list(set(nodes))

    longest_depth = 0
    for start_node in nodes:
        root = get_conected_nodes_recursive(edges, start_node, 0, set())
        depth = root.get_longest_path()
        if depth > longest_depth:
            longest_depth = depth

    return longest_depth
