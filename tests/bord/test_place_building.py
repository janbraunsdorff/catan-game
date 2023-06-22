import networkx as nx
import pytest

import catan.board.types as T
from catan.board.place import PlaceNotAllowed, add_building
from catan.player import Player


class TestPlayer(Player):
    def __init__(self, color: T.COLOR) -> None:
        super().__init__(color)


def test_place_settelments_to_much_settelments(self):
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

    assert len(G.nodes()) == num_nodes
    assert len(G.edges()) == num_edges
