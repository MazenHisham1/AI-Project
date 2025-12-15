import customtkinter as ctk
import time
from core.constants import BLACK, WHITE, EMPTY, COLOR_MAP
from core.game_controller import GameController

# COLORS
COLOR_BG = "#0b1210"
COLOR_CARD_BG = "#14211a"
COLOR_CARD_HOVER = "#1e3328"
COLOR_ACCENT = "#2cc985"
COLOR_GOLD = "#e4c94e"
COLOR_TEXT_MAIN = "#ffffff"
COLOR_TEXT_SUB = "#8fa39a"
COLOR_BOARD_MAT = "#183020"
COLOR_CELL_1 = "#266337"
COLOR_CELL_HOVER = "#36804a"

class BoardCell(ctk.CTkFrame):
    def __init__(self, master, r, c, size, click_callback):
        super().__init__(master, width=size, height=size, fg_color=COLOR_CELL_1, corner_radius=4)
        self.pack_propagate(False)
        self.r = r
        self.c = c
        self.click_callback = click_callback 
        self.piece_frame = None
        
        self.current_state = "empty" # "empty", "black", "white", "hint"

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click) 

    def on_enter(self, event):
        # Only hover effect if cell is truly empty (no piece, no hint)
        if self.current_state == "empty": 
            self.configure(fg_color=COLOR_CELL_HOVER)
    
    def on_leave(self, event):
        self.configure(fg_color=COLOR_CELL_1)

    def on_click(self, event):
        if self.click_callback: self.click_callback(self.r, self.c)

    def update_view(self, state_type, color=None):
       
        # Create a signature for the new state
        new_state_signature = f"{state_type}_{color}"
        
        # If nothing changed, do absolutely nothing (Instant Speed)
        if self.current_state == new_state_signature:
            return

        self.current_state = new_state_signature
        
        # 1. Clean up old widgets
        if self.piece_frame:
            self.piece_frame.destroy()
            self.piece_frame = None
        
        # 2. Reset Base
        self.configure(fg_color=COLOR_CELL_1, border_width=0)

        # 3. Draw New State
        if state_type == "piece":
            size = self.winfo_reqwidth() * 0.75
            self.piece_frame = ctk.CTkFrame(self, width=size, height=size, corner_radius=size/2, fg_color=color, bg_color="transparent")
            self.piece_frame.place(relx=0.5, rely=0.5, anchor="center")
            # Bind click through the piece
            self.piece_frame.bind("<Button-1>", self.on_click)
            
        elif state_type == "hint":
            self.configure(border_width=2, border_color=COLOR_GOLD)
            self.piece_frame = ctk.CTkFrame(self, width=12, height=12, corner_radius=6, fg_color=COLOR_GOLD)
            self.piece_frame.place(relx=0.5, rely=0.5, anchor="center")
            self.piece_frame.bind("<Button-1>", self.on_click)

