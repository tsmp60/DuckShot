"""Screen identifiers and the data of one play session."""
from dataclasses import dataclass, field

from config import settings

# Which screen is active
MENU = "menu"
PLAYING = "playing"
BANKRUPT = "bankrupt"


@dataclass
class GameState:
    """Everything that belongs to ONE play session. Make a new one = fresh game."""

    money: int = settings.START_MONEY
    ammo: int = settings.AMMO_MAX
    is_reloading: bool = False
    reload_timer: int = 0
    spawn_timer: int = 0
    ducks_shot: int = 0
    ducks: list = field(default_factory=list)
    pellets: list = field(default_factory=list)
    popups: list = field(default_factory=list)  # floating "+$15" texts

    @property
    def is_bankrupt(self) -> bool:
        return self.money <= 0
