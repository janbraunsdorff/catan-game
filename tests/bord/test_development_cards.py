import pytest

import catan.board.types as T
from catan.board.developments import (
    check_ressources_for_development,
    trade_developement,
)
from catan.board.graph import BoardBuilder
from catan.board.ressources import add_ressources_to_player


@pytest.mark.parametrize(
    "ressources",
    [
        [T.RESSOURCE.Wool, T.RESSOURCE.Grain],
        [T.RESSOURCE.Ore, T.RESSOURCE.Grain],
        [T.RESSOURCE.Ore, T.RESSOURCE.Wool],
    ],
)
def test_check_less_ressources_not_raise(player_blue, ressources):
    G = BoardBuilder().create_board_of_size([1]).with_player(player_blue).build()
    add_ressources_to_player(G, player_blue, ressources)

    res = check_ressources_for_development(G, player_blue)

    assert res == False


@pytest.mark.parametrize(
    "ressources",
    [
        [T.RESSOURCE.Wool, T.RESSOURCE.Grain, T.RESSOURCE.Ore],
    ],
)
def test_check_ressources_not_raise(player_blue, ressources):
    G = BoardBuilder().create_board_of_size([1]).with_player(player_blue).build()
    add_ressources_to_player(G, player_blue, ressources)

    res = check_ressources_for_development(G, player_blue)

    assert res == True


@pytest.mark.parametrize(
    "ressources",
    [
        [T.RESSOURCE.Wool, T.RESSOURCE.Grain],
        [T.RESSOURCE.Ore, T.RESSOURCE.Grain],
        [T.RESSOURCE.Ore, T.RESSOURCE.Wool],
    ],
)
def test_add_random_development_card_not_enough_ressources(player_blue, ressources):
    G = BoardBuilder().create_board_of_size([1]).with_player(player_blue).build()
    add_ressources_to_player(G, player_blue, ressources)

    with pytest.raises(ValueError) as e:
        trade_developement(G, player_blue)

    assert e.value.args[0] == "Not enough resources available"
