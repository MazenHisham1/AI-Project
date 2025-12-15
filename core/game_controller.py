import threading
import copy
from core.game_state import GameState
from core.constants import BLACK, WHITE

class GameController:
    def __init__(self, agent_black, agent_white, callbacks):
        self.agent_black = agent_black
        self.agent_white = agent_white
        self.callbacks = callbacks
        
        self.game_state = GameState()
        self.is_ai_thinking = False
        
        # Initial check
        self.check_ai_turn()

    def restart(self):
        self.game_state = GameState()
        self.is_ai_thinking = False
        self.callbacks['on_update']()
        self.check_ai_turn()

    def handle_click(self, r, c):
        if self.is_ai_thinking or self.game_state.game_over:
            return

        curr = self.game_state.current_player
        # Verify it is a human turn
        if (curr == BLACK and self.agent_black) or (curr == WHITE and self.agent_white):
            return

        if self.game_state.apply_move(r, c):
            self.callbacks['on_update']()
            self.check_ai_turn()

    def check_ai_turn(self):
        if self.game_state.game_over:
            return

        curr = self.game_state.current_player
        agent = self.agent_black if curr == BLACK else self.agent_white

        if agent:
            self.is_ai_thinking = True
            name = 'Black' if curr == BLACK else 'White'
            self.callbacks['on_status'](f"AI ({name}) Thinking...", True)
            
            # Run AI in a separate thread to prevent UI freezing
            board_copy = copy.deepcopy(self.game_state.board)
            threading.Thread(target=self._ai_worker, args=(agent, board_copy), daemon=True).start()

    def _ai_worker(self, agent, board):
        """Runs in background thread."""
        try:
            move = agent.get_move(board)
        except Exception as e:
            print(f"AI Error: {e}")
            move = None
        
        # Trigger UI callback (UI must handle thread-safety via .after)
        self.callbacks['on_ai_result'](move)

    def finish_ai_move(self, move):
        """Called by UI on Main Thread after AI finishes."""
        if move:
            self.game_state.apply_move(move[0], move[1])
        
        self.is_ai_thinking = False
        self.callbacks['on_update']()
        
        # Schedule next check
        if not self.game_state.game_over:
            self.check_ai_turn()

    # GETTERS FOR UI
    def get_board(self):
        return self.game_state.board
