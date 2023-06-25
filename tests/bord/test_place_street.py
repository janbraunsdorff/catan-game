from uuid import uuid4

import networkx as nx
import pytest

import catan.board.types as T
from catan.board.graph import BoardBuilder
from catan.board.place import PlaceNotAllowed, add_connection
from catan.board.ressources import get_ressources_of_player_list
from catan.player import Player


class TestPlayer(Player):
    def __init__(self, color: T.COLOR) -> None:
        super().__init__(color)


def test_place_street_on_no_street_edge():
    player = TestPlayer(T.COLOR.BLUE)

    G = BoardBuilder().create_board_of_size([1]).with_player(player=player).build()

    with pytest.raises(PlaceNotAllowed) as e:
        add_connection(G, player, node_u=1, node_v=100, building=T.CONNECTION.Road)

    assert e.value.args[0] == "Connection is not a street"


def test_place_street_on_no_street_edge_reverse():
    player = TestPlayer(T.COLOR.BLUE)

    G = BoardBuilder().create_board_of_size([1]).with_player(player=player).build()

    with pytest.raises(PlaceNotAllowed) as e:
        add_connection(G, player, node_u=100, node_v=1, building=T.CONNECTION.Road)

    assert e.value.args[0] == "Connection is not a street"


def test_place_street_on_street():
    player = TestPlayer(T.COLOR.BLUE)

    G = BoardBuilder().create_board_of_size([1]).with_player(player=player).build()
    G.edges[100, 101]["street_type"] = T.CONNECTION.Road

    with pytest.raises(PlaceNotAllowed) as e:
        add_connection(G, player, node_u=100, node_v=101, building=T.CONNECTION.Road)

    assert e.value.args[0] == "A street alreay exists"


def test_player_has_no_enough_ressources():
    player = TestPlayer(T.COLOR.BLUE)

    G = BoardBuilder().create_board_of_size([1]).with_player(player=player).build()

    with pytest.raises(PlaceNotAllowed) as e:
        add_connection(G, player, node_u=100, node_v=101, building=T.CONNECTION.Road)

    assert e.value.args[0] == "Player has not enough resources"


def test_player_has_no_enough_ressources_brick():
    player = TestPlayer(T.COLOR.BLUE)

    G = BoardBuilder().create_board_of_size([1]).with_player(player=player).build()

    for r in [T.RESSOURCE.Brick]:
        ressource_id = str(uuid4())

        G.add_node(ressource_id, type=T.NODE_TYPE.RESSOURCE, ressource=r)
        G.add_edge(player.color, ressource_id, type=T.EDGE_TYPE.RESSOURCE_OWNERSHIP)

    with pytest.raises(PlaceNotAllowed) as e:
        add_connection(G, player, node_u=100, node_v=101, building=T.CONNECTION.Road)

    assert e.value.args[0] == "Player has not enough resources"


def test_player_has_no_enough_ressources_Lumber():
    player = TestPlayer(T.COLOR.BLUE)

    G = BoardBuilder().create_board_of_size([1]).with_player(player=player).build()

    for r in [T.RESSOURCE.Lumber]:
        ressource_id = str(uuid4())

        G.add_node(ressource_id, type=T.NODE_TYPE.RESSOURCE, ressource=r)
        G.add_edge(player.color, ressource_id, type=T.EDGE_TYPE.RESSOURCE_OWNERSHIP)

    with pytest.raises(PlaceNotAllowed) as e:
        add_connection(G, player, node_u=100, node_v=101, building=T.CONNECTION.Road)

    assert e.value.args[0] == "Player has not enough resources"


def test_not_connected_to_street_or_building_nothing():
    player = TestPlayer(T.COLOR.BLUE)

    G = BoardBuilder().create_board_of_size([1]).with_player(player=player).build()

    for r in [T.RESSOURCE.Lumber, T.RESSOURCE.Brick]:
        ressource_id = str(uuid4())

        G.add_node(ressource_id, type=T.NODE_TYPE.RESSOURCE, ressource=r)
        G.add_edge(player.color, ressource_id, type=T.EDGE_TYPE.RESSOURCE_OWNERSHIP)

    with pytest.raises(PlaceNotAllowed) as e:
        add_connection(G, player, node_u=100, node_v=101, building=T.CONNECTION.Road)

    assert e.value.args[0] == "No Street or Building is connected"


def test_not_connected_to_street_or_building_opponent_settelment():
    player = TestPlayer(T.COLOR.BLUE)
    player_b = Player(T.COLOR.RED)

    G = (
        BoardBuilder()
        .create_board_of_size([1])
        .with_player(player=player)
        .with_player(player_b)
        .build()
    )

    for r in [T.RESSOURCE.Lumber, T.RESSOURCE.Brick]:
        ressource_id = str(uuid4())

        G.add_node(ressource_id, type=T.NODE_TYPE.RESSOURCE, ressource=r)
        G.add_edge(player.color, ressource_id, type=T.EDGE_TYPE.RESSOURCE_OWNERSHIP)

    G.nodes[100]["bulding_type"] = T.BUILDING.SETTELMENT
    G.add_edge(player_b.color, 100, type=T.EDGE_TYPE.SETTELMENT_OWNERSHIP)

    with pytest.raises(PlaceNotAllowed) as e:
        add_connection(G, player, node_u=100, node_v=101, building=T.CONNECTION.Road)

    assert e.value.args[0] == "No Street or Building is connected"


