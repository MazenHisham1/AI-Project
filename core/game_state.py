from .board import Board
from .constants import BLACK, WHITE

class GameState:
    def __init__(self):
        self.board = Board()
        self.current_player = BLACK
        self.game_over = False
        self.winner = None
        self.log = []

    def apply_move(self, r, c):
        if self.game_over:
            return False

        new_board = self.board.make_move(r, c, self.current_player)
        if new_board: # if the move is valid
            self.board = new_board
            self.log.append((self.current_player, r, c))
            self.switch_turn()
            return True
        return False

    def switch_turn(self):
        self.current_player = -self.current_player
        if not self.board.get_valid_moves(self.current_player):
            print(f"Player {self.current_player} has no moves.")
            self.current_player = -self.current_player
            if not self.board.get_valid_moves(self.current_player):
                self.game_over = True
                self.determine_winner()

    def determine_winner(self):
        b, w = self.board.get_score()
        if b > w: self.winner = BLACK
        elif w > b: self.winner = WHITE
        else: self.winner = 0 # Draw
