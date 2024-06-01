import random
import time

def get_available_moves(board, size):
    return [(i, j) for i in range(size) for j in range(size) if board[i][j] == ' ']

def is_winner(board, size, player):
    for i in range(size):
        if all(board[i][j] == player for j in range(size)):
            return True
        if all(board[j][i] == player for j in range(size)):
            return True
    for i in range(size - 4):
        for j in range(size - 4):
            if all(board[i+k][j+k] == player for k in range(5)):
                return True
            if all(board[i+4-k][j+k] == player for k in range(5)):
                return True
    return False

def evaluate(board, size, player, opponent):
    if is_winner(board, size, player):
        return 10000
    elif is_winner(board, size, opponent):
        return -10000

    score = 0

    for row in board:
        score += evaluate_line(row, player, opponent)
    
    for col in range(size):
        column = []
        for row in range(size):
            column.append(board[row][col])
        score += evaluate_line(column, player, opponent)
    
    score += evaluate_all_diagonals(board, size, player, opponent)

    return score

def evaluate_all_diagonals(board, size, player, opponent):
    score = 0
    for d in range(-size + 1, size):
        diagonal1 = get_diagonal(board, size, d, True)
        diagonal2 = get_diagonal(board, size, d, False)
        score += evaluate_line(diagonal1, player, opponent)
        score += evaluate_line(diagonal2, player, opponent)
    return score

def get_diagonal(board, size, offset, top_left_to_bottom_right):
    diagonal = []
    for i in range(max(0, offset), min(size, size + offset)):
        if top_left_to_bottom_right:
            j = i - offset
            if 0 <= j < size:
                diagonal.append(board[i][j])
        else:
            j = size - 1 - (i - offset)
            if 0 <= j < size:
                diagonal.append(board[i][j])
    return diagonal

def evaluate_line(line, player, opponent):
    score = 0
    
    # Define patterns and their corresponding weights
    patterns = {
        player*5: 10000,
        player*4 + ' ': 1000,
        ' ' + player*4: 1000,
        ' ' + player*3 + ' ': 100,
        player + ' ' + player*2: 70,
        player*2 + ' ' + player: 70,
        player*3 + '  ': 50,
        '  ' + player*3: 50,
        player*2 + '   ': 10,
        ' ' + player*2 + '  ': 10,
        '  ' + player*2 + ' ': 10,
        '   ' + player*2: 10,
        player + '    ': 1,
        ' ' + player + '   ': 1,
        '  ' + player + '  ': 1,
        '   ' + player + ' ': 1,
        opponent*5: -10000,
        opponent*4 + ' ': -2000,
        ' ' + opponent*4: -2000,
        opponent*2 + ' ' + opponent: -1000, 
        opponent + ' ' + opponent*2: -1000,  
        ' ' + opponent*3 + ' ': -500,
        opponent*3 + '  ': -500,
        '  ' + opponent*3: -500,
        opponent*2 + '   ': -10,
        ' ' + opponent*2 + '  ': -10,
        '  ' + opponent*2: -10,
        opponent + '    ': -1,
        ' ' + opponent + '   ': -1,
        '  ' + opponent + '  ': -1,
        '   ' + opponent + ' ': -1,
        player*3 + ' ' + player + ' ': 90,
        player + ' ' + player*3 + ' ': 90,
        ' ' + player*3 + ' ' + player: 90,
        player + ' ' + player + ' ' + player: 80,
        ' ' + player + ' ' + player + ' ' + player: 80,
        player*4: 2000,
        player*3: 100,
        player*2: 10,
        opponent*3 + ' ' + opponent: -200,
        opponent + ' ' + opponent*3: -200,
        opponent*4: -2000,
        opponent*3: -100,
        opponent*2: -10,
        opponent + ' ' + player*2: -20,
        player*2 + ' ' + opponent: -20,
        opponent + ' ' + player + ' ' + opponent: -40,
        player*2 + ' ' + opponent*2: -40,
        player*3 + ' ' + opponent: 150,
        opponent + ' ' + player*3: -150,
        player*4 + ' ' + opponent: 4000,
        opponent + ' ' + player*4: -4000,
        player*3 + ' ' + opponent*2: 300,
        opponent*2 + ' ' + player*3: -300,
        player*2 + ' ' + opponent*3: 20,
        opponent*3 + ' ' + player*2: -20,
    }
    
    line_str = ''.join(line)
    
    # Evaluate each pattern and accumulate the score
    for pattern, value in patterns.items():
        score += line_str.count(pattern) * value
    
    return score

transposition_table = {}

def minimax(board, depth, alpha, beta, size, max_depth, start_time, time_limit, player, opponent):
    board_tuple = tuple(map(tuple, board))
    if board_tuple in transposition_table and transposition_table[board_tuple][0] >= depth:
        return transposition_table[board_tuple][1]
    
    if time.time() - start_time > time_limit:
        return evaluate(board, size, player, opponent)

    available_moves = get_available_moves(board, size)
    score = evaluate(board, size, player, opponent)
    
    if abs(score) == 10000 or not available_moves or depth == 0:
        return score

    max_eval = -float('inf') if player == 'o' else float('inf')
    for move in available_moves:
        board[move[0]][move[1]] = player
        eval = -minimax(board, depth - 1, -beta, -alpha, size, max_depth, start_time, time_limit, opponent, player)
        board[move[0]][move[1]] = ' '
        if player == 'o':
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
        else:
            max_eval = min(max_eval, eval)
            beta = min(beta, eval)
        if beta <= alpha:
            break
    
    transposition_table[board_tuple] = (depth, max_eval)
    return max_eval

def find_best_move(board, size, player, opponent, max_depth=5, time_limit=1.0):

    best_value = -float('inf')
    best_move = None
    available_moves = get_available_moves(board, size)
    
    start_time = time.time()

    for move in available_moves:
        board[move[0]][move[1]] = player
        move_value = minimax(board, 0, -float('inf'), float('inf'), size, max_depth, start_time, time_limit, player, opponent)
        board[move[0]][move[1]] = ' '
        if move_value > best_value:
            best_move = move
            best_value = move_value
    
    return best_move

def get_move(board, size, team_roles):
    size = int(size)
    available_moves = get_available_moves(board, size)
    if not available_moves:
        return None
    
    player = team_roles
    opponent = 'x' if team_roles == 'o' else 'o'
    
    best_move = find_best_move(board, size, player, opponent)
    
    if best_move is None:
        return available_moves[random.randint(0, len(available_moves) - 1)]
    else:
        return best_move

