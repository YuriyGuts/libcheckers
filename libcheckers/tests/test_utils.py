from libcheckers.utils import (
    index_to_coords,
    coords_to_index,
    get_indexes_between,
    get_lines_of_sight,
)


def test_index_to_coords():
    assert index_to_coords(1) == (1, 2)
    assert index_to_coords(5) == (1, 10)
    assert index_to_coords(6) == (2, 1)
    assert index_to_coords(28) == (6, 5)
    assert index_to_coords(41) == (9, 2)
    assert index_to_coords(45) == (9, 10)
    assert index_to_coords(46) == (10, 1)
    assert index_to_coords(50) == (10, 9)


def test_coords_to_index():
    assert coords_to_index(1, 2) == 1
    assert coords_to_index(1, 10) == 5
    assert coords_to_index(2, 1) == 6
    assert coords_to_index(6, 5) == 28
    assert coords_to_index(9, 2) == 41
    assert coords_to_index(9, 10) == 45
    assert coords_to_index(10, 1) == 46
    assert coords_to_index(10, 9) == 50


def test_get_intermediate_indexes():
    assert get_indexes_between(1, 6) == []
    assert get_indexes_between(1, 12) == [7]
    assert sorted(get_indexes_between(5, 46)) == [10, 14, 19, 23, 28, 32, 37, 41]
    assert sorted(get_indexes_between(7, 23)) == [12, 18]
    assert sorted(get_indexes_between(8, 26)) == [12, 17, 21]
    assert sorted(get_indexes_between(44, 6)) == [11, 17, 22, 28, 33, 39]


def test_get_lines_of_sight_mid_board_limited():
    assert get_lines_of_sight(23, visibility_range=2) == [
        [18, 12],
        [19, 14],
        [28, 32],
        [29, 34],
    ]
    assert get_lines_of_sight(27, visibility_range=1) == [
        [21],
        [22],
        [31],
        [32],
    ]


def test_get_lines_of_sight_mid_board_full():
    assert get_lines_of_sight(28, visibility_range=10) == [
        [22, 17, 11, 6],
        [23, 19, 14, 10, 5],
        [32, 37, 41, 46],
        [33, 39, 44, 50],
    ]


def test_get_lines_of_sight_edge_limited():
    assert get_lines_of_sight(1, visibility_range=2) == [
        [],
        [],
        [6],
        [7, 12],
    ]
    assert get_lines_of_sight(5, visibility_range=2) == [
        [],
        [],
        [10, 14],
        [],
    ]
    assert get_lines_of_sight(46, visibility_range=2) == [
        [],
        [41, 37],
        [],
        [],
    ]
    assert get_lines_of_sight(50, visibility_range=2) == [
        [44, 39],
        [45],
        [],
        [],
    ]
