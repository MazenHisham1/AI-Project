import copy
from .constants import BLACK, WHITE, EMPTY

class Board:
    def _init_(self):
        self.size = 8
        self.grid = [[EMPTY for _ in range(8)] for _ in range(8)]
        self._setup_board()

    def _setup_board(self):
        self.grid[3][3] = WHITE
        self.grid[3][4] = BLACK
        self.grid[4][3] = BLACK
        self.grid[4][4] = WHITE

    def is_on_board(self, r, c):
        return 0 <= r < 8 and 0 <= c < 8

    def get_valid_moves(self, player):
        moves = []
        
        for r in range(8):
            for c in range(8):
                if self.is_valid_move(r, c, player):
                    moves.append((r, c))
        return moves

    def is_valid_move(self, r, c, player):
        if self.grid[r][c] != EMPTY:
            return False

        opponent = -player
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

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
        """Returns a new Board instance with the move applied."""
        if not self.is_valid_move(r, c, player):
            return None

        new_board = copy.deepcopy(self)
        new_board.grid[r][c] = player
        opponent = -player
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for dr, dc in directions:
            rr, cc = r + dr, c + dc
            flips = []

            while new_board.is_on_board(rr, cc) and new_board.grid[rr][cc] == opponent:
                flips.append((rr, cc))
                rr += dr
                cc += dc

            if new_board.is_on_board(rr, cc) and new_board.grid[rr][cc] == player:
                for fr, fc in flips:
                    new_board.grid[fr][fc] = player
        
        return new_board

    def get_score(self):
        b = sum(row.count(BLACK) for row in self.grid)
        w = sum(row.count(WHITE) for row in self.grid)
        return b, w
