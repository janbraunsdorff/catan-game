from uuid import uuid4

import networkx as nx
import pytest

import catan.board.types as T
from catan.board.graph import BoardBuilder
from catan.board.place import (
    PlaceNotAllowed,
    add_building,
    check_building,
    get_buildings_of_player,
)
from catan.board.ressources import get_ressources_of_player_list
from catan.player import Player


def test_place_settelments_to_much_settelments(player_blue):
    G = nx.Graph()

    G.add_node(player_blue.color, type=T.NODE_TYPE.PLAYER)

    for x in range(5):
        G.add_node(x, type=T.NODE_TYPE.BUILDING, kind=T.BUILDING.SETTELMENT)
        G.add_edge(x, player_blue.color, type=T.EDGE_TYPE.SETTELMENT_OWNERSHIP)

    num_nodes = len(G.nodes())
    num_edges = len(G.edges())

    with pytest.raises(PlaceNotAllowed) as e:
        add_building(
            G,
            player=player_blue,
            index=-1,
            building=T.BUILDING.SETTELMENT,
            founding=False,
        )

    assert e.value.args[0] == "Too many BUILDING.SETTELMENT already exits"

    assert len(G.nodes()) == num_nodes
    assert len(G.edges()) == num_edges


def test_place_settelments_to_much_cities(player_blue):
    G = nx.Graph()

    G.add_node(player_blue.color, type=T.NODE_TYPE.PLAYER)

    for x in range(4):
        G.add_node(x, type=T.NODE_TYPE.BUILDING, kind=T.BUILDING.CITY)
        G.add_edge(x, player_blue.color, type=T.EDGE_TYPE.CITY_ONWERSHIP)

    num_nodes = len(G.nodes())
    num_edges = len(G.edges())

    with pytest.raises(PlaceNotAllowed) as e:
        add_building(
            G, player=player_blue, index=-1, building=T.BUILDING.CITY, founding=False
        )

    assert e.value.args[0] == "Too many BUILDING.CITY already exits"

    assert len(G.nodes()) == num_nodes
    assert len(G.edges()) == num_edges


def test_place_to_none_existing_node(player_blue):
    G = nx.Graph()

    G.add_node(player_blue.color, type=T.NODE_TYPE.PLAYER)

    with pytest.raises(PlaceNotAllowed) as e:
        add_building(
            G,
            player=player_blue,
            index=404,
            building=T.BUILDING.SETTELMENT,
            founding=False,
        )

    assert e.value.args[0] == "Node with index 404 not exits"


def test_place_to_wrong_node_type(player_blue):
    G = nx.Graph()

    G.add_node(player_blue.color, type=T.NODE_TYPE.PLAYER)

    G.add_node(100, type=T.NODE_TYPE.PORT)

    with pytest.raises(PlaceNotAllowed) as e:
        add_building(
            G,
            player=player_blue,
            index=100,
            building=T.BUILDING.SETTELMENT,
            founding=False,
        )

    assert (
        e.value.args[0]
        == "Can not place building to node of type NODE_TYPE.PORT. Allowd is only NODE_TYPE.BUILDING"
    )


def test_place_already_filled(player_blue):
    G = nx.Graph()

    G.add_node(player_blue.color, type=T.NODE_TYPE.PLAYER)

    G.add_node(100, type=T.NODE_TYPE.BUILDING, bulding_type=T.BUILDING.SETTELMENT)

    with pytest.raises(PlaceNotAllowed) as e:
        add_building(
            G,
            player=player_blue,
            index=100,
            building=T.BUILDING.SETTELMENT,
            founding=False,
        )

    assert (
        e.value.args[0]
        == "Can not place building to an already build node. Current buiding type BUILDING.SETTELMENT"
    )


def test_place_city_to_none_existing_node(player_blue):
    G = nx.Graph()

    G.add_node(player_blue.color, type=T.NODE_TYPE.PLAYER)

    with pytest.raises(PlaceNotAllowed) as e:
        add_building(
            G, player=player_blue, index=404, building=T.BUILDING.CITY, founding=False
        )

    assert e.value.args[0] == "Node with index 404 not exits"


