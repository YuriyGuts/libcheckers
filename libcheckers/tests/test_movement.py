import pytest

from libcheckers import InvalidMoveException
from libcheckers.enum import Player, PieceClass, GameOverReason
from libcheckers.movement import Board, ForwardMove, CaptureMove, ComboCaptureMove


def test_forward_move_to_occupied_square_raises(one_vs_one_men_capture_board):
    board = one_vs_one_men_capture_board
    move = ForwardMove(23, 28)
    with pytest.raises(InvalidMoveException):
        move.apply(board)


def test_forward_move_from_empty_square_raises(one_vs_one_men_capture_board):
    board = one_vs_one_men_capture_board
    move = ForwardMove(1, 6)
    with pytest.raises(InvalidMoveException):
        move.apply(board)


def test_forward_move_man_white_south_raises(one_vs_one_men_capture_board):
    board = one_vs_one_men_capture_board
    move = ForwardMove(28, 33)
    with pytest.raises(InvalidMoveException):
        move.apply(board)


def test_forward_move_man_black_north_raises(one_vs_one_men_capture_board):
    board = one_vs_one_men_capture_board
    move = ForwardMove(23, 18)
    with pytest.raises(InvalidMoveException):
        move.apply(board)


def test_forward_move_king_white_south_accepts(one_vs_one_kings_capture_board):
    board = one_vs_one_kings_capture_board
    move = ForwardMove(28, 33)
    move.apply(board)


def test_forward_move_king_black_north_accepts(one_vs_one_kings_capture_board):
    board = one_vs_one_kings_capture_board
    move = ForwardMove(23, 18)
    move.apply(board)


def test_capture_protected_raises(two_vs_two_protected_kings_board):
    board = two_vs_two_protected_kings_board
    move = CaptureMove(29, 15)
    with pytest.raises(InvalidMoveException):
        move.apply(board)
    move = CaptureMove(29, 20)
    with pytest.raises(InvalidMoveException):
        move.apply(board)
    move = CaptureMove(33, 20)
    with pytest.raises(InvalidMoveException):
        move.apply(board)


def test_capture_ending_in_home_row_promotes():
    board = Board()
    board.add_piece(15, Player.WHITE, PieceClass.MAN)
    board.add_piece(10, Player.BLACK, PieceClass.MAN)
    move = CaptureMove(15, 4)
    new_board = move.apply(board)
    assert new_board.owner[4] == Player.WHITE
    assert new_board.piece_class[4] == PieceClass.KING


def test_man_when_finishing_move_in_home_row_gets_promoted():
    board_before = Board()
    board_before.add_piece(6, Player.WHITE, PieceClass.MAN)
    move = ForwardMove(6, 1)
    board_after = move.apply(board_before)
    assert board_after.owner[1] == Player.WHITE
    assert board_after.piece_class[1] == PieceClass.KING

    board_before = Board()
    board_before.add_piece(41, Player.BLACK, PieceClass.MAN)
    move = ForwardMove(41, 47)
    board_after = move.apply(board_before)
    assert board_after.owner[47] == Player.BLACK
    assert board_after.piece_class[47] == PieceClass.KING


def test_man_when_finishing_capture_in_home_row_gets_promoted():
    board_before = Board()
    board_before.add_piece(12, Player.WHITE, PieceClass.MAN)
    board_before.add_piece(7, Player.BLACK, PieceClass.MAN)
    move = CaptureMove(12, 1)
    board_after = move.apply(board_before)

    assert board_after.owner[1] == Player.WHITE
    assert board_after.piece_class[1] == PieceClass.KING
    assert board_after.owner[7] is None
    assert board_after.piece_class[7] is None

    board_before = Board()
    board_before.add_piece(42, Player.WHITE, PieceClass.MAN)
    board_before.add_piece(37, Player.BLACK, PieceClass.MAN)
    move = CaptureMove(37, 48)
    board_after = move.apply(board_before)

    assert board_after.owner[48] == Player.BLACK
    assert board_after.piece_class[48] == PieceClass.KING
    assert board_after.owner[42] is None
    assert board_after.piece_class[42] is None


