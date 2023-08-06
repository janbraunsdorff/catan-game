# longest streets -> https://stackoverflow.com/questions/64737143/is-there-a-networkx-algorithm-to-find-the-longest-path-from-a-source-to-a-target b
from __future__ import annotations

from typing import TYPE_CHECKING, List, Self, Set, Tuple

import networkx as nx

import catan.board.types as T
from catan.board.developments import get_knights_of_player
from catan.board.place import get_buildings_of_player, get_ownership_of_node
from catan.player import Player


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
    stop_nodes: List[int],
) -> Node:
    surrounding_nodes = get_conected_nodes_to(edges, start_node)
    surrounding_nodes -= history

    leafes = []
    if len(surrounding_nodes) > 0:
        for x in surrounding_nodes:
            further_node = x[0] if x[0] != start_node else x[1]
            if further_node in stop_nodes:
                continue

            hc = history.copy()
            hc.add(x)
            leafe = get_conected_nodes_recursive(
                edges, further_node, depth=depth + 1, history=hc, stop_nodes=stop_nodes
            )
            leafes.append(leafe)

    return Node(start_node, length=depth, leafes=leafes)


def count_connected_nodes(G: T.Board, stopnodes: List[int]) -> int:
    edges = G.edges()
    edges = sorted(edges, key=lambda element: (element[0], element[1]))
    nodes = [x for x, y in edges]
    nodes.extend([y for x, y in edges])

    nodes = list(set(nodes))

    longest_depth = 0
    for start_node in nodes:
        root = get_conected_nodes_recursive(edges, start_node, 0, set(), stopnodes)
        depth = root.get_longest_path()
        if depth > longest_depth:
            longest_depth = depth

    return longest_depth


def get_filter_nodes_by_player(G: T.Board):
    def filter_nodes(node):
        node_data = G.nodes[node]

        if node_data["type"] != T.NODE_TYPE.BUILDING:
            return False

        if node_data["building_type"] == T.BUILDING.MISSING:
            return True

        return True

    return filter_nodes


def get_filter_edges_by_player(G: T.Board, plyer: Player):
    def filter_edges(node_v, node_u):
        edge = G.get_edge_data(node_v, node_u)

        if edge["type"] != T.EDGE_TYPE.STREET:
            return False

        if edge["street_type"] == T.CONNECTION.MISSING:
            return False

        if edge["owner"] != plyer.color:
            return False

        return True

    return filter_edges


def count_nodes_of_player(G: T.Board, player: Player) -> int:
    sub_graph = nx.subgraph_view(
        G,
        filter_edge=get_filter_edges_by_player(G, player),
        filter_node=get_filter_nodes_by_player(G),
    )

    stop_nodes_owner: List[Tuple[int, str]] = [
        (node, get_ownership_of_node(G, node))
        for node, data in G.nodes(data=True)
        if data["type"] == T.NODE_TYPE.BUILDING
    ]

    stop_nodes: List[int] = list(
        map(
            lambda x: x[0],
            filter(lambda x: x[1] != "" and x[1] != player.color, stop_nodes_owner),
        )
    )
    return count_connected_nodes(sub_graph, stopnodes=stop_nodes)


def get_longest_road_victory_points(G, player: Player) -> int:
    players = [x for x, y in G.nodes(data=True) if y["type"] == T.NODE_TYPE.PLAYER]
    player_to_longest_road = [
        (color, count_nodes_of_player(G, Player(T.COLOR(color)))) for color in players
    ]

    max_length = max(map(lambda x: x[1], player_to_longest_road))

    if max_length < 5:
        return 0

    best_player = list(filter(lambda x: x[1] == max_length, player_to_longest_road))

    if len(best_player) > 1:
        return 0

    if best_player[0][0] == player.color:
        return 2
    else:
        return 0
