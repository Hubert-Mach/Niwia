# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# some screen settings
WIDTH_FACTOR = 0.6
WIDTH = 1024
HEIGHT = 768

# GUI elements setting
MARGIN = 10
BUTTON_HEIGHT = 60
TEXT_WIDGET_FACTOR = 0.6 # What portion of screen height should text box take

# Where to write code and read commands
CODEDIR="save" # directory where created script is saved
CODEFILE="scipt.py" # file where code from textwidget is written
COMDIR="run" # directory where runtime file are created
COMFILE="commands" # file where commands are written to be read by game

# game settings
FPS = 60
TITLE = "Niwia - code your game!"
BGCOLOR = DARKGREY

TILESIZE = 64
GRIDWIDTH = 500 / TILESIZE
GRIDHEIGHT = 500 / TILESIZE