def test_man_when_jumping_across_the_edge_does_not_get_promoted():
    board_before = Board()
    board_before.add_piece(11, Player.WHITE, PieceClass.MAN)
    board_before.add_piece(7, Player.BLACK, PieceClass.MAN)
    board_before.add_piece(8, Player.BLACK, PieceClass.MAN)
    move = ComboCaptureMove([CaptureMove(11, 2), CaptureMove(2, 13)])
    board_after = move.apply(board_before)

    assert board_after.owner[13] == Player.WHITE
    assert board_after.piece_class[13] == PieceClass.MAN
    assert board_after.owner[7] is None
    assert board_after.piece_class[7] is None
    assert board_after.owner[8] is None
    assert board_after.piece_class[8] is None

    board_before = Board()
    board_before.add_piece(41, Player.WHITE, PieceClass.MAN)
    board_before.add_piece(42, Player.WHITE, PieceClass.MAN)
    board_before.add_piece(36, Player.BLACK, PieceClass.MAN)
    move = ComboCaptureMove([CaptureMove(36, 47), CaptureMove(47, 38)])
    board_after = move.apply(board_before)

    assert board_after.owner[38] == Player.BLACK
    assert board_after.piece_class[38] == PieceClass.MAN
    assert board_after.owner[41] is None
    assert board_after.piece_class[41] is None
    assert board_after.owner[42] is None
    assert board_after.piece_class[42] is None


def test_get_capturable_pieces_starting_pos_none(starting_board):
    board = starting_board
    for index in range(1, 51):
        assert board.get_capturable_pieces(index) == []


def test_get_capturable_pieces_1v1_men(one_vs_one_men_capture_board):
    board = one_vs_one_men_capture_board
    assert board.get_capturable_pieces(28) == [23]
    assert board.get_capturable_pieces(23) == [28]


def test_get_capturable_pieces_backwards_move(one_vs_one_men_backwards_capture_board):
    board = one_vs_one_men_backwards_capture_board
    assert board.get_capturable_pieces(28) == [23]
    assert board.get_capturable_pieces(23) == [28]


def test_get_capturable_pieces_2v1_kings(two_vs_one_kings_board):
    board = two_vs_one_kings_board
    assert sorted(board.get_capturable_pieces(31)) == [18]
    assert sorted(board.get_capturable_pieces(34)) == [18]
    assert sorted(board.get_capturable_pieces(18)) == [31, 34]


def test_get_capturable_pieces_2v2_protected_kings(two_vs_two_protected_kings_board):
    board = two_vs_two_protected_kings_board
    for index in [29, 33, 24, 20]:
        assert board.get_capturable_pieces(index) == []


def test_get_capturable_pieces_1v1_cornered_kings(one_vs_one_kings_cornered_board):
    board = one_vs_one_kings_cornered_board
    assert board.get_capturable_pieces(5) == []
    assert board.get_capturable_pieces(46) == []


def test_get_capturable_pieces_complex(multiple_capture_options_complex_board):
    board = multiple_capture_options_complex_board
    assert sorted(board.get_capturable_pieces(23)) == [18, 29]


def test_get_movement_destinations(one_vs_one_men_surrender_board):
    board = one_vs_one_men_surrender_board
    assert sorted(board.get_free_movement_destinations(18)) == [22, 23]
    assert sorted(board.get_free_movement_destinations(28)) == [22, 23]


def test_get_movement_destinations_1v1_men(one_vs_one_men_surrender_board):
    board = one_vs_one_men_surrender_board
    assert sorted(board.get_free_movement_destinations(18)) == [22, 23]
    assert sorted(board.get_free_movement_destinations(28)) == [22, 23]


def test_get_movement_destinations_1v1_kings(one_vs_one_kings_cornered_board):
    board = one_vs_one_kings_cornered_board
    assert sorted(board.get_free_movement_destinations(5)) == [10, 14, 19, 23, 28, 32, 37, 41]
    assert sorted(board.get_free_movement_destinations(46)) == [10, 14, 19, 23, 28, 32, 37, 41]


