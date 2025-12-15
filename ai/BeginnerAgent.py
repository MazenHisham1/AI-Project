import random
from ai.base_agent import BaseAgent
from ai.move_generator import MoveGenerator

class BeginnerAgent(BaseAgent):
    def get_move(self, board):
        moves = MoveGenerator.get_moves(board, self.color)
        if moves:
            return random.choice(moves)
        return None
