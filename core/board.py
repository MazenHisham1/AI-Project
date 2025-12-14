import copy
from .constants import BLACK, WHITE, EMPTY,BOARD_SIZE,DIRECTIONS

class Board:
    def _init_(self):
        self.size = BOARD_SIZE
        self.grid = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self._setup_board()

    #INITIAL STATE
    def _setup_board(self):
        self.grid[3][3] = WHITE
        self.grid[3][4] = BLACK
        self.grid[4][3] = BLACK
        self.grid[4][4] = WHITE

    #Ensure the move on the board
    def is_on_board(self, r, c):
        return 0 <= r < self.size and 0 <= c < self.size

    def get_valid_moves(self, player):
        moves = []
        for r in range(self.size):
            for c in range(self.size):
                if self.is_valid_move(r, c, player):
                    moves.append((r, c))
        
        return moves #List of valid moves for the player

    def is_valid_move(self, r, c, player):
        # base condition
        if self.grid[r][c] != EMPTY:
            return False

        directions = DIRECTIONS
        opponent = -player

        for dr, dc in directions:
            rr, cc = r + dr, c + dc
            found_opponent = False

            while self.is_on_board(rr, cc) and self.grid[rr][cc] == opponent:
                rr += dr
                cc += dc
                found_opponent = True

            if found_opponent and self.is_on_board(rr, cc) and self.grid[rr][cc] == player:
                return True
        
        return False

   
    def make_move(self, r, c, player):
        """Returns a new Board instance. Used by GameState to keep history."""
        if not self.is_valid_move(r, c, player):
            return None
        new_board = copy.deepcopy(self)
        new_board.apply_move(r, c, player) 
        return new_board

    # --- FAST (For AI) ---
    def apply_move(self, r, c, player):
        """
        Modifies the board IN-PLACE. 
        Returns a list of flipped pieces so we can Undo later.
        """
        self.grid[r][c] = player
        opponent = -player
        directions = DIRECTIONS
        flipped_pieces = []

        for dr, dc in directions:
            rr, cc = r + dr, c + dc
            potential_flips = []

            while self.is_on_board(rr, cc) and self.grid[rr][cc] == opponent:
                potential_flips.append((rr, cc))
                rr += dr
                cc += dc

            if potential_flips and self.is_on_board(rr, cc) and self.grid[rr][cc] == player:
                for fr, fc in potential_flips:
                    self.grid[fr][fc] = player
                    flipped_pieces.append((fr, fc))
        
        return flipped_pieces

    def undo_move(self, r, c, flipped_pieces, player):
        """Reverts a move using the list of flipped pieces."""
        self.grid[r][c] = EMPTY
        opponent = -player
        for r_flip, c_flip in flipped_pieces:
            self.grid[r_flip][c_flip] = opponent

    def get_score(self):
        b = sum(row.count(BLACK) for row in self.grid)
        w = sum(row.count(WHITE) for row in self.grid)
        return b, w
    
    def get_hash(self):
        """Returns a hashable representation of the board for caching."""
        return tuple(tuple(row) for row in self.grid)