def test_get_movement_destinations_2v1_kings(two_vs_one_kings_board):
    board = two_vs_one_kings_board
    assert sorted(board.get_free_movement_destinations(31)) == [22, 26, 27, 36, 37, 42, 48]
    assert sorted(board.get_free_movement_destinations(34)) == [23, 25, 29, 30, 39, 40, 43, 45, 48]
    assert sorted(board.get_free_movement_destinations(18)) == [1, 4, 7, 9, 12, 13, 22, 23, 27, 29]


def test_get_capture_landing_pos_men(one_vs_one_men_capture_board):
    board = one_vs_one_men_capture_board
    assert board.get_available_capture_landing_positions(23, 28) == [32]
    assert board.get_available_capture_landing_positions(28, 23) == [19]


def test_get_capture_landing_pos_men_backwards(one_vs_one_men_backwards_capture_board):
    board = one_vs_one_men_backwards_capture_board
    assert board.get_available_capture_landing_positions(23, 28) == [32]
    assert board.get_available_capture_landing_positions(28, 23) == [19]


def test_get_capture_landing_pos_kings(two_vs_one_kings_board):
    board = two_vs_one_kings_board
    assert sorted(board.get_available_capture_landing_positions(31, 18)) == [4, 9, 13]
    assert sorted(board.get_available_capture_landing_positions(34, 18)) == [1, 7, 12]
    assert sorted(board.get_available_capture_landing_positions(18, 31)) == [36]
    assert sorted(board.get_available_capture_landing_positions(18, 34)) == [40, 45]


def assert_moves_equal(actual_moves, expected_moves):
    for move in actual_moves:
        assert move in expected_moves
    for move in expected_moves:
        assert move in actual_moves


def test_get_available_moves_starting_pos(starting_board):
    board = starting_board
    actual_moves = board.get_available_moves(Player.WHITE)
    expected_moves = [
        ForwardMove(31, 26),
        ForwardMove(31, 27),
        ForwardMove(32, 27),
        ForwardMove(32, 28),
        ForwardMove(33, 28),
        ForwardMove(33, 29),
        ForwardMove(34, 29),
        ForwardMove(34, 30),
        ForwardMove(35, 30),
    ]
    assert_moves_equal(actual_moves, expected_moves)

    actual_moves = board.get_available_moves(Player.BLACK)
    expected_moves = [
        ForwardMove(16, 21),
        ForwardMove(17, 21),
        ForwardMove(17, 22),
        ForwardMove(18, 22),
        ForwardMove(18, 23),
        ForwardMove(19, 23),
        ForwardMove(19, 24),
        ForwardMove(20, 24),
        ForwardMove(20, 25),
    ]
    assert_moves_equal(actual_moves, expected_moves)


def test_get_available_moves_1v1_men(one_vs_one_men_surrender_board):
    board = one_vs_one_men_surrender_board
    actual_moves = board.get_available_moves(Player.WHITE)
    expected_moves = [
        ForwardMove(28, 22),
        ForwardMove(28, 23),
    ]
    assert_moves_equal(actual_moves, expected_moves)

    actual_moves = board.get_available_moves(Player.BLACK)
    expected_moves = [
        ForwardMove(18, 22),
        ForwardMove(18, 23),
    ]
    assert_moves_equal(actual_moves, expected_moves)


def test_get_available_moves_1v1_men_capture(one_vs_one_men_capture_board):
    board = one_vs_one_men_capture_board
    actual_moves = board.get_available_moves(Player.WHITE)
    expected_moves = [
        CaptureMove(28, 19),
    ]
    assert_moves_equal(actual_moves, expected_moves)

    actual_moves = board.get_available_moves(Player.BLACK)
    expected_moves = [
        CaptureMove(23, 32),
    ]
    assert_moves_equal(actual_moves, expected_moves)


def test_get_available_moves_1v1_men_backwards_capture(one_vs_one_men_backwards_capture_board):
    board = one_vs_one_men_backwards_capture_board
    actual_moves = board.get_available_moves(Player.WHITE)
    expected_moves = [
        CaptureMove(23, 32),
    ]
    assert_moves_equal(actual_moves, expected_moves)

    actual_moves = board.get_available_moves(Player.BLACK)
    expected_moves = [
        CaptureMove(28, 19),
    ]
    assert_moves_equal(actual_moves, expected_moves)


