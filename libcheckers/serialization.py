from libcheckers import BoardConfig
from libcheckers.enum import Player, PieceClass
from libcheckers.movement import Board, ForwardMove, CaptureMove, ComboCaptureMove


_player_serializer = {
    Player.BLACK: 'black',
    Player.WHITE: 'white',
}

_piece_class_serializer = {
    PieceClass.MAN: 'man',
    PieceClass.KING: 'king',
}

_player_deserializer = dict(zip(_player_serializer.values(), _player_serializer.keys()))
_piece_class_deserializer = dict(zip(_piece_class_serializer.values(), _piece_class_serializer.keys()))


def load_board(board_dict):
    board = Board()
    for index, square_data in board_dict.items():
        board.owner[int(index)] = load_player(square_data['player'])
        board.piece_class[int(index)] = load_piece_class(square_data['class'])

    return board


def save_board(board):
    board_dict = {}
    for index in range(1, BoardConfig.total_squares + 1):
        if board.owner[index]:
            board_dict[index] = {
                'player': _player_serializer[board.owner[index]],
                'class': _piece_class_serializer[board.piece_class[index]],
            }

    return board_dict


def save_move(move):
    move_data = {}
    if isinstance(move, ForwardMove):
        move_data = {
            'type': 'ForwardMove',
            'startIndex': move.start_index,
            'endIndex': move.end_index,
        }
    elif isinstance(move, CaptureMove):
        move_data = {
            'type': 'CaptureMove',
            'startIndex': move.start_index,
            'endIndex': move.end_index,
        }
    elif isinstance(move, ComboCaptureMove):
        move_data = {
            'type': 'ComboCaptureMove',
            'moves': [save_move(move) for move in move.moves],
        }
    return move_data


def load_move(move_dict):
    if move_dict['type'] == 'ForwardMove':
        return ForwardMove(move_dict['startIndex'], move_dict['endIndex'])
    elif move_dict['type'] == 'CaptureMove':
        return CaptureMove(move_dict['startIndex'], move_dict['endIndex'])
    elif move_dict['type'] == 'ComboCaptureMove':
        return ComboCaptureMove([load_move(move) for move in move_dict['moves']])


def load_player(player_data):
    return _player_deserializer[player_data]


def save_player(player):
    return _player_serializer[player]


def load_piece_class(piece_class_data):
    return _piece_class_deserializer[piece_class_data]


def save_piece_class(piece_class):
    return _piece_class_serializer[piece_class]
