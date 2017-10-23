from abc import abstractmethod
from collections import deque
from copy import deepcopy

from libcheckers import BoardConfig, InvalidMoveException
from libcheckers.enum import Player, PieceClass, GameOverReason
from libcheckers.utils import (
    index_to_coords,
    coords_to_index,
    get_indexes_between,
    get_lines_of_sight,
    is_black_home_row,
    is_white_home_row,
)


class BaseMove(object):
    @abstractmethod
    def apply(self, board):
        return board

    @abstractmethod
    def __eq__(self, other):
        return False

    @abstractmethod
    def __repr__(self):
        return super(BaseMove, self).__repr__()


class ForwardMove(BaseMove):
    def __init__(self, start_index, end_index):
        self.start_index = start_index
        self.end_index = end_index

    def apply(self, board):
        if not board.owner[self.start_index]:
            msg = 'Cannot move from an empty square ({0})'.format(self.start_index)
            raise InvalidMoveException(msg)
        if board.owner[self.end_index]:
            msg = 'Cannot move to a non-empty square ({0})'.format(self.end_index)
            raise InvalidMoveException(msg)
        is_backward_move = (
            (board.owner[self.start_index] == Player.WHITE and self.end_index > self.start_index) or
            (board.owner[self.start_index] == Player.BLACK and self.end_index < self.start_index)
        )
        if is_backward_move and board.piece_class[self.start_index] != PieceClass.KING:
            msg = 'Cannot freely move backwards unless the piece is a king'
            raise InvalidMoveException(msg)

        new_board = board.clone()
        new_board.move_piece(self.start_index, self.end_index)
        return new_board

    def __eq__(self, other):
        return (isinstance(other, ForwardMove) and
                self.start_index == other.start_index and
                self.end_index == other.end_index)

    def __repr__(self):
        return 'Move: {0} -> {1}'.format(self.start_index, self.end_index)


class CaptureMove(BaseMove):
    def __init__(self, start_index, end_index):
        self.start_index = start_index
        self.end_index = end_index

    def apply(self, board):
        path_indexes = get_indexes_between(self.start_index, self.end_index)
        own_color = board.owner[self.start_index]

        own_path_squares = [
            index
            for index in path_indexes
            if board.owner[index] == own_color
        ]
        opponent_path_squares = [
            index
            for index in path_indexes
            if board.owner[index] and board.owner[index] != own_color
        ]

        if len(own_path_squares) > 0:
            msg = 'Cannot capture when own pieces are in the way: {0}'
            raise InvalidMoveException(msg.format(', '.join(str(index) for index in own_path_squares)))
        if len(opponent_path_squares) != 1:
            msg = 'Cannot capture: must have exactly one opponent piece along the way'
            raise InvalidMoveException(msg)
        if not board.owner[self.start_index]:
            msg = 'Cannot move from an empty square ({0})'.format(self.start_index)
            raise InvalidMoveException(msg)
        if board.owner[self.end_index]:
            msg = 'Cannot move to a non-empty square ({0})'.format(self.end_index)
            raise InvalidMoveException(msg)

        new_board = board.clone()
        new_board.move_piece(self.start_index, self.end_index)
        new_board.remove_piece(opponent_path_squares[0])
        return new_board

    def __eq__(self, other):
        return (isinstance(other, CaptureMove) and
                self.start_index == other.start_index and
                self.end_index == other.end_index)

    def __repr__(self):
        return 'Capture: {0} -> {1}'.format(self.start_index, self.end_index)


class ComboCaptureMove(BaseMove):
    def __init__(self, moves):
        self.moves = moves

    def apply(self, board):
        new_board = board
        for i, move in enumerate(self.moves):
            # According to the rules, men should not be promoted when merely passing through
            # the home row. They actually need to finish the move there to be promoted.
            old_class = new_board.piece_class[move.start_index]
            new_board = move.apply(new_board)

            # Restore the piece class if it was "accidentally" promoted in between the moves.
            if i < len(self.moves) - 1:
                new_board.piece_class[move.end_index] = old_class

        return new_board

    def __eq__(self, other):
        return (isinstance(other, ComboCaptureMove) and
                len(self.moves) == len(other.moves) and
                all(self.moves[i] == other.moves[i] for i in range(len(self.moves))))

    def __repr__(self):
        return 'Combo x{0}: [{1}]'.format(len(self.moves), ', '.join(str(move) for move in self.moves))


