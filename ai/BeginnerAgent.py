import random
import math


from ai.algorithm import minimax, move_generator

class BeginnerAgent(BaseAgent):
    """Randomly selects a valid move."""
    def get_move(self, game_state):
        moves = MoveGenerator.get_moves(board, self.color)
        if not moves:
            return None
        return random.choice(moves)