def test_place_city_to_wrong_node_type(player_blue):
    G = nx.Graph()

    G.add_node(player_blue.color, type=T.NODE_TYPE.PLAYER)

    G.add_node(100, type=T.NODE_TYPE.PORT)

    with pytest.raises(PlaceNotAllowed) as e:
        add_building(
            G, player=player_blue, index=100, building=T.BUILDING.CITY, founding=False
        )

    assert (
        e.value.args[0]
        == "Can not place building to node of type NODE_TYPE.PORT. Allowd is only NODE_TYPE.BUILDING"
    )


def test_place_city_only_if_settelment_was_placed_no_settelment(player_blue):
    G = nx.Graph()

    G.add_node(player_blue.color, type=T.NODE_TYPE.PLAYER)

    G.add_node(100, type=T.NODE_TYPE.BUILDING, bulding_type=T.BUILDING.MISSING)

    with pytest.raises(PlaceNotAllowed) as e:
        add_building(
            G, player=player_blue, index=100, building=T.BUILDING.CITY, founding=False
        )

    assert (
        e.value.args[0]
        == "Can not upgrade settlement. Target Node is not any settelment, got: BUILDING.MISSING"
    )


def test_place_city_only_if_own_settelment_was_placed(player_blue, player_red):
    G = nx.Graph()

    G.add_node(player_blue.color, type=T.NODE_TYPE.PLAYER)
    G.add_node(player_red.color, type=T.NODE_TYPE.PLAYER)

    G.add_node(100, type=T.NODE_TYPE.BUILDING, bulding_type=T.BUILDING.SETTELMENT)

    G.add_edge(player_blue.color, 100, type=T.EDGE_TYPE.SETTELMENT_OWNERSHIP)

    with pytest.raises(PlaceNotAllowed) as e:
        add_building(
            G, player=player_red, index=100, building=T.BUILDING.CITY, founding=False
        )

    assert (
        e.value.args[0]
        == "Can not upgrade settlement. Target settelment is of player 'blue'. You are 'red'"
    )


@pytest.mark.parametrize(
    "ressources",
    (
        [],
        [T.RESSOURCE.Brick],
        [T.RESSOURCE.Brick, T.RESSOURCE.Wool],
        [T.RESSOURCE.Brick, T.RESSOURCE.Lumber],
        [T.RESSOURCE.Brick, T.RESSOURCE.Lumber, T.RESSOURCE.Wool],
        [T.RESSOURCE.Brick, T.RESSOURCE.Lumber, T.RESSOURCE.Wool, T.RESSOURCE.Wool],
        [T.RESSOURCE.Brick, T.RESSOURCE.Lumber, T.RESSOURCE.Grain],
        [T.RESSOURCE.Brick, T.RESSOURCE.Lumber, T.RESSOURCE.Wool, T.RESSOURCE.Ore],
    ),
)
def test_place_settelment_to_low_ressources(player_red, ressources):
    G = nx.Graph()

    G.add_node(player_red.color, type=T.NODE_TYPE.PLAYER)
    G.add_node(100, type=T.NODE_TYPE.BUILDING, bulding_type=T.BUILDING.MISSING)

    for r in ressources:
        ressource_id = str(uuid4())

        G.add_node(ressource_id, type=T.NODE_TYPE.RESSOURCE, ressource=r)
        G.add_edge(player_red.color, ressource_id, type=T.EDGE_TYPE.RESSOURCE_OWNERSHIP)

    with pytest.raises(PlaceNotAllowed) as e:
        add_building(
            G,
            player=player_red,
            index=100,
            building=T.BUILDING.SETTELMENT,
            founding=False,
        )


@pytest.mark.parametrize(
    "ressources",
    (
        [],
        [T.RESSOURCE.Brick],
        [T.RESSOURCE.Brick, T.RESSOURCE.Lumber, T.RESSOURCE.Wool],
        [T.RESSOURCE.Brick, T.RESSOURCE.Lumber, T.RESSOURCE.Wool, T.RESSOURCE.Wool],
        [T.RESSOURCE.Brick, T.RESSOURCE.Lumber, T.RESSOURCE.Wool, T.RESSOURCE.Ore],
        [T.RESSOURCE.Grain, T.RESSOURCE.Grain, T.RESSOURCE.Ore, T.RESSOURCE.Ore],
        [
            T.RESSOURCE.Grain,
            T.RESSOURCE.Grain,
            T.RESSOURCE.Grain,
            T.RESSOURCE.Ore,
            T.RESSOURCE.Ore,
        ],
        [T.RESSOURCE.Grain, T.RESSOURCE.Ore, T.RESSOURCE.Ore, T.RESSOURCE.Ore],
    ),
)
def test_place_citiy_to_low_ressources(ressources, player_red):
    G = nx.Graph()

    G.add_node(player_red.color, type=T.NODE_TYPE.PLAYER)
    G.add_node(100, type=T.NODE_TYPE.BUILDING, bulding_type=T.BUILDING.SETTELMENT)
    G.add_edge(player_red.color, 100, type=T.EDGE_TYPE.SETTELMENT_OWNERSHIP)

    for r in ressources:
        ressource_id = str(uuid4())

        G.add_node(ressource_id, type=T.NODE_TYPE.RESSOURCE, ressource=r)
        G.add_edge(player_red.color, ressource_id, type=T.EDGE_TYPE.RESSOURCE_OWNERSHIP)

    with pytest.raises(PlaceNotAllowed) as e:
        add_building(
            G, player=player_red, index=100, building=T.BUILDING.CITY, founding=False
        )


