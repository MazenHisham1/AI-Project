import threading
import copy
from core.game_state import GameState
from core.constants import BLACK, WHITE

class GameController:
    def _init_(self, agent_black, agent_white, callbacks):
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

    # --- VIEW HELPERS (Exposing data and logic for GUI) ---
    def get_board(self):
        return self.game_state.board

    def get_scores(self):
        return self.game_state.board.get_score()

    def get_current_player(self):
        return self.game_state.current_player

    def is_game_over(self):
        return self.game_state.game_over

    def get_valid_moves(self):
        """Returns valid moves for the current player if game is active."""
        if self.game_state.game_over:
            return []
        return self.game_state.board.get_valid_moves(self.game_state.current_player)

    def should_show_hints(self):
        """Determines if hints should be visible (Human turn only)."""
        if self.game_state.game_over or self.is_ai_thinking:
            return False
        
        curr = self.game_state.current_player
        is_human_turn = (curr == BLACK and not self.agent_black) or \
                        (curr == WHITE and not self.agent_white)
        return is_human_turn

    def get_game_over_details(self):
        """
        Returns (message, result_type)
        result_type: 'draw', 'win', 'loss', 'neutral_win'
        """
        winner = self.game_state.winner
        is_pva = (self.agent_black or self.agent_white)
        
        if winner == 0:
            return "It's a Draw!", 'draw'
        
        # Player vs Agent Logic
        if is_pva and not (self.agent_black and self.agent_white):
            human_color = BLACK if not self.agent_black else WHITE
            if winner == human_color:
                return "🎉 Victory! You Won! 🎉", 'win'
            else:
                return "Game Over. Try Again!", 'loss'
        
        # PvP or AvA Logic
        name = "Black" if winner == BLACK else "White"
        return f"{name} Wins!", 'neutral_win'
