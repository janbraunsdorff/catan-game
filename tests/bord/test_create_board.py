from catan.bord.graph import create_board


def test_lol():
    assert create_board([1, 21]) == [1, 21]
