from pyray import *
from enum import Enum, auto
from os.path import join

SCREEN_WIDTH, SCREEN_HEIGHT = 960, 540
RENDER_WIDTH, RENDER_HEIGHT = 192, 108

class GameScreen(Enum):
    LOGO = auto()
    TITLE = auto()
    GAMEPLAY = auto()
    END = auto()
    CREDITS = auto()