def test_not_connected_to_street_or_building_opponent_citiy():
    player = TestPlayer(T.COLOR.BLUE)
    player_b = Player(T.COLOR.RED)

    G = (
        BoardBuilder()
        .create_board_of_size([1])
        .with_player(player=player)
        .with_player(player_b)
        .build()
    )

    for r in [T.RESSOURCE.Lumber, T.RESSOURCE.Brick]:
        ressource_id = str(uuid4())

        G.add_node(ressource_id, type=T.NODE_TYPE.RESSOURCE, ressource=r)
        G.add_edge(player.color, ressource_id, type=T.EDGE_TYPE.RESSOURCE_OWNERSHIP)

    G.nodes[100]["bulding_type"] = T.BUILDING.CITY
    G.add_edge(player_b.color, 100, type=T.EDGE_TYPE.CITY_ONWERSHIP)

    with pytest.raises(PlaceNotAllowed) as e:
        add_connection(G, player, node_u=100, node_v=101, building=T.CONNECTION.Road)

    assert e.value.args[0] == "No Street or Building is connected"


def test_build_street_next_to_street():
    player = TestPlayer(T.COLOR.BLUE)
    player_b = Player(T.COLOR.RED)

    G = (
        BoardBuilder()
        .create_board_of_size([1])
        .with_player(player=player)
        .with_player(player_b)
        .build()
    )

    for r in [T.RESSOURCE.Lumber, T.RESSOURCE.Brick]:
        ressource_id = str(uuid4())

        G.add_node(ressource_id, type=T.NODE_TYPE.RESSOURCE, ressource=r)
        G.add_edge(player.color, ressource_id, type=T.EDGE_TYPE.RESSOURCE_OWNERSHIP)

    G.edges[100, 101]["street_type"] = T.CONNECTION.Road
    G.edges[100, 101]["owner"] = player.color

    num_nodes = len(G.nodes())
    num_edges = len(G.edges())

    add_connection(G, player, node_u=100, node_v=102, building=T.CONNECTION.Road)

    assert len(G.edges()) == num_edges - 2
    assert len(G.nodes()) == num_nodes - 2
    assert G.edges[100, 102]["owner"] == player.color
    assert G.edges[100, 102]["street_type"] == T.CONNECTION.Road


def test_build_street_next_to_citiy():
    player = TestPlayer(T.COLOR.BLUE)
    player_b = Player(T.COLOR.RED)

    G = (
        BoardBuilder()
        .create_board_of_size([1])
        .with_player(player=player)
        .with_player(player_b)
        .build()
    )

    for r in [T.RESSOURCE.Lumber, T.RESSOURCE.Brick]:
        ressource_id = str(uuid4())

        G.add_node(ressource_id, type=T.NODE_TYPE.RESSOURCE, ressource=r)
        G.add_edge(player.color, ressource_id, type=T.EDGE_TYPE.RESSOURCE_OWNERSHIP)

    G.nodes[100]["bulding_type"] = T.BUILDING.CITY
    G.add_edge(player.color, 100, type=T.EDGE_TYPE.CITY_ONWERSHIP)

    num_nodes = len(G.nodes())
    num_edges = len(G.edges())

    add_connection(G, player, node_u=100, node_v=102, building=T.CONNECTION.Road)

    assert len(G.edges()) == num_edges - 2
    assert len(G.nodes()) == num_nodes - 2
    assert G.edges[100, 102]["owner"] == player.color
    assert G.edges[100, 102]["street_type"] == T.CONNECTION.Road


def test_build_street_next_to_settelement():
    player = TestPlayer(T.COLOR.BLUE)
    player_b = Player(T.COLOR.RED)

    G = (
        BoardBuilder()
        .create_board_of_size([1])
        .with_player(player=player)
        .with_player(player_b)
        .build()
    )

    for r in [T.RESSOURCE.Lumber, T.RESSOURCE.Brick]:
        ressource_id = str(uuid4())

        G.add_node(ressource_id, type=T.NODE_TYPE.RESSOURCE, ressource=r)
        G.add_edge(player.color, ressource_id, type=T.EDGE_TYPE.RESSOURCE_OWNERSHIP)

    G.nodes[100]["bulding_type"] = T.BUILDING.SETTELMENT
    G.add_edge(player.color, 100, type=T.EDGE_TYPE.SETTELMENT_OWNERSHIP)

    num_nodes = len(G.nodes())
    num_edges = len(G.edges())

    add_connection(G, player, node_u=100, node_v=102, building=T.CONNECTION.Road)

    assert len(G.edges()) == num_edges - 2
    assert len(G.nodes()) == num_nodes - 2
    assert G.edges[100, 102]["owner"] == player.color
    assert G.edges[100, 102]["street_type"] == T.CONNECTION.Road