class Board(object):
    def __init__(self):
        self.owner = [None] * (BoardConfig.total_squares + 1)
        self.piece_class = [None] * (BoardConfig.total_squares + 1)

    def move_piece(self, start_index, end_index):
        self.owner[end_index] = self.owner[start_index]
        self.owner[start_index] = None

        self.piece_class[end_index] = self.piece_class[start_index]
        self.piece_class[start_index] = None

        # Promote the piece if it has reached the opponent's home row.
        if self.owner[end_index] == Player.WHITE and is_black_home_row(end_index):
            self.piece_class[end_index] = PieceClass.KING
        if self.owner[end_index] == Player.BLACK and is_white_home_row(end_index):
            self.piece_class[end_index] = PieceClass.KING

    def add_piece(self, index, player, piece_class):
        self.owner[index] = player
        self.piece_class[index] = piece_class

    def remove_piece(self, index):
        self.owner[index] = None
        self.piece_class[index] = None

    def get_player_squares(self, player):
        return [
            index
            for index in range(1, BoardConfig.total_squares + 1)
            if self.owner[index] == player
        ]

    def get_free_movement_destinations(self, index):
        own_color = self.owner[index]
        own_class = self.piece_class[index]

        visibility_range = BoardConfig.board_dim if own_class == PieceClass.KING else 1
        lines_of_sight = get_lines_of_sight(index, visibility_range)

        # Men can only move forward, and the direction of forward depends on the color.
        if own_class == PieceClass.MAN and own_color == Player.WHITE:
            lines_of_sight = lines_of_sight[:2]
        if own_class == PieceClass.MAN and own_color == Player.BLACK:
            lines_of_sight = lines_of_sight[-2:]

        result = []
        for line in lines_of_sight:
            for i in range(0, len(line)):
                # Cannot move beyond another piece if not capturing.
                if self.owner[line[i]]:
                    break
                result.append(line[i])

        return result

    def get_capturable_pieces(self, index):
        own_color = self.owner[index]
        own_class = self.piece_class[index]

        visibility_range = BoardConfig.board_dim if own_class == PieceClass.KING else 2
        lines_of_sight = get_lines_of_sight(index, visibility_range)

        result = []
        for line in lines_of_sight:
            for i in range(0, len(line) - 1):
                # Cannot capture protected pieces.
                if self.owner[line[i]] and self.owner[line[i + 1]]:
                    break
                # Can only capture if the square following the piece is empty.
                if self.owner[line[i]] and self.owner[line[i]] != own_color and not self.owner[line[i + 1]]:
                    result.append(line[i])

        return result

    def get_available_capture_landing_positions(self, attacker_index, capture_index):
        own_class = self.piece_class[attacker_index]

        attacker_row, attacker_col = index_to_coords(attacker_index)
        capture_row, capture_col = index_to_coords(capture_index)

        # Calculate the unit movement vector.
        movement_row = (capture_row - attacker_row) // abs(capture_row - attacker_row)
        movement_col = (capture_col - attacker_col) // abs(capture_col - attacker_col)

        result = []
        current_row = capture_row + movement_row
        current_col = capture_col + movement_col

        if own_class == PieceClass.MAN:
            return [coords_to_index(current_row, current_col)]

        # Kings can make arbitrarily long jumps as long as they capture only one piece.
        while 1 <= current_row <= BoardConfig.board_dim and 1 <= current_col <= BoardConfig.board_dim:
            current_index = coords_to_index(current_row, current_col)
            if not self.owner[current_index]:
                result.append(current_index)
                current_row = current_row + movement_row
                current_col = current_col + movement_col
            else:
                break

        return result

    def get_capture_sequence_candidates(self, player):
        player_squares = self.get_player_squares(player)

        # Check if there are any pieces in our line of sight that can be captured.
        attack_options = []
        for attacker in player_squares:
            attack_options.extend([
                (attacker, target)
                for target in self.get_capturable_pieces(attacker)
            ])

        # Run a tree traversal (BFS) to find all capture sequences, and choose the longest ones.
        capture_sequences = []

        # Each item in the queue is a 3-tuple: (board, move, previous moves).
        queue = deque()

        # Initial queue items: first step in each possible sequence.
        for attacker, target in attack_options:
            queue.extend([
                (self, CaptureMove(attacker, landing), [])
                for landing in self.get_available_capture_landing_positions(attacker, target)
            ])

        # Main search queue.
        while queue:
            board_before, move, prev_moves = queue.popleft()
            board_after = move.apply(board_before)
            next_attack_options = [
                (move.end_index, target)
                for target in board_after.get_capturable_pieces(move.end_index)
            ]

            # Terminal position, nothing more to capture.
            if not next_attack_options:
                capture_sequences.append(prev_moves + [move])

            # Search deeper for the consecutive captures.
            for attacker, target in next_attack_options:
                queue.extend([
                    (board_after, CaptureMove(attacker, landing), prev_moves + [move])
                    for landing in board_after.get_available_capture_landing_positions(attacker, target)
                ])

        return capture_sequences

    def get_available_moves(self, player):
        result = []
        capture_sequences = self.get_capture_sequence_candidates(player)

        if not capture_sequences:
            # There are no pieces we must capture. Free movement is allowed.
            for source in self.get_player_squares(player):
                result.extend([
                    ForwardMove(source, destination)
                    for destination in self.get_free_movement_destinations(source)
                ])
        else:
            # There's a piece we must capture. Rules demand we capture as many as possible.
            max_seq_length = max(len(seq) for seq in capture_sequences)
            result.extend([
                ComboCaptureMove(seq) if len(seq) > 1 else seq[0]
                for seq in capture_sequences
                if len(seq) == max_seq_length
            ])

        return result

    def check_game_over(self, player_turn):
        white_moves = self.get_available_moves(Player.WHITE)
        black_moves = self.get_available_moves(Player.BLACK)

        # If a player is unable to move, they lose.
        if player_turn == Player.WHITE and not white_moves:
            return GameOverReason.BLACK_WON
        if player_turn == Player.BLACK and not black_moves:
            return GameOverReason.WHITE_WON

        # If both players have only one king left, the game is a draw.
        white_squares = self.get_player_squares(Player.WHITE)
        black_squares = self.get_player_squares(Player.BLACK)
        only_one_king_each = (
            len(white_squares) == 1 and
            len(black_squares) == 1 and
            self.piece_class[white_squares[0]] == PieceClass.KING and
            self.piece_class[black_squares[0]] == PieceClass.KING and
            not self.get_capturable_pieces(white_squares[0]) and
            not self.get_capturable_pieces(black_squares[0])
        )
        if only_one_king_each:
            return GameOverReason.DRAW

        return None

    def clone(self):
        return deepcopy(self)

    def __repr__(self):
        return 'White: {0} | Black: {1}'.format(
            ', '.join(str(idx) for idx in self.get_player_squares(Player.WHITE)),
            ', '.join(str(idx) for idx in self.get_player_squares(Player.BLACK)),
        )