def test_get_available_moves_multiple_options_men(multiple_capture_options_men_board):
    board = multiple_capture_options_men_board
    actual_moves = board.get_available_moves(Player.WHITE)
    expected_moves = [
        CaptureMove(29, 18),
    ]
    assert_moves_equal(actual_moves, expected_moves)

    actual_moves = board.get_available_moves(Player.BLACK)
    expected_moves = [
        ComboCaptureMove([CaptureMove(23, 32), CaptureMove(32, 41)]),
        ComboCaptureMove([CaptureMove(23, 34), CaptureMove(34, 45)]),
    ]
    assert_moves_equal(actual_moves, expected_moves)


def test_get_available_moves_2v1_kings(two_vs_one_kings_board):
    board = two_vs_one_kings_board
    actual_moves = board.get_available_moves(Player.WHITE)
    expected_moves = [
        CaptureMove(31, 13),
        CaptureMove(31, 9),
        CaptureMove(31, 4),
        CaptureMove(34, 12),
        CaptureMove(34, 7),
        CaptureMove(34, 1),
    ]
    assert_moves_equal(actual_moves, expected_moves)

    actual_moves = board.get_available_moves(Player.BLACK)
    expected_moves = [
        CaptureMove(18, 36),
        CaptureMove(18, 40),
        CaptureMove(18, 45),
    ]
    assert_moves_equal(actual_moves, expected_moves)


def test_get_available_moves_insane_combo(insane_king_combo_board):
    board = insane_king_combo_board
    actual_moves = board.get_available_moves(Player.WHITE)
    expected_moves = [
        ComboCaptureMove([
            CaptureMove(1, 29),
            CaptureMove(29, 47),
            CaptureMove(47, 36),
            CaptureMove(36, 9),
            CaptureMove(9, 25),
            CaptureMove(25, 43),
        ])
    ]
    assert_moves_equal(actual_moves, expected_moves)

    actual_moves = board.get_available_moves(Player.BLACK)
    expected_moves = [
        CaptureMove(35, 44),
    ]
    assert_moves_equal(actual_moves, expected_moves)


def test_get_available_moves_1v1_men_cornered(one_vs_one_men_cornered_board):
    board = one_vs_one_men_cornered_board
    actual_moves = board.get_available_moves(Player.WHITE)
    expected_moves = [
        ForwardMove(50, 44),
    ]
    assert_moves_equal(actual_moves, expected_moves)
    assert board.get_available_moves(Player.BLACK) == []


def test_get_available_moves_filled_board(completely_filled_board):
    board = completely_filled_board
    assert board.get_available_moves(Player.WHITE) == []
    assert board.get_available_moves(Player.BLACK) == []


def test_get_available_moves_no_pieces():
    board = Board()
    assert board.get_available_moves(Player.WHITE) == []
    assert board.get_available_moves(Player.BLACK) == []


def test_game_over_still_playable():
    board = Board()
    board.add_piece(13, Player.BLACK, PieceClass.MAN)
    board.add_piece(32, Player.WHITE, PieceClass.MAN)
    assert board.check_game_over(Player.WHITE) is None
    assert board.check_game_over(Player.BLACK) is None


def test_game_over_no_white_pieces():
    board = Board()
    board.add_piece(32, Player.BLACK, PieceClass.MAN)
    assert board.check_game_over(Player.WHITE) == GameOverReason.BLACK_WON


def test_game_over_no_black_pieces():
    board = Board()
    board.add_piece(32, Player.WHITE, PieceClass.MAN)
    assert board.check_game_over(Player.BLACK) == GameOverReason.WHITE_WON


def test_game_over_one_king_each_draw():
    board = Board()
    board.add_piece(13, Player.WHITE, PieceClass.KING)
    board.add_piece(32, Player.BLACK, PieceClass.KING)
    assert board.check_game_over(Player.WHITE) == GameOverReason.DRAW
    assert board.check_game_over(Player.BLACK) == GameOverReason.DRAW


def test_game_over_one_king_each_adjacent_not_draw():
    board = Board()
    board.add_piece(28, Player.WHITE, PieceClass.KING)
    board.add_piece(32, Player.BLACK, PieceClass.KING)
    assert board.check_game_over(Player.WHITE) is None
    assert board.check_game_over(Player.BLACK) is None
