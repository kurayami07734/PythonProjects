"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    player = X
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    Xs, Os = 0, 0
    for row in board:
        for cell in row:
            if cell == X: Xs += 1
            elif cell == O: Os += 1
    
    return X if Xs <= Os else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    empty_cells = set()
    
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == EMPTY:
                empty_cells.add((i, j))
    return empty_cells


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if len(action) != 2:
        raise Exception("Incorrect action")
    if action[0] < 0 or action[0] > 2 or action[1] < 0 or action[1] > 2:
        raise Exception("Out of bounds")
    x, y = action
    board_copy = deepcopy(board)
    if board_copy[x][y] != EMPTY:
        raise Exception("Action Not Available")
    board_copy[x][y] = player(board)
    return board_copy



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(len(board)):
        # Check row
        if board[i][0] == board[i][1] and board[i][1] == board[i][2] and board[i][0] != EMPTY:
            return board[i][0]
        # Check column
        if board[0][i] == board[1][i] and board[1][i] == board[2][i] and board[0][i] != EMPTY:
            return board[0][i]

    # Check diagonal
    if board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[1][1] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] and board[1][1] == board[2][0] and board[1][1] != EMPTY:
        return board[0][2]
    
    return None



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X or winner(board) == O: return True
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X: return 1
    elif winner(board) == O: return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board): return None
    if player(board) == X:
        score = -math.inf
        action = None
        for a in actions(board):
            min_val = minvalue(result(board, a))
            if min_val > score:
                score = min_val
                action = a
        return action
    elif player(board) == O:
        score = math.inf
        action = None
        for a in actions(board):
            max_val = maxvalue(result(board, a))
            if max_val < score:
                score = max_val
                action = a
        return action


def minvalue(board):
    if terminal(board): return utility(board)
    max_val = math.inf
    for a in actions(board):
        max_val = min(max_val, maxvalue(result(board, a)))
    return max_val

def maxvalue(board):
    if terminal(board): return utility(board)
    min_val = -math.inf
    for a in actions(board):
        min_val = max(min_val, minvalue(result(board, a)))
    return min_val