from core.board import Board
from core.constants import BLACK, WHITE
from core.game_state import GameState
import math

def evaluate_board (state, player):
    score = 0
    b, w = state.get_score()

    if player == BLACK:
        score += b - w 
    else:
        score += w - b

    return score

def get_move_using_minimax(game, player, depth = 4):
    if player == 1:
        max_move = None
        max_eval = -math.inf
        moves_evals = []
        for valid_move in game.get_valid_moves(player):
            current_game = game.make_move(valid_move[0], valid_move[1], player)
            current_eval = minimax(current_game, depth, -player, alpha = -math.inf, beta = math.inf)
            moves_evals.append((valid_move, current_eval))
            
            if current_eval > max_eval:
                max_eval = current_eval
                max_move = valid_move
        #print("Maximize")
        #print(moves_evals)
        return max_move
    else:
        min_move = None
        min_eval = math.inf
        moves_evals = []
        for valid_move in game.get_valid_moves(player):
            current_game = game.make_move(valid_move[0], valid_move[1], player)
            current_eval = minimax(current_game, depth, -player, alpha = -math.inf, beta = math.inf)
            moves_evals.append((valid_move, current_eval))
            
            if current_eval < min_eval:
                min_eval = current_eval
                min_move = valid_move
        #print("Minimize")
        #print(moves_evals)
        return min_move
    
def minimax (state, depth, player, alpha, beta):
    if depth == 0:
        return evaluate_board(state, -player)
    
    if player == 1:
        if len(state.get_valid_moves(BLACK)) == 0:
            return evaluate_board(state, player)
        maxEval = -math.inf
        for move in state.get_valid_moves(player):
            new_state = state.make_move(move[0],move[1], player)
            evaluation = minimax(new_state, depth-1, -player, alpha, beta)
            maxEval = max(maxEval, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return maxEval
    
    else:
        if len(state.get_valid_moves(WHITE)) == 0:
            return evaluate_board(state, player)
        minEval = math.inf
        for move in state.get_valid_moves(player):
            new_state = state.make_move(move[0],move[1], player)
            evaluation = minimax(new_state, depth-1, -player, alpha, beta)
            minEval = min(minEval, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return minEval