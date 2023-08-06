import catan.board.types as T
from catan.board.graph import BoardBuilder, print

board = BoardBuilder().create_board_of_size([3, 4, 5, 4, 3]).build()
print(board)
