from os import path
# CONSTANTS
# game
TITLE = "Hello world!"
FPS = 60

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

# sprite specific
TILE_SIZE = 32

# player
PLAYER_ACC = 0.75
PLAYER_FRICTION = -0.11
PLAYER_GRAVITY = 0.6

# splash screen
BLOCK_LIST = [(0, HEIGHT - 40, WIDTH, 40),
              (WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20),
              (125, HEIGHT - 350, 100, 20),
              (350, 200, 100, 20),
              (175, 100, 50, 20)]

# assets
GAME_FONT = 'Arial'
SCORE_FILE = "highscores.txt"
game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, "img")
