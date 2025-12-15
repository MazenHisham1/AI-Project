from ai.beginner_agent import BeginnerAgent
from ai.advanced_agent import AdvancedAgent
from core.constants import BLACK, WHITE

class AvAMode:
    @staticmethod
    def get_agents():  
        return BeginnerAgent(BLACK), AdvancedAgent(WHITE)

