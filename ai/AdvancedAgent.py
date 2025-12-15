from ai.base_agent import BaseAgent
from ai.algorithm import Minimax

class AdvancedAgent(BaseAgent):
    def __init__(self, color):
        super().__init__(color)
        self.ai = Minimax()

    def get_move(self, board):
        
        return self.ai.get_move_using_minimax(board, self.color, depth=5)
