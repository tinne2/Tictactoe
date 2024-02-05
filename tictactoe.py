import copy

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
    Returns which player's turn it is.
    """
    # Count the number of X's and O's on the board
    num_X = sum(row.count(X) for row in board)
    num_O = sum(row.count(O) for row in board)

    # X goes first if the number of X's is equal to or less than the number of O's
    return X if num_X <= num_O else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making a move (i, j) on the board.
    """
    i, j = action
    if board[i][j] != EMPTY:
        raise Exception("Invalid action")

    new_board = copy.deepcopy(board)
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game if there is one (X, O, or None).
    """
    # Check rows, columns, and diagonals for three-in-a-row
    for row in board:
        if all(cell == row[0] for cell in row) and row[0] != EMPTY:
            return row[0]
    for col in range(3):
        if all(board[row][col] == board[0][col] for row in range(3)) and board[0][col] != EMPTY:
            return board[0][col]
    if all(board[i][i] == board[0][0] for i in range(3)) and board[0][0] != EMPTY:
        return board[0][0]
    if all(board[i][2 - i] == board[0][2] for i in range(3)) and board[0][2] != EMPTY:
        return board[0][2]

    # If no winner, return None
    return None


def terminal(board):
    """
    Returns True if the game is over, False otherwise.
    """
    return winner(board) is not None or all(all(cell is not EMPTY for cell in row) for row in board)


def utility(board):
    """
    Returns the utility of the terminal board.
    """
    winner_player = winner(board)
    if winner_player == X:
        return 1
    elif winner_player == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal move for the player to move on the board.
    """
    if terminal(board):
        return None

    player_turn = player(board)
    if player_turn == X:
        max_utility = -float('inf')
        best_action = None
        for action in actions(board):
            next_state = result(board, action)
            action_utility = min_value(next_state)
            if action_utility > max_utility:
                max_utility = action_utility
                best_action = action
        return best_action
    else:
        min_utility = float('inf')
        best_action = None
        for action in actions(board):
            next_state = result(board, action)
            action_utility = max_value(next_state)
            if action_utility < min_utility:
                min_utility = action_utility
                best_action = action
        return best_action


def min_value(board):
    if terminal(board):
        return utility(board)
    v = float('inf')
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v


def max_value(board):
    if terminal(board):
        return utility(board)
    v = -float('inf')
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v
