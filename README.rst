libcheckers
-----------

`International checkers <https://en.wikipedia.org/wiki/International_draughts>`_ gameplay library for the CS301 AI course I teach at UCU.

Basic Usage
===========

.. code-block:: python

    from libcheckers.enum import Player, PieceClass, GameOverReason
    from libcheckers.movement import Board, ForwardMove, CaptureMove, ComboCaptureMove


Creating a new board:

.. code-block:: python

    board = Board()
    board.add_piece(22, Player.BLACK, PieceClass.KING)
    board.add_piece(23, Player.BLACK, PieceClass.MAN)
    board.add_piece(28, Player.WHITE, PieceClass.MAN)


Retrieving square info:

.. code-block:: python

    board.get_player_squares(Player.WHITE)
    # >>> [28]
    
    board.get_player_squares(Player.BLACK)
    # >>> [22, 23]
    
    board.owner[22] == Player.BLACK
    # >>> True
    
    board.piece_class[22] == PieceClass.KING
    # >>> True


Listing available moves:

.. code-block:: python

    board.get_available_moves(Player.WHITE)
    # >>> [Capture: 28 -> 17, Capture: 28 -> 19]

    board.get_available_moves(Player.BLACK)
    # >>> [Capture: 22 -> 33, Capture: 22 -> 39, Capture: 22 -> 44, Capture: 22 -> 50, Capture: 23 -> 32]


Making a move and retrieving the results:

.. code-block:: python

    move = CaptureMove(22, 33)
    new_board = move.apply(board)
    
    new_board.check_game_over(Player.WHITE) == GameOverReason.WHITE_WON
    # >>> False
    
    new_board.check_game_over(Player.WHITE) == GameOverReason.BLACK_WON
    # >>> True
