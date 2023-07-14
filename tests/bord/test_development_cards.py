from uuid import uuid4

import pytest

import catan.board.types as T
from catan.board.developments import (
    check_cards,
    check_ressources_for_development,
    get_development_cards_of_player_dict,
    trade_developement,
)
from catan.board.graph import BoardBuilder
from catan.board.ressources import (
    add_ressources_to_player,
    get_ressources_of_player_list,
)


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


def test_no_develpment_cards_left(player_blue):
    G = BoardBuilder().create_board_of_size([1]).with_player(player_blue).build()
    add_ressources_to_player(
        G, player_blue, [T.RESSOURCE.Wool, T.RESSOURCE.Grain, T.RESSOURCE.Ore]
    )

    cards = [x for x, y in G.nodes(data=True) if y["type"] == T.NODE_TYPE.DEVELOPEMENT]
    for c in cards:
        G.remove_node(c)

    with pytest.raises(ValueError) as e:
        trade_developement(G, player_blue)

    assert e.value.args[0] == "No cards left"


def test_no_specific_card_present(player_blue):
    G = BoardBuilder().create_board_of_size([1]).with_player(player_blue).build()
    add_ressources_to_player(
        G, player_blue, [T.RESSOURCE.Wool, T.RESSOURCE.Grain, T.RESSOURCE.Ore]
    )

    cards = [x for x, y in G.nodes(data=True) if y["type"] == T.NODE_TYPE.DEVELOPEMENT]
    for c in cards:
        G.remove_node(c)

    G.add_node(
        str(uuid4()),
        type=T.NODE_TYPE.DEVELOPEMENT,
        development_type=T.DEVELOPMENT_CARDS.MONOPOL,
    )

    with pytest.raises(ValueError) as e:
        trade_developement(G, player_blue, T.DEVELOPMENT_CARDS.KNIGHT)

    assert e.value.args[0] == "Requested card not longer exists"


def test_no_specific_card_present_not_raise(player_blue):
    G = BoardBuilder().create_board_of_size([1]).with_player(player_blue).build()
    add_ressources_to_player(
        G, player_blue, [T.RESSOURCE.Wool, T.RESSOURCE.Grain, T.RESSOURCE.Ore]
    )

    cards = [x for x, y in G.nodes(data=True) if y["type"] == T.NODE_TYPE.DEVELOPEMENT]
    for c in cards:
        G.remove_node(c)

    G.add_node(
        str(uuid4()),
        type=T.NODE_TYPE.DEVELOPEMENT,
        development_type=T.DEVELOPMENT_CARDS.MONOPOL,
    )

    assert check_cards(G, T.DEVELOPMENT_CARDS.KNIGHT) == False


def test_card_is_taken_to_other_player(player_blue, player_red):
    G = (
        BoardBuilder()
        .create_board_of_size([1])
        .with_player(player_blue)
        .with_player(player_red)
        .build()
    )
    add_ressources_to_player(
        G, player_blue, [T.RESSOURCE.Wool, T.RESSOURCE.Grain, T.RESSOURCE.Ore]
    )

    cards = [x for x, y in G.nodes(data=True) if y["type"] == T.NODE_TYPE.DEVELOPEMENT]
    for c in cards:
        G.remove_node(c)

    card_idx = str(uuid4())

    G.add_node(
        card_idx,
        type=T.NODE_TYPE.DEVELOPEMENT,
        development_type=T.DEVELOPMENT_CARDS.MONOPOL,
    )

    G.add_edge(player_blue.color, card_idx, type=T.EDGE_TYPE.DEVELOPMENT_OWNERSHIP)

    with pytest.raises(ValueError) as e:
        trade_developement(G, player_blue)

    assert e.value.args[0] == "No cards left"


def test_add_specific_card_to_player(player_blue):
    G = BoardBuilder().create_board_of_size([1]).with_player(player_blue).build()
    add_ressources_to_player(
        G, player_blue, [T.RESSOURCE.Wool, T.RESSOURCE.Grain, T.RESSOURCE.Ore]
    )

    trade_developement(G, player_blue, T.DEVELOPMENT_CARDS.INVENTION)

    assert T.DEVELOPMENT_CARDS.INVENTION in get_development_cards_of_player_dict(
        G, player_blue
    )
    assert (
        get_development_cards_of_player_dict(G, player_blue)[
            T.DEVELOPMENT_CARDS.INVENTION
        ]
        == 1
    )


def test_add_random_card_to_player(player_blue):
    G = BoardBuilder().create_board_of_size([1]).with_player(player_blue).build()
    add_ressources_to_player(
        G, player_blue, [T.RESSOURCE.Wool, T.RESSOURCE.Grain, T.RESSOURCE.Ore]
    )

    trade_developement(G, player_blue)

    assert len(get_development_cards_of_player_dict(G, player_blue)) == 1


def test_remove_ressources(player_blue):
    G = BoardBuilder().create_board_of_size([1]).with_player(player_blue).build()
    add_ressources_to_player(
        G, player_blue, [T.RESSOURCE.Wool, T.RESSOURCE.Grain, T.RESSOURCE.Ore]
    )

    trade_developement(G, player_blue)

    assert len(get_ressources_of_player_list(G, player_blue)) == 0
