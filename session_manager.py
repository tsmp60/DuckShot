"""Owns the current screen and the current play session.

Screens never talk to each other directly - they ask the manager to switch.
"""
from assets_loader import Fonts, load_assets
from bankruptcy import BankruptcyScreen
from game_state import BANKRUPT, MENU, PLAYING, GameState
from gameplay import GameplayScreen
from menu import MenuScreen


class SessionManager:
    def __init__(self, surface):
        self.surface = surface
        self.assets = load_assets()
        self.fonts = Fonts()
        self.game = GameState()
        self.snapshot = None  # last game frame, shown behind the bankruptcy screen
        self.running = True

        self.screens = {
            MENU: MenuScreen(self),
            PLAYING: GameplayScreen(self),
            BANKRUPT: BankruptcyScreen(self),
        }
        self.state = None
        self._switch(MENU)

    # --- transitions ------------------------------------------------------
    def _switch(self, new_state):
        if self.state is not None:
            self.screens[self.state].on_exit()
        self.state = new_state
        self.screens[new_state].on_enter()

    def start_new_session(self):
        """Play / Replay: always a completely fresh game."""
        self.game = GameState()
        self._switch(PLAYING)

    def go_to_menu(self):
        self._switch(MENU)

    def end_session(self):
        """Called when money <= 0."""
        self.screens[PLAYING].draw(self.surface, crosshair=False)  # up-to-date final frame
        self.snapshot = self.surface.copy()
        self._switch(BANKRUPT)

    def quit(self):
        self.running = False

    # --- frame hooks (called from main.py) --------------------------------
    def handle_event(self, event):
        self.screens[self.state].handle_event(event)

    def update(self):
        self.screens[self.state].update()

    def draw(self):
        self.screens[self.state].draw(self.surface)
