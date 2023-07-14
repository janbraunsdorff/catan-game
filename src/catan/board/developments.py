from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Optional

if TYPE_CHECKING:
    from catan.player import Player  # pragma: no cover

import random
from collections import Counter

import catan.board.types as T
from catan.board.ressources import (
    get_ressources_of_player_dict,
    remove_ressource_from_player,
)


def check_ressources_for_development(G: T.Board, player: Player, raise_on_error=False):
    ressource = get_ressources_of_player_dict(G, player)
    error = ""
    if ressource.get(T.RESSOURCE.Wool, 0) < 1:
        error = "Not enough resources available"

    if ressource.get(T.RESSOURCE.Ore, 0) < 1:
        error = "Not enough resources available"

    if ressource.get(T.RESSOURCE.Grain, 0) < 1:
        error = "Not enough resources available"

    if len(error) == 0:
        return True

    if raise_on_error:
        raise ValueError(error)

    return False


def check_cards(
    G: T.Board, card: Optional[T.DEVELOPMENT_CARDS] = None, raise_on_error: bool = False
):
    error = ""
    cards = [
        y["development_type"]
        for x, y in G.nodes(data=True)
        if y["type"] == T.NODE_TYPE.DEVELOPEMENT and len(G.edges(x)) == 0
    ]

    if len(cards) == 0:
        error = "No cards left"

    if card != None and card not in cards:
        error = "Requested card not longer exists"

    if len(error) == 0:
        return True

    if raise_on_error:
        raise ValueError(error)

    return False


def get_development_cards_of_player_dict(
    G: T.Board, player: Player
) -> Dict[T.DEVELOPMENT_CARDS, int]:
    ownerships = [
        v
        for u, v, data in G.edges(data=True)
        if data["type"] == T.EDGE_TYPE.DEVELOPMENT_OWNERSHIP
        and data["owner"] == player.color
    ]
    development_types = [
        G.nodes[ownership]["development_type"] for ownership in ownerships
    ]
    return {k: x for k, x in Counter(development_types).items()}


def trade_developement(
    G: T.Board, player: Player, card: Optional[T.DEVELOPMENT_CARDS] = None
):
    check_ressources_for_development(G, player, True)
    check_cards(G, card, True)

    if card:
        req_card = [
            x
            for x, y in G.nodes(data=True)
            if y["type"] == T.NODE_TYPE.DEVELOPEMENT
            and len(G.edges(x)) == 0
            and y["development_type"] == card
        ][0]
    else:
        req_card = random.choice(
            [
                x
                for x, y in G.nodes(data=True)
                if y["type"] == T.NODE_TYPE.DEVELOPEMENT and len(G.edges(x)) == 0
            ]
        )

    G.add_edge(
        player.color,
        req_card,
        type=T.EDGE_TYPE.DEVELOPMENT_OWNERSHIP,
        owner=player.color,
    )

    remove_ressource_from_player(G, player, T.RESSOURCE.Wool)
    remove_ressource_from_player(G, player, T.RESSOURCE.Grain)
    remove_ressource_from_player(G, player, T.RESSOURCE.Ore)