def test_add_settelement_next_to_another_one_tile(player_red):
    G = BoardBuilder().create_board_of_size([1]).with_player(player=player_red).build()

    for r in [
        T.RESSOURCE.Brick,
        T.RESSOURCE.Wool,
        T.RESSOURCE.Grain,
        T.RESSOURCE.Lumber,
    ]:
        ressource_id = str(uuid4())
        G.add_node(ressource_id, type=T.NODE_TYPE.RESSOURCE, ressource=r)
        G.add_edge(player_red.color, ressource_id, type=T.EDGE_TYPE.RESSOURCE_OWNERSHIP)

    G.nodes[100]["bulding_type"] = T.BUILDING.SETTELMENT
    assert G.nodes[100]["bulding_type"] == T.BUILDING.SETTELMENT

    with pytest.raises(PlaceNotAllowed) as e:
        add_building(G=G, player=player_red, index=101, building=T.BUILDING.SETTELMENT)

    assert e.value.args[0] == "Building too close to another"


def test_add_settelement_without_connecting_street(player_red):
    G = BoardBuilder().create_board_of_size([1]).with_player(player=player_red).build()

    for r in [
        T.RESSOURCE.Brick,
        T.RESSOURCE.Wool,
        T.RESSOURCE.Grain,
        T.RESSOURCE.Lumber,
    ]:
        ressource_id = str(uuid4())
        G.add_node(ressource_id, type=T.NODE_TYPE.RESSOURCE, ressource=r)
        G.add_edge(player_red.color, ressource_id, type=T.EDGE_TYPE.RESSOURCE_OWNERSHIP)

    with pytest.raises(PlaceNotAllowed) as e:
        add_building(G=G, player=player_red, index=101, building=T.BUILDING.SETTELMENT)

    assert e.value.args[0] == "Building connects not to an road"


def test_add_settelment_connect_to_other_road(player_red):
    G = BoardBuilder().create_board_of_size([1]).with_player(player=player_red).build()

    for r in [
        T.RESSOURCE.Brick,
        T.RESSOURCE.Wool,
        T.RESSOURCE.Grain,
        T.RESSOURCE.Lumber,
    ]:
        ressource_id = str(uuid4())
        G.add_node(ressource_id, type=T.NODE_TYPE.RESSOURCE, ressource=r)
        G.add_edge(player_red.color, ressource_id, type=T.EDGE_TYPE.RESSOURCE_OWNERSHIP)

    G.edges[100, 101]["street_type"] = T.CONNECTION.Road
    G.edges[100, 101]["owner"] = "404"

    with pytest.raises(PlaceNotAllowed) as e:
        add_building(G=G, player=player_red, index=101, building=T.BUILDING.SETTELMENT)

    assert e.value.args[0] == "Building connects not to an road"


