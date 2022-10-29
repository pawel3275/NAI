import random

piece_score = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "P": 1}
CHECKMATE_SCORE = 1000
STALEMATE_SCORE = 0
DEPTH = 2


def find_random_move(valid_moves):
    """Returns the random move from available moves in the log

    Args:
        valid_moves (list): List of all possible valid moves for a given palyer.

    Returns:
        list: List of random valid moves for a given palyer.
    """
    return valid_moves[random.randint(0, len(valid_moves)-1)]


def find_best_move_min_max_no_recursion(game_context, valid_moves):
    """Finds the best possible move by the given values of the chess piece.

    Algorithm of min max without recursion.

    Args:
        game_context (GameContext): Context of the game object.
        valid_moves (list): listt of possible moves.

    Returns:
        Move: Move object with the best move possible.
    """
    turn_multiplier = 1 if game_context.white_to_move else -1
    opponent_min_max_score = CHECKMATE_SCORE
    best_move = None
    random.shuffle(valid_moves)
    for player_move in valid_moves:
        game_context.make_move(player_move)
        opponent_moves = game_context.get_valid_moves()

        if game_context.checkmate:
            opponent_max_score = -CHECKMATE_SCORE
        elif game_context.stalemate:
            opponent_max_score = STALEMATE_SCORE
        else:
            opponent_max_score = -CHECKMATE_SCORE
            for opponent_move in opponent_moves:
                game_context.make_move(opponent_move)
                #opponent_moves = game_context.get_valid_moves()
                if game_context.checkmate:
                    score = -turn_multiplier * CHECKMATE_SCORE
                elif game_context.stalemate:
                    score = STALEMATE_SCORE
                else:
                    score = -turn_multiplier * score_material(game_context.board)
                if score > opponent_max_score:
                    opponent_max_score = score
                game_context.undo_move()
        if opponent_max_score < opponent_min_max_score:
            opponent_min_max_score = opponent_max_score
            best_move = player_move

        game_context.undo_move()
    return best_move


def score_material(board):
    """Calculates the score for the each move given. (Loss function)

    Args:
        board (string matrix): board matrix

    Returns:
        int: score
    """
    score = 0
    for row in board:
        for square in row:
            if square[0] == "w":
                score += piece_score[square[1]]
            elif square[0] == "b":
                score -= piece_score[square[1]]

    return score


'''
    Min max (non-recurse) to find the best available move
'''


def find_best_move(game_context, valid_moves):
    """Different implementations for finding the best move for the AI.

    Args:
        game_context (GameContext): context of the game
        valid_moves (list): list of possible moves

    Returns:
        Move: object containing the next move
    """
    global next_move
    next_move = None
    random.shuffle(valid_moves)
    # uncomment below for min max
    # find_move_min_max(game_context, valid_moves, DEPTH)  
    
    # uncomment below for nega max
    # find_move_nega_max(game_context, valid_moves, DEPTH, 1 if game_context.white_to_move else -1) 

    # uncomment below for nega max alpha beta pruning
    find_move_nega_max_alpha_beta_pruning(game_context, valid_moves, DEPTH, -CHECKMATE_SCORE, CHECKMATE_SCORE, 1 if game_context.white_to_move else -1)
    return next_move


def find_move_min_max(game_context, valid_moves, depth, white_moving):
    """Min max (recurse) to find the best available move

    Args:
        game_context (GameContext): context of the game
        valid_moves (list): list of possible moves
        depth (int): how deep we want to go in finding the optimal move.
        white_moving (bool): bool if it's whites turn.

    Returns:
        int: score for a move.
    """
    global next_move
    if depth == 0:
        return score_material(game_context.board)

    if white_moving:
        max_score = -CHECKMATE_SCORE
        for move in valid_moves:
            game_context.make_move(move)
            next_moves = game_context.get_valid_moves()
            score = find_move_min_max(game_context, next_moves, depth-1, False)
            if score > max_score:
                max_score = score
                if depth == DEPTH:
                    next_move = move
            game_context.undo_move()
        return max_score
    else:
        min_score = CHECKMATE_SCORE
        for move in valid_moves:
            next_moves = game_context.get_valid_moves()
            score = find_move_min_max(game_context, next_moves, depth - 1, True)
            if score > min_score:
                min_score = score
                if depth == DEPTH:
                    next_move = move
            game_context.undo_move()
        return min_score


def find_move_nega_max(game_context, valid_moves, depth, turn_multiplier):
    """Find the best move using nega max algorithm

    Args:
        game_context (GameContext): context of the game
        valid_moves (list): list of possible moves
        depth (int): how deep we want to go in finding the optimal move.
        turn_multiplier (int): multiplier for the score losee function.

    Returns:
        int: score for a given move
    """
    global next_move
    if depth == 0:
        return turn_multiplier * score_board(game_context)
    
    max_score = -CHECKMATE_SCORE

    for move in valid_moves:
        game_context.make_move(move)
        next_moves = game_context.get_valid_moves()
        score = -find_move_min_max(game_context, next_moves, depth - 1, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        game_context.undo_move()

    return max_score


def find_move_nega_max_alpha_beta_pruning(game_context, valid_moves, depth, alpha, beta, turn_multiplier):
    """Find the best move using nega max alpha beta pruning algorithm

    Args:
        game_context (GameContext): context of the game
        valid_moves (list): list of possible moves
        depth (int): how deep we want to go in finding the optimal move.
        alpha (int): alpha border value
        beta (int): beta border value
        turn_multiplier (int): multiplier for the score losee function.

    Returns:
        int: score for a given move
    """
    global next_move
    if depth == 0:
        return turn_multiplier * score_board(game_context)
    
    max_score = -CHECKMATE_SCORE

    for move in valid_moves:
        game_context.make_move(move)
        next_moves = game_context.get_valid_moves()
        score = -find_move_nega_max_alpha_beta_pruning(game_context, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        game_context.undo_move()
        
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break

    return max_score


def score_board(game_context):
    """Adjust the score if the checkmate is possible to do. Returns MAX score for checkmate possibility


    Args:
        game_context (GameContext): context of the game

    Returns:
        int: score for a given move
    """
    if game_context.checkmate:
        if game_context.white_to_move:
            return -CHECKMATE_SCORE
        else:
            return CHECKMATE_SCORE
    elif game_context.stalemate:
        return STALEMATE_SCORE

    score = 0
    for row in game_context.board:
        for square in row:
            if square[0] == "w":
                score += piece_score[square[1]]
            elif square[0] == "b":
                score -= piece_score[square[1]]

    return score
