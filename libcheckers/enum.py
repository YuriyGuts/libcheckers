class Player(object):
    WHITE = 1       # White piece
    BLACK = 2       # Black piece
    ZOMBIE = 3      # Special piece type for tracking the captured squares in ComboCaptureMove


class PieceClass(object):
    MAN = 1         # Regular, or "man" piece
    KING = 2        # Crowned, or "king" piece


class GameOverReason(object):
    WHITE_WON = 1   # White player has won the game
    BLACK_WON = 2   # Black player has won the game
    DRAW = 3        # Neither player can win the game
