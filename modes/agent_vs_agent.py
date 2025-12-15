from ai.beginner_agent import BeginnerAgent
from ai.advanced_agent import AdvancedAgent
from core.constants import BLACK, WHITE

class ava:
    def get_agents():  
        return BeginnerAgent(BLACK), AdvancedAgent(WHITE)

