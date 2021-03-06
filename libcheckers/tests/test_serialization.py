from libcheckers.enum import Player, PieceClass, GameOverReason
from libcheckers.movement import ForwardMove, CaptureMove, ComboCaptureMove
from libcheckers.serialization import (
    load_board,
    save_board,
    load_move,
    save_move,
    load_player,
    save_player,
    load_piece_class,
    save_piece_class,
    load_game_over_reason,
    save_game_over_reason,
)


def test_deserialize_board():
    payload = {
        19: {'player': 'black', 'class': 'king'},
        23: {'player': 'white', 'class': 'man'},
        24: {'player': 'white', 'class': 'man'},
    }
    board = load_board(payload)
    assert sorted(board.get_player_squares(Player.WHITE)) == [23, 24]
    assert sorted(board.get_player_squares(Player.BLACK)) == [19]
    assert board.piece_class[23] == PieceClass.MAN
    assert board.piece_class[24] == PieceClass.MAN
    assert board.piece_class[19] == PieceClass.KING


def test_serialize_board():
    payload = {
        19: {'player': 'black', 'class': 'king'},
        23: {'player': 'white', 'class': 'man'},
        24: {'player': 'white', 'class': 'man'},
    }
    board = load_board(payload)
    saved_board = save_board(board)
    reloaded_board = load_board(saved_board)
    assert str(board) == str(reloaded_board)


def test_serialize_forward_move():
    move = ForwardMove(1, 6)
    assert load_move(save_move(move)) == move


def test_serialize_capture_move():
    move = CaptureMove(1, 12)
    assert load_move(save_move(move)) == move


def test_serialize_combo_capture_move():
    move = ComboCaptureMove([CaptureMove(1, 12), CaptureMove(12, 3), CaptureMove(3, 14)])
    assert load_move(save_move(move)) == move


def test_serialize_player():
    assert load_player(save_player(Player.WHITE)) == Player.WHITE
    assert load_player(save_player(Player.BLACK)) == Player.BLACK


def test_serialize_piece_class():
    assert load_piece_class(save_piece_class(PieceClass.MAN)) == PieceClass.MAN
    assert load_piece_class(save_piece_class(PieceClass.KING)) == PieceClass.KING


def test_serialize_game_over_reason():
    assert load_game_over_reason(save_game_over_reason(GameOverReason.WHITE_WON)) == GameOverReason.WHITE_WON
    assert load_game_over_reason(save_game_over_reason(GameOverReason.BLACK_WON)) == GameOverReason.BLACK_WON
    assert load_game_over_reason(save_game_over_reason(GameOverReason.DRAW)) == GameOverReason.DRAW