class GameScreen(ctk.CTkFrame):
    def __init__(self, master, on_back, agent_black, agent_white):
        super().__init__(master, fg_color="transparent")
        self.master = master
        self.on_back = on_back
        
        self.game_over_shown = False

        # Initialize Controller
        self.controller = GameController(
            agent_black, 
            agent_white, 
            callbacks={
                'on_update': self.update_gui,
                'on_status': self.update_status,
                'on_ai_result': self.handle_ai_result
            }
        )

        # --- UI Setup ---
        self.top_bar = ctk.CTkFrame(self, fg_color="transparent", height=100)
        self.top_bar.pack(fill="x", padx=50, pady=(15, 5))

        self.score_container = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        self.score_container.pack()
        self.create_score_cards()

        self.status_pill = ctk.CTkFrame(self, fg_color=COLOR_CARD_BG, corner_radius=20, height=35, width=200)
        self.status_pill.pack(pady=(10, 15))
        self.status_pill.pack_propagate(False)
        self.lbl_status = ctk.CTkLabel(self.status_pill, text="Initializing...", font=("Roboto", 15, "bold"), text_color=COLOR_GOLD)
        self.lbl_status.place(relx=0.5, rely=0.5, anchor="center")

        BOARD_SIZE = 750
        self.board_frame = ctk.CTkFrame(self, width=BOARD_SIZE, height=BOARD_SIZE, fg_color=COLOR_BOARD_MAT, corner_radius=8)
        self.board_frame.pack(pady=5)
        
        self.grid_inner = ctk.CTkFrame(self.board_frame, fg_color="transparent")
        self.grid_inner.place(relx=0.5, rely=0.5, anchor="center")

        self.cells = []
        cell_size = (BOARD_SIZE - 24) / 8
        for r in range(8):
            row_cells = []
            for c in range(8):
                cell = BoardCell(self.grid_inner, r, c, cell_size, self.controller.handle_click)
                cell.grid(row=r, column=c, padx=2, pady=2)
                row_cells.append(cell)
            self.cells.append(row_cells)

        self.bottom_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_bar.pack(side="bottom", pady=30)
        
        self.update_gui()

    # --- UI CALLBACKS ---
    def handle_ai_result(self, move):
        self.after(0, lambda: self.controller.finish_ai_move(move))

    def update_status(self, text, is_busy=False):
        self.lbl_status.configure(text=text, text_color=COLOR_ACCENT if is_busy else COLOR_GOLD)

    def update_gui(self):
        # 1. Update Buttons
        self.setup_bottom_buttons()

        # 2. Get Data
        game_state = self.controller.game_state
        board = self.controller.get_board()
        current_plr = game_state.current_player
        is_replay = self.controller.is_replay_mode
        
        # 3. Update Grid (OPTIMIZED)
        valid_moves = []
        if not is_replay and not game_state.game_over:
            valid_moves = board.get_valid_moves(current_plr)
        
        is_human_turn = (current_plr == BLACK and not self.controller.agent_black) or \
                        (current_plr == WHITE and not self.controller.agent_white)
        show_hints = is_human_turn and not is_replay and not self.controller.is_ai_thinking

        for r in range(8):
            for c in range(8):
                cell = self.cells[r][c]
                val = board.grid[r][c]
                
                # Use update_view instead of clear/set_piece
                if val != EMPTY:
                    cell.update_view("piece", COLOR_MAP[val])
                elif show_hints and (r, c) in valid_moves:
                    cell.update_view("hint")
                else:
                    cell.update_view("empty")

        # 4. Update Scores
        b, w = board.get_score()
        self.lbl_score_black.configure(text=str(b))
        self.lbl_score_white.configure(text=str(w))

        # 5. Status
        if is_replay:
            self.lbl_status.configure(text="Replay Mode", text_color="white")
        elif game_state.game_over:
            self.lbl_status.configure(text="Game Over", text_color=COLOR_GOLD)
            self.show_game_over_overlay()
        elif not self.controller.is_ai_thinking:
            txt = "Black's Turn" if current_plr == BLACK else "White's Turn"
            self.lbl_status.configure(text=txt, text_color=COLOR_GOLD)

        # 6. Active Card
        if not is_replay:
            self.card_black.configure(border_width=2 if current_plr == BLACK else 0, border_color=COLOR_GOLD)
            self.card_white.configure(border_width=2 if current_plr == WHITE else 0, border_color=COLOR_GOLD)

    def setup_bottom_buttons(self):
        for widget in self.bottom_bar.winfo_children(): widget.destroy()

        if self.controller.is_replay_mode:
            ctk.CTkButton(self.bottom_bar, text="Exit Replay", command=self.controller.exit_replay, fg_color="#ff5555", width=100, height=40, corner_radius=8).pack(side="left", padx=10)
            ctk.CTkButton(self.bottom_bar, text="< Prev", command=self.controller.prev_replay, fg_color=COLOR_CARD_BG, width=80, height=40, corner_radius=8).pack(side="left", padx=10)
            
            txt = self.controller.get_replay_text()
            self.lbl_replay_step = ctk.CTkLabel(self.bottom_bar, text=f"Move {txt}", font=("Roboto", 16, "bold"), text_color="white")
            self.lbl_replay_step.pack(side="left", padx=15)
            
            ctk.CTkButton(self.bottom_bar, text="Next >", command=self.controller.next_replay, fg_color=COLOR_CARD_BG, width=80, height=40, corner_radius=8).pack(side="left", padx=10)
        else:
            self.btn_menu = ctk.CTkButton(self.bottom_bar, text="Menu", font=("Roboto", 14), fg_color=COLOR_CARD_BG, text_color="white", hover_color=COLOR_CARD_HOVER, width=120, height=40, corner_radius=8, command=self.on_back)
            self.btn_menu.pack(side="left", padx=15)
            
            self.btn_undo = ctk.CTkButton(self.bottom_bar, text="Undo", font=("Roboto", 14), fg_color="#d68c29", text_color="white", hover_color="#b57521", width=120, height=40, corner_radius=8, command=self.controller.undo)
            self.btn_undo.pack(side="left", padx=15)

            self.btn_restart = ctk.CTkButton(self.bottom_bar, text="Restart", font=("Roboto", 14, "bold"), fg_color=COLOR_ACCENT, text_color="black", hover_color="#24a36b", width=120, height=40, corner_radius=8, command=self.restart_game_ui)
            self.btn_restart.pack(side="left", padx=15)

    def restart_game_ui(self):
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and widget not in [self.top_bar, self.board_frame, self.bottom_bar, self.status_pill]:
                widget.destroy()
        self.game_over_shown = False
        self.controller.restart()

    def enter_replay_ui(self):
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and widget not in [self.top_bar, self.board_frame, self.bottom_bar, self.status_pill]:
                widget.destroy()
        self.game_over_shown = False 
        self.controller.start_replay()

    def show_game_over_overlay(self):
        if self.game_over_shown: return
        self.game_over_shown = True

        winner = self.controller.game_state.winner
        is_pva = (self.controller.agent_black or self.controller.agent_white)
        
        msg = ""
        color = COLOR_ACCENT
        
        if winner == 0:
            msg = "It's a Draw!"
            color = COLOR_GOLD
        elif is_pva:
            human_color = BLACK if not self.controller.agent_black else WHITE
            if self.controller.agent_black and self.controller.agent_white:
                 name = "Black" if winner == BLACK else "White"
                 msg = f"{name} Wins!"
            elif winner == human_color:
                msg = "🎉 Victory! You Won! 🎉"
            else:
                msg = "Game Over. Try Again!"
                color = "#ff5555" 
        else:
            name = "Black" if winner == BLACK else "White"
            msg = f"{name} Wins!"

        overlay = ctk.CTkFrame(self, fg_color=COLOR_BG, corner_radius=20, border_width=2, border_color=COLOR_GOLD)
        overlay.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.6, relheight=0.35)
        
        ctk.CTkLabel(overlay, text=msg, font=("Roboto", 32, "bold"), text_color=color).pack(expand=True, pady=(15, 5))
        
        btn_box = ctk.CTkFrame(overlay, fg_color="transparent")
        btn_box.pack(pady=20)
        
        ctk.CTkButton(btn_box, text="Menu", command=self.on_back, fg_color=COLOR_CARD_BG, width=120, height=45).pack(side="left", padx=10)
        ctk.CTkButton(btn_box, text="Watch Replay", command=self.enter_replay_ui, fg_color=COLOR_CARD_BG, width=120, height=45, border_width=1, border_color=COLOR_ACCENT).pack(side="left", padx=10)
        ctk.CTkButton(btn_box, text="Play Again", command=self.restart_game_ui, fg_color=COLOR_ACCENT, text_color="black", hover_color="#24a36b", width=120, height=45).pack(side="left", padx=10)
        
        overlay.lift()

    def create_score_cards(self):
        self.card_black = self._make_card(self.score_container, "Black", BLACK, 0)
        self.card_white = self._make_card(self.score_container, "White", WHITE, 1)

    def _make_card(self, parent, name, color, col_idx):
        card = ctk.CTkFrame(parent, width=240, height=80, fg_color=COLOR_CARD_BG, corner_radius=12)
        card.grid(row=0, column=col_idx, padx=10)
        card.grid_propagate(False)
        ctk.CTkLabel(card, text="●", font=("Arial", 48), text_color=COLOR_MAP[color]).place(relx=0.1, rely=0.5, anchor="w")
        ctk.CTkLabel(card, text=name, font=("Roboto", 13), text_color=COLOR_TEXT_SUB).place(relx=0.4, rely=0.3)
        lbl_score = ctk.CTkLabel(card, text="2", font=("Roboto", 26, "bold"), text_color="white")
        lbl_score.place(relx=0.4, rely=0.65)
        setattr(self, f"lbl_score_{name.lower()}", lbl_score)
        return card

