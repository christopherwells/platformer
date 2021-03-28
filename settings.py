from os import path
# CONSTANTS

# window
WIDTH, HEIGHT = 480, 600

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
PINK = (255, 0, 255)
YELLOW = (255, 255, 0)
SKY = (0, 155, 155)

# game
TITLE = "Hello world!"
FPS = 60
MOB_FREQ = 5000

# layers
BLOCK_LAYER = 1
PLAYER_LAYER = 2
MOB_LAYER = 2

# player
PLAYER_ACC = 0.8
PLAYER_FRICTION = -0.10
PLAYER_GRAVITY = 0.8
PLAYER_JUMP = -19

# starting blocks
BLOCK_LIST = [(0, HEIGHT - 60),
              (WIDTH / 2 - 50, HEIGHT * 3 / 4),
              (125, HEIGHT - 350),
              (350, 200),
              (175, 100)]

# assets
GAME_FONT = 'Arial'
SCORE_FILE = 'highscores.txt'
game_folder = path.dirname(__file__)
SPRITESHEET1 = 'tiles_sheet.png'
SPRITESHEET2 = 'spritesheet_players.png'
SPRITESHEET3 = 'spritesheet_jumper.png'
ANIMATION_SPEED = 200
