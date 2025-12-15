from ai.BeginnerAgent import BeginnerAgent
from ai.IntermediateAgent import IntermediateAgent
from ai.AdvancedAgent import AdvancedAgent
from core.constants import WHITE

class PvAMode:
    @staticmethod
    def get_agents(difficulty='advanced'):
        # Player (None) vs Agent (White)
        if difficulty == 'beginner':
            return None, BeginnerAgent(WHITE)
        elif difficulty == 'intermediate':
            return None, IntermediateAgent(WHITE)
        else:
            # Default to advanced
            return None, AdvancedAgent(WHITE)

