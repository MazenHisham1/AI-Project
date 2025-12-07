from core.game_state import GameState
from core.constants import BLACK, WHITE

from ai.BaseAgent import BaseAgent
from ai.BeginnerAgent import BeginnerAgent
from ai.IntermediateAgent import IntermediateAgent
from ai.AdvancedAgent import AdvancedAgent


class AgentVsAgentMode:
    def __init__(self, black_cls=BeginnerAgent, white_cls=AdvancedAgent):
        self.state = GameState()
        self.black_agent: BaseAgent = black_cls(BLACK)
        self.white_agent: BaseAgent = white_cls(WHITE)

    def step(self):
        if self.state.game_over:
            return {
                "success": False,
                "reason": "game_over",
                "game_over": True,
                "winner": self.state.winner,
            }

        if self.state.current_player == BLACK:
            agent = self.black_agent
        else:
            agent = self.white_agent

        move = agent.get_move(self.state)

        if move is None:
            self.state.switch_turn()
            return {
                "success": False,
                "reason": "no_valid_move",
                "game_over": self.state.game_over,
                "winner": self.state.winner,
                "current_player": self.state.current_player,
            }

        success = self.state.apply_move(*move)

        if not success:
            return {
                "success": False,
                "reason": "invalid_agent_move",
                "game_over": self.state.game_over,
                "winner": self.state.winner,
            }

        return {
            "success": True,
            "reason": None,
            "game_over": self.state.game_over,
            "winner": self.state.winner,
            "current_player": self.state.current_player,
            "last_move": move,
        }

    def get_board(self):
        return self.state.board.grid

    def get_current_player(self):
        return self.state.current_player
