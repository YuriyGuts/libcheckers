from libcheckers import BoardConfig, InvalidMoveException


# Northwest, Northeast, Southwest, Southeast.
valid_move_offsets = [(-1, -1), (-1, +1), (+1, -1), (+1, +1)]


def index_to_coords(index):
    """
    Transform an index in checkers notation to a (row, column) coordinate pair.
    Rows are numbered top to bottom, columns are numbered left to right.
    """

    row = (index - 1) // BoardConfig.squares_per_row + 1
    if row % 2:
        col = index % BoardConfig.board_dim * 2
    else:
        col = (index - BoardConfig.squares_per_row) % BoardConfig.board_dim * 2 - 1
    return row, col


def coords_to_index(row, col):
    """
    Transform (row, column) coordinate pair to an index in checkers notation.
    """

    return (row - 1) * BoardConfig.squares_per_row + (col - row % 2 + 1) // 2


def get_indexes_between(start_index, end_index):
    """
    Get the indexes of squares between the given start index and end index (exclusive).
    """

    start_row, start_col = index_to_coords(start_index)
    end_row, end_col = index_to_coords(end_index)

    if abs(start_row - end_row) != abs(start_col - end_col):
        msg = 'Non-diagonal move detected ({0} to {1})'.format(start_index, end_index)
        raise InvalidMoveException(msg)

    length = abs(start_row - end_row)
    return [
        coords_to_index(
            start_row + (end_row - start_row) // length * i,
            start_col + (end_col - start_col) // length * i,
        )
        for i in range(1, length)
    ]


def is_black_home_row(index):
    """
    Identify whether the square index belongs to the black player's home row.
    """

    return 1 <= index <= BoardConfig.squares_per_row


def is_white_home_row(index):
    """
    Identify whether the square index belongs to the white player's home row.
    """

    return BoardConfig.total_squares - BoardConfig.squares_per_row < index <= BoardConfig.total_squares


def get_lines_of_sight(index, visibility_range):
    """
    Cast 4 diagonal rays (NW, NE, SW, SE) from the given square index
    using the specified visibility range.

    Parameters
    ----------
    index : int
        The index of the square to cast the lines of sight from.
    visibility_range : int
        Visibility range. For example, 1 will return only the adjacent squares around the piece.

    Returns
    -------
    list
        A list of 4 lists, each containing the indexes of a single diagonal line of sight
        ordered by distance. Empty lines of sight will be represented by empty lists.
    """

    result = [[] for _ in valid_move_offsets]
    current_row, current_col = index_to_coords(index)

    for line_idx, (row_offset, col_offset) in enumerate(valid_move_offsets):
        for step_size in range(1, visibility_range + 1):
            new_row = current_row + step_size * row_offset
            new_col = current_col + step_size * col_offset
            if 1 <= new_row <= BoardConfig.board_dim and 1 <= new_col <= BoardConfig.board_dim:
                result[line_idx].append(coords_to_index(new_row, new_col))

    return result
