import pytest

from catan.board.graph import BoardBuilder, add_port
from catan.board.types import EDGE_TYPE, NODE_TYPE, PORT_TYPE


def test_create_port():
    board = BoardBuilder().create_board_of_size([1, 2, 1]).build()

    num_edges = len(board.edges())
    num_nodes = len(board.nodes())

    board = add_port(board, port_type=PORT_TYPE.PORT_BRICK, buildings=(100, 101))

    assert len(board.nodes()) == num_nodes + 1
    assert len(board.edges()) == num_edges + 2


def test_create_port_only_one_exsting_nodes():
    board = BoardBuilder().create_board_of_size([1, 2, 1]).build()

    num_edges = len(board.edges())
    num_nodes = len(board.nodes())

    with pytest.raises(ValueError) as e:
        board = add_port(board, port_type=PORT_TYPE.PORT_BRICK, buildings=(100, 404))

    assert len(board.nodes()) == num_nodes
    assert len(board.edges()) == num_edges


def test_create_port_not_exsting_nodes():
    board = BoardBuilder().create_board_of_size([1, 2, 1]).build()

    num_edges = len(board.edges())
    num_nodes = len(board.nodes())

    with pytest.raises(ValueError) as e:
        board = add_port(board, port_type=PORT_TYPE.PORT_BRICK, buildings=(300, 404))

    assert len(board.nodes()) == num_nodes
    assert len(board.edges()) == num_edges


def test_create_port_with_build():
    board = (
        BoardBuilder()
        .create_board_of_size(size=[1])
        .with_port(port_type=PORT_TYPE.PORT_ANY, buildings=(100, 101))
        .build()
    )

    edges = [
        (x1, x2)
        for x1, x2, x in board.edges(data=True)
        if x.get("type", None) == EDGE_TYPE.PORT_TO
    ]

    assert len(edges) == 2
    assert (
        len([x for x, y in board.nodes(data=True) if y["type"] == NODE_TYPE.PORT]) == 1
    )

    assert edges[0][1] == edges[1][1]
    assert edges[0][0] == 100
    assert edges[1][0] == 101
