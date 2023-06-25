from uuid import uuid4

import pytest

import catan.board.ressources as R
import catan.board.types as T
from catan.board.graph import BoardBuilder
from catan.player import Player


class TestPlayer(Player):
    def __init__(self, color: T.COLOR) -> None:
        super().__init__(color)


@pytest.mark.parametrize(
    "input_,output",
    [
        (T.RESSOURCE.Brick, T.RESSOURCE.Grain),
        (T.RESSOURCE.Ore, T.RESSOURCE.Grain),
        (T.RESSOURCE.Lumber, T.RESSOURCE.Ore),
        (T.RESSOURCE.Wool, T.RESSOURCE.Wool),
        (T.RESSOURCE.Brick, T.RESSOURCE.Grain),
        (T.RESSOURCE.Grain, T.RESSOURCE.Brick),
    ],
)
def test_trate_ressources_4_to_1(input_, output):
    player = TestPlayer(T.COLOR.BLUE)

    G = BoardBuilder().create_board_of_size([1]).with_player(player).build()

    for r in range(4):
        ressource_id = str(uuid4())

        G.add_node(ressource_id, type=T.NODE_TYPE.RESSOURCE, ressource=input_)
        G.add_edge(player.color, ressource_id, type=T.EDGE_TYPE.RESSOURCE_OWNERSHIP)

    num_nodes = len(G.nodes())
    num_edges = len(G.edges())
    assert R.get_ressources_of_player_dict(G, player)[input_] == 4

    done = R.port_trate_4_to_1(G, player, input_, output)

    assert len(G.nodes()) == num_nodes - 3
    assert len(G.edges()) == num_edges - 3
    assert R.get_ressources_of_player_dict(G, player)[output] == 1
    assert done


@pytest.mark.parametrize(
    "input_,output",
    [
        (T.RESSOURCE.Brick, T.RESSOURCE.Grain),
        (T.RESSOURCE.Ore, T.RESSOURCE.Grain),
        (T.RESSOURCE.Lumber, T.RESSOURCE.Ore),
        (T.RESSOURCE.Wool, T.RESSOURCE.Lumber),
        (T.RESSOURCE.Brick, T.RESSOURCE.Grain),
        (T.RESSOURCE.Grain, T.RESSOURCE.Brick),
    ],
)
def test_trate_ressources_4_to_1_less_ressources_check(input_, output):
    player = TestPlayer(T.COLOR.BLUE)

    G = BoardBuilder().create_board_of_size([1]).with_player(player).build()

    for r in range(3):
        ressource_id = str(uuid4())

        G.add_node(ressource_id, type=T.NODE_TYPE.RESSOURCE, ressource=input_)
        G.add_edge(player.color, ressource_id, type=T.EDGE_TYPE.RESSOURCE_OWNERSHIP)

    num_nodes = len(G.nodes())
    num_edges = len(G.edges())
    assert R.get_ressources_of_player_dict(G, player)[input_] == 3

    done = R.port_trate_4_to_1(G, player, input_, output)

    assert len(G.nodes()) == num_nodes
    assert len(G.edges()) == num_edges
    assert output not in R.get_ressources_of_player_dict(G, player)
    assert R.get_ressources_of_player_dict(G, player)[input_] == 3
    assert done == False


@pytest.mark.parametrize(
    "input_,output",
    [
        (T.RESSOURCE.Brick, T.RESSOURCE.Grain),
        (T.RESSOURCE.Ore, T.RESSOURCE.Grain),
        (T.RESSOURCE.Lumber, T.RESSOURCE.Ore),
        (T.RESSOURCE.Wool, T.RESSOURCE.Lumber),
        (T.RESSOURCE.Brick, T.RESSOURCE.Grain),
        (T.RESSOURCE.Grain, T.RESSOURCE.Brick),
    ],
)
def test_trate_ressources_4_to_1_less_ressources_raise(input_, output):
    player = TestPlayer(T.COLOR.BLUE)

    G = BoardBuilder().create_board_of_size([1]).with_player(player).build()

    for r in range(3):
        ressource_id = str(uuid4())

        G.add_node(ressource_id, type=T.NODE_TYPE.RESSOURCE, ressource=input_)
        G.add_edge(player.color, ressource_id, type=T.EDGE_TYPE.RESSOURCE_OWNERSHIP)

    num_nodes = len(G.nodes())
    num_edges = len(G.edges())
    assert R.get_ressources_of_player_dict(G, player)[input_] == 3

    with pytest.raises(ValueError) as e:
        R.port_trate_4_to_1(G, player, input_, output, raise_on_error=True)

    assert e.value.args[0] == "No enough ressource for 4:1 trate"

    assert len(G.nodes()) == num_nodes
    assert len(G.edges()) == num_edges
    assert output not in R.get_ressources_of_player_dict(G, player)
    assert R.get_ressources_of_player_dict(G, player)[input_] == 3
