# sprite class
import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite,__init__(self)
        self.image = pygame.Surface((32, 32))
        self.image.fill(CYAN)
