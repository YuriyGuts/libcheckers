import pytest

from libcheckers.enum import Player, PieceClass
from libcheckers.movement import Board


@pytest.fixture
def starting_board():
    board = Board()
    for index in range(31, 51):
        board.add_piece(index, Player.WHITE, PieceClass.MAN)
    for index in range(1, 21):
        board.add_piece(index, Player.BLACK, PieceClass.MAN)
    return board


@pytest.fixture
def completely_filled_board():
    board = Board()
    for index in range(26, 51):
        board.add_piece(index, Player.WHITE, PieceClass.MAN)
    for index in range(1, 26):
        board.add_piece(index, Player.BLACK, PieceClass.MAN)
    return board


@pytest.fixture
def one_vs_one_men_capture_board():
    board = Board()
    board.add_piece(28, Player.WHITE, PieceClass.MAN)
    board.add_piece(23, Player.BLACK, PieceClass.MAN)
    return board


@pytest.fixture
def one_vs_one_kings_capture_board():
    board = Board()
    board.add_piece(28, Player.WHITE, PieceClass.KING)
    board.add_piece(23, Player.BLACK, PieceClass.KING)
    return board


@pytest.fixture
def one_vs_one_men_backwards_capture_board():
    board = Board()
    board.add_piece(23, Player.WHITE, PieceClass.MAN)
    board.add_piece(28, Player.BLACK, PieceClass.MAN)
    return board


@pytest.fixture
def one_vs_one_men_surrender_board():
    board = Board()
    board.add_piece(28, Player.WHITE, PieceClass.MAN)
    board.add_piece(18, Player.BLACK, PieceClass.MAN)
    return board


@pytest.fixture
def one_vs_one_men_cornered_board():
    board = Board()
    board.add_piece(50, Player.WHITE, PieceClass.MAN)
    board.add_piece(45, Player.BLACK, PieceClass.MAN)
    return board


@pytest.fixture
def two_vs_one_kings_board():
    board = Board()
    board.add_piece(31, Player.WHITE, PieceClass.KING)
    board.add_piece(34, Player.WHITE, PieceClass.KING)
    board.add_piece(18, Player.BLACK, PieceClass.KING)
    return board


@pytest.fixture
def two_vs_two_protected_kings_board():
    board = Board()
    board.add_piece(29, Player.WHITE, PieceClass.KING)
    board.add_piece(33, Player.WHITE, PieceClass.KING)
    board.add_piece(24, Player.BLACK, PieceClass.KING)
    board.add_piece(20, Player.BLACK, PieceClass.KING)
    return board


@pytest.fixture
def one_vs_one_kings_cornered_board():
    board = Board()
    board.add_piece(46, Player.WHITE, PieceClass.KING)
    board.add_piece(5, Player.BLACK, PieceClass.KING)
    return board


@pytest.fixture
def multiple_capture_options_men_board():
    board = Board()
    board.add_piece(23, Player.BLACK, PieceClass.MAN)
    board.add_piece(28, Player.WHITE, PieceClass.MAN)
    board.add_piece(37, Player.WHITE, PieceClass.MAN)
    board.add_piece(29, Player.WHITE, PieceClass.MAN)
    board.add_piece(40, Player.WHITE, PieceClass.MAN)
    board.add_piece(19, Player.WHITE, PieceClass.MAN)
    return board


@pytest.fixture
def multiple_capture_options_complex_board():
    board = Board()
    board.add_piece(23, Player.BLACK, PieceClass.KING)
    board.add_piece(28, Player.BLACK, PieceClass.MAN)
    board.add_piece(18, Player.WHITE, PieceClass.MAN)
    board.add_piece(7, Player.WHITE, PieceClass.MAN)
    board.add_piece(19, Player.WHITE, PieceClass.MAN)
    board.add_piece(14, Player.WHITE, PieceClass.MAN)
    board.add_piece(37, Player.WHITE, PieceClass.MAN)
    board.add_piece(29, Player.WHITE, PieceClass.MAN)
    return board


@pytest.fixture
def insane_king_combo_board():
    # From Wikipedia GIF: https://en.wikipedia.org/wiki/International_draughts
    board = Board()
    board.add_piece(1, Player.WHITE, PieceClass.KING)
    board.add_piece(40, Player.WHITE, PieceClass.MAN)
    board.add_piece(48, Player.WHITE, PieceClass.MAN)
    board.add_piece(7, Player.BLACK, PieceClass.MAN)
    board.add_piece(13, Player.BLACK, PieceClass.MAN)
    board.add_piece(20, Player.BLACK, PieceClass.MAN)
    board.add_piece(35, Player.BLACK, PieceClass.MAN)
    board.add_piece(39, Player.BLACK, PieceClass.MAN)
    board.add_piece(41, Player.BLACK, PieceClass.MAN)
    board.add_piece(42, Player.BLACK, PieceClass.MAN)
    return board
