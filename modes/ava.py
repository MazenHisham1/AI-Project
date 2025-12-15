from ai.BeginnerAgent import BeginnerAgent
from ai.AdvancedAgent import AdvancedAgent
from core.constants import BLACK, WHITE

class AvAMode:
    @staticmethod
    def get_agents():  
        return BeginnerAgent(BLACK), AdvancedAgent(WHITE)

