
from ai.beginner_agent import BeginnerAgent
from ai.intermediate_agent import IntermediateAgent
from ai.advanced_agent import AdvancedAgent
from core.constants import WHITE

class pvp:
    def get_agents(difficulty='advanced'):
        # Player (None) vs Agent (White)
        if difficulty == 'beginner':
            return None, BeginnerAgent(WHITE)
        elif difficulty == 'intermediate':
            return None, IntermediateAgent(WHITE)
        else:
            # Default to advanced
            return None, AdvancedAgent(WHITE)