def test_successfull_place_settelmemt(player_red):
    G = BoardBuilder().create_board_of_size([1]).with_player(player=player_red).build()

    for r in [
        T.RESSOURCE.Brick,
        T.RESSOURCE.Wool,
        T.RESSOURCE.Grain,
        T.RESSOURCE.Lumber,
    ]:
        ressource_id = str(uuid4())
        G.add_node(ressource_id, type=T.NODE_TYPE.RESSOURCE, ressource=r)
        G.add_edge(player_red.color, ressource_id, type=T.EDGE_TYPE.RESSOURCE_OWNERSHIP)

    G.edges[100, 101]["street_type"] = T.CONNECTION.Road
    G.edges[100, 101]["owner"] = player_red.color

    num_nodes = len(G.nodes())
    num_edges = len(G.edges())

    add_building(G=G, player=player_red, index=101, building=T.BUILDING.SETTELMENT)

    assert len(G.nodes()) == num_nodes - 4
    assert len(G.edges()) == num_edges + 1 - 4

    assert G.nodes[101]["bulding_type"] == T.BUILDING.SETTELMENT
    assert len(get_ressources_of_player_list(G, player_red)) == 0
    assert (
        len(get_buildings_of_player(G, player_red, T.EDGE_TYPE.SETTELMENT_OWNERSHIP))
        == 1
    )


def test_city_place_settelmemt(player_red):
    G = BoardBuilder().create_board_of_size([1]).with_player(player=player_red).build()

    for r in [
        T.RESSOURCE.Brick,
        T.RESSOURCE.Wool,
        T.RESSOURCE.Grain,
        T.RESSOURCE.Lumber,
    ]:
        ressource_id = str(uuid4())
        G.add_node(ressource_id, type=T.NODE_TYPE.RESSOURCE, ressource=r)
        G.add_edge(player_red.color, ressource_id, type=T.EDGE_TYPE.RESSOURCE_OWNERSHIP)

    G.edges[100, 101]["street_type"] = T.CONNECTION.Road
    G.edges[100, 101]["owner"] = player_red.color

    add_building(G=G, player=player_red, index=101, building=T.BUILDING.SETTELMENT)

    for r in [
        T.RESSOURCE.Grain,
        T.RESSOURCE.Grain,
        T.RESSOURCE.Ore,
        T.RESSOURCE.Ore,
        T.RESSOURCE.Ore,
    ]:
        ressource_id = str(uuid4())
        G.add_node(ressource_id, type=T.NODE_TYPE.RESSOURCE, ressource=r)
        G.add_edge(player_red.color, ressource_id, type=T.EDGE_TYPE.RESSOURCE_OWNERSHIP)

    num_nodes = len(G.nodes())
    num_edges = len(G.edges())

    add_building(G=G, player=player_red, index=101, building=T.BUILDING.CITY)

    assert len(G.nodes()) == num_nodes - 5
    assert len(G.edges()) == num_edges - 5

    assert G.nodes[101]["bulding_type"] == T.BUILDING.CITY
    assert len(get_ressources_of_player_list(G, player_red)) == 0
    assert len(get_buildings_of_player(G, player_red, T.EDGE_TYPE.CITY_ONWERSHIP)) == 1
    assert len(G.edges(player_red.color, data=True)) == 1


def test_founding_without_ressources_and_streets(player_red):
    G = BoardBuilder().create_board_of_size([1]).with_player(player=player_red).build()

    add_building(
        G=G, player=player_red, index=101, building=T.BUILDING.SETTELMENT, founding=True
    )

    assert G.nodes[101]["bulding_type"] == T.BUILDING.SETTELMENT
    assert (
        len(get_buildings_of_player(G, player_red, T.EDGE_TYPE.SETTELMENT_OWNERSHIP))
        == 1
    )


def test_retun_False_on_error(player_red):
    G = BoardBuilder().create_board_of_size([1]).with_player(player=player_red).build()

    res = check_building(
        G=G,
        player=player_red,
        index=101,
        building=T.BUILDING.SETTELMENT,
        founding=False,
        raise_on_error=False,
    )

    assert res == False


def test_retun_True_on_error(player_red):
    G = BoardBuilder().create_board_of_size([1]).with_player(player=player_red).build()

    for r in [
        T.RESSOURCE.Brick,
        T.RESSOURCE.Wool,
        T.RESSOURCE.Grain,
        T.RESSOURCE.Lumber,
    ]:
        ressource_id = str(uuid4())
        G.add_node(ressource_id, type=T.NODE_TYPE.RESSOURCE, ressource=r)
        G.add_edge(player_red.color, ressource_id, type=T.EDGE_TYPE.RESSOURCE_OWNERSHIP)

    G.edges[100, 101]["street_type"] = T.CONNECTION.Road
    G.edges[100, 101]["owner"] = player_red.color

    res = check_building(
        G=G,
        player=player_red,
        index=101,
        building=T.BUILDING.SETTELMENT,
        founding=False,
        raise_on_error=False,
    )

    assert res == True
