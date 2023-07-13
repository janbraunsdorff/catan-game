from uuid import uuid4

import pytest

import catan.board.ressources as R
import catan.board.types as T
from catan.board.graph import BoardBuilder
from catan.player import Player


def test_add_robber(player_blue):
    G = BoardBuilder().create_board_of_size([1]).with_player(player_blue).build()

    assert G.nodes["robber"]["type"] == T.NODE_TYPE.ROBBER
    assert G.nodes["robber"]["robber_type"] == T.ROBBER.Normal
