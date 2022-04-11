"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = sum(x.count(X) for x in board)
    o_count = sum(o.count(O) for o in board)

    return X if x_count == o_count else O



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    temp = []
    l = len(board)
   
    for i in range(l):
        for j in range(l):
            if board[i][j] == EMPTY:
                temp.append((i,j))
    return temp

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # deep copy
    l = len(board)
    temp = initial_state()
    for i in range(l):
        for j in range(l):
            temp[i][j] = board[i][j]
    temp[action[0]][action[1]] = player(board)
    return temp


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    lst = [[board[0][0], board[0][1], board[0][2]],
           [board[1][0], board[1][1], board[1][2]],
           [board[2][0], board[2][1], board[2][2]],
           [board[0][0], board[1][0], board[2][0]],
           [board[0][1], board[1][1], board[2][1]],
           [board[0][2], board[1][2], board[2][2]],
           [board[0][0], board[1][1], board[2][2]],
           [board[0][2], board[1][1], board[2][0]],]
    
    for row in lst:
        if row.count(X) == 3:
            return X
        elif row.count(O) == 3:
            return O
    return EMPTY

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != EMPTY:
        return True
    else:
        return False if sum(e.count(EMPTY) for e in board) != 0 else True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0
    
def max_value(board):
    v = float("-inf")
    if terminal(board):
        return utility(board)
    for a in actions(board):
        v = max(v, min_value(result(board, a)))  
        if v == 1:
            return v
    return v

def min_value(board):
    v = float("inf")
    if terminal(board):
        return utility(board)
    for a in actions(board):
        v = min(v, max_value(result(board, a)))
        if v == -1:
            return v
    return v
    
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if player(board) == X:
        v = -2
        for a in actions(board):
            r = max(v, min_value(result(board, a)))
            if r > v:
                v = r
                optimal_action = a

    if player(board) == O:
        v = 2
        for a in actions(board):
            r = min(v, max_value(result(board, a)))
            if r < v:
                v = r
                optimal_action = a

    return optimal_action
