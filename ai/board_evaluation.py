from core.constants import BLACK

class BoardEvaluation:
    def evaluate_board (self,state, player):
        score = 0
        b, w = state.get_score()

        if player == BLACK:
            score += b - w 
        else:
            score += w - b

        return score