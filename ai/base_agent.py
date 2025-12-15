import random
import math


from ai.algorithm import minimax, move_generator


class BaseAgent:
    def __init__(self, color):
        self.color = color

    def get_move(self, game_state):
        raise NotImplementedError("Subclasses must implement get_move()")