class GameModeButton(ctk.CTkFrame):
    def __init__(self, master, title, description, icon, command=None):
        super().__init__(master, fg_color=COLOR_CARD_BG, corner_radius=15, height=90, width=500)
        self.command = command
        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=0, minsize=90)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(self, text=icon, font=("Segoe UI Emoji", 32), text_color=COLOR_ACCENT).grid(row=0, column=0, rowspan=2)
        ctk.CTkLabel(self, text=title, font=("Roboto Medium", 18), text_color=COLOR_TEXT_MAIN, anchor="w").grid(row=0, column=1, sticky="sw", padx=(0, 20), pady=(12, 0))
        ctk.CTkLabel(self, text=description, font=("Roboto", 13), text_color=COLOR_TEXT_SUB, anchor="w").grid(row=1, column=1, sticky="nw", padx=(0, 20), pady=(0, 12))
        
        self.bind("<Button-1>", self.on_click)
        for child in self.winfo_children(): child.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", lambda e: self.configure(fg_color=COLOR_CARD_HOVER))
        self.bind("<Leave>", lambda e: self.configure(fg_color=COLOR_CARD_BG))

    def on_click(self, e):
        if self.command: self.command()

class MenuScreen(ctk.CTkFrame):
    def __init__(self, master, start_pvp, start_pva, start_ava):
        super().__init__(master, fg_color="transparent")
        self.start_pvp = start_pvp
        self.start_pva = start_pva
        self.start_ava = start_ava
        
        try:
            self.after(100, lambda: self.master.state("zoomed"))
        except:
            pass 

        self.center_box = ctk.CTkFrame(self, fg_color="transparent")
        self.center_box.place(relx=0.5, rely=0.5, anchor="center")
        
        self.show_main_menu()

    def show_main_menu(self):
        for widget in self.center_box.winfo_children(): widget.destroy()

        ctk.CTkLabel(self.center_box, text="Othello AI", font=("Roboto", 56, "bold"), text_color="white").pack(pady=(0, 5))
        ctk.CTkLabel(self.center_box, text="Choose Your Game Mode", font=("Roboto", 16), text_color=COLOR_TEXT_SUB).pack(pady=(0, 45))

        GameModeButton(self.center_box, "Player vs Player", "Local Multiplayer", "👥", command=self.start_pvp).pack(pady=8)
        GameModeButton(self.center_box, "Player vs Computer", "Challenge the AI", "🤖", command=self.show_difficulty_selection).pack(pady=8)
        GameModeButton(self.center_box, "Computer vs Computer", "Watch AI Battle", "💻", command=self.start_ava).pack(pady=8)

    def show_difficulty_selection(self):
        for widget in self.center_box.winfo_children(): widget.destroy()

        ctk.CTkLabel(self.center_box, text="Select Difficulty", font=("Roboto", 48, "bold"), text_color="white").pack(pady=(0, 40))

        GameModeButton(self.center_box, "Beginner", "Easy Agent", "🐣", command=lambda: self._safe_start_pva('beginner')).pack(pady=8)
        GameModeButton(self.center_box, "Intermediate", "Medium Agent", "⚖️", command=lambda: self._safe_start_pva('intermediate')).pack(pady=8)
        GameModeButton(self.center_box, "Advanced", "Hard Agent", "🔥", command=lambda: self._safe_start_pva('advanced')).pack(pady=8)
        
        ctk.CTkButton(self.center_box, text="Back", fg_color=COLOR_CARD_BG, width=200, height=50, command=self.show_main_menu).pack(pady=20)

    def _safe_start_pva(self, level):
        try:
            self.start_pva(level)
        except TypeError:
            print(f"[WARNING] Crash prevented: 'main.py' outdated. Defaulting.")
            self.start_pva()
