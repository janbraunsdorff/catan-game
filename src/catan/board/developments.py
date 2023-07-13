from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from catan.player import Player  # pragma: no cover

import catan.board.types as T
from catan.board.ressources import get_ressources_of_player_dict


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


def trade_developement(
    G: T.Board, player: Player, card: Optional[T.DEVELOPMENT_CARDS] = None
):
    check_ressources_for_development(G, player, True)
    # #check if card is avible
    # if card  = None -> random
    # else check if card is aviable -> add
