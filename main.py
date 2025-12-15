import customtkinter as ctk
import sys
import os

# Ensure we can find the submodules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.gui import MenuScreen, GameScreen, COLOR_BG
from modes.pvp import PvPMode
from modes.pva import PvAMode
from modes.ava import AvAMode

class OthelloApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Othello")
        self.geometry("1200x1050")
        self.minsize(900, 700)
        self.configure(fg_color=COLOR_BG) 
        
        
        try:
             from ctypes import windll
             windll.shcore.SetProcessDpiAwareness(1)
        except:
             pass

        self.current_frame = None
        self.show_menu()

    def show_menu(self):
        if self.current_frame: self.current_frame.destroy()
        self.current_frame = MenuScreen(
            self, 
            start_pvp=lambda: self.start_game(PvPMode),
            start_pva=lambda: self.start_game(PvAMode),
            start_ava=lambda: self.start_game(AvAMode)
        )
        self.current_frame.pack(fill="both", expand=True)

    def start_game(self, mode_class):
        if self.current_frame: self.current_frame.destroy()
        
        # Get agents from the mode class factory
        agent_black, agent_white = mode_class.get_agents()
        
        self.current_frame = GameScreen(
            self, 
            on_back=self.show_menu,
            agent_black=agent_black,
            agent_white=agent_white
        )
        self.current_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = OthelloApp()
    app.mainloop()