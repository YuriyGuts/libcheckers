class BoardConfig(object):
    board_dim = 10
    squares_per_row = board_dim // 2
    total_squares = board_dim ** 2 // 2


class InvalidMoveException(Exception):
    pass
