import networkx as nx
import pytest

import catan.board.types as T
from catan.board.place import PlaceNotAllowed, add_building
from catan.player import Player


class TestPlayer(Player):
    def __init__(self, color: T.COLOR) -> None:
        super().__init__(color)


def test_place_settelments_to_much_settelments():
    G = nx.Graph()

    player = TestPlayer(T.COLOR.BLUE)
    G.add_node(player.color, type=T.NODE_TYPE.PLAYER)

    for x in range(5):
        G.add_node(x, type=T.NODE_TYPE.BUILDING, kind=T.BUILDING.SETTELMENT)
        G.add_edge(x, player.color, type=T.EDGE_TYPE.SETTELMENT_OWNERSHIP)

    num_nodes = len(G.nodes())
    num_edges = len(G.edges())

    with pytest.raises(PlaceNotAllowed) as e:
        add_building(
            G, player=player, index=-1, building=T.BUILDING.SETTELMENT, founding=False
        )

    assert e.value.args[0] == "Too many BUILDING.SETTELMENT already exits"

    assert len(G.nodes()) == num_nodes
    assert len(G.edges()) == num_edges


def test_place_settelments_to_much_cities():
    G = nx.Graph()

    player = TestPlayer(T.COLOR.BLUE)
    G.add_node(player.color, type=T.NODE_TYPE.PLAYER)

    for x in range(4):
        G.add_node(x, type=T.NODE_TYPE.BUILDING, kind=T.BUILDING.CITY)
        G.add_edge(x, player.color, type=T.EDGE_TYPE.CITY_ONWERSHIP)

    num_nodes = len(G.nodes())
    num_edges = len(G.edges())

    with pytest.raises(PlaceNotAllowed) as e:
        add_building(
            G, player=player, index=-1, building=T.BUILDING.CITY, founding=False
        )

    assert e.value.args[0] == "Too many BUILDING.CITY already exits"

    assert len(G.nodes()) == num_nodes
    assert len(G.edges()) == num_edges


def test_place_to_none_existing_node():
    G = nx.Graph()

    player = TestPlayer(T.COLOR.BLUE)
    G.add_node(player.color, type=T.NODE_TYPE.PLAYER)

    with pytest.raises(PlaceNotAllowed) as e:
        add_building(
            G, player=player, index=404, building=T.BUILDING.SETTELMENT, founding=False
        )

    assert e.value.args[0] == "Node with index 404 not exits"


def test_place_to_wrong_node_type():
    G = nx.Graph()

    player = TestPlayer(T.COLOR.BLUE)
    G.add_node(player.color, type=T.NODE_TYPE.PLAYER)

    G.add_node(100, type=T.NODE_TYPE.PORT)

    with pytest.raises(PlaceNotAllowed) as e:
        add_building(
            G, player=player, index=100, building=T.BUILDING.SETTELMENT, founding=False
        )

    assert (
        e.value.args[0]
        == "Can not place building to node of type NODE_TYPE.PORT. Allowd is only NODE_TYPE.BUILDING"
    )


def test_place_already_filled():
    G = nx.Graph()

    player = TestPlayer(T.COLOR.BLUE)
    G.add_node(player.color, type=T.NODE_TYPE.PLAYER)

    G.add_node(100, type=T.NODE_TYPE.BUILDING, bulding_type=T.BUILDING.SETTELMENT)

    with pytest.raises(PlaceNotAllowed) as e:
        add_building(
            G, player=player, index=100, building=T.BUILDING.SETTELMENT, founding=False
        )

    assert (
        e.value.args[0]
        == "Can not place building to an already build node. Current buiding type BUILDING.SETTELMENT"
    )


def test_place_city_to_none_existing_node():
    G = nx.Graph()

    player = TestPlayer(T.COLOR.BLUE)
    G.add_node(player.color, type=T.NODE_TYPE.PLAYER)

    with pytest.raises(PlaceNotAllowed) as e:
        add_building(
            G, player=player, index=404, building=T.BUILDING.CITY, founding=False
        )

    assert e.value.args[0] == "Node with index 404 not exits"


def test_place_city_to_wrong_node_type():
    G = nx.Graph()

    player = TestPlayer(T.COLOR.BLUE)
    G.add_node(player.color, type=T.NODE_TYPE.PLAYER)

    G.add_node(100, type=T.NODE_TYPE.PORT)

    with pytest.raises(PlaceNotAllowed) as e:
        add_building(
            G, player=player, index=100, building=T.BUILDING.CITY, founding=False
        )

    assert (
        e.value.args[0]
        == "Can not place building to node of type NODE_TYPE.PORT. Allowd is only NODE_TYPE.BUILDING"
    )


def test_place_city_only_if_settelment_was_placed_no_settelment():
    G = nx.Graph()

    player = TestPlayer(T.COLOR.BLUE)
    G.add_node(player.color, type=T.NODE_TYPE.PLAYER)

    G.add_node(100, type=T.NODE_TYPE.BUILDING, bulding_type=T.BUILDING.MISSING)

    with pytest.raises(PlaceNotAllowed) as e:
        add_building(
            G, player=player, index=100, building=T.BUILDING.CITY, founding=False
        )

    assert (
        e.value.args[0]
        == "Can not upgrade settlement. Target Node is not any settelment, got: BUILDING.MISSING"
    )


def test_place_city_only_if_own_settelment_was_placed():
    G = nx.Graph()

    player_a = TestPlayer(T.COLOR.BLUE)
    player_b = TestPlayer(T.COLOR.RED)

    G.add_node(player_a.color, type=T.NODE_TYPE.PLAYER)
    G.add_node(player_b.color, type=T.NODE_TYPE.PLAYER)

    G.add_node(100, type=T.NODE_TYPE.BUILDING, bulding_type=T.BUILDING.SETTELMENT)

    G.add_edge(player_a.color.value, 100, type=T.EDGE_TYPE.SETTELMENT_OWNERSHIP)

    with pytest.raises(PlaceNotAllowed) as e:
        add_building(
            G, player=player_b, index=100, building=T.BUILDING.CITY, founding=False
        )

    assert (
        e.value.args[0]
        == "Can not upgrade settlement. Target settelment is of player 'blue'. You are 'red'"
    )
