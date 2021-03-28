# sprite class
import pygame
from settings import *
vector = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.Surface((32, 32))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vector(WIDTH / 2, HEIGHT / 2)
        self.vel = vector(0, 0)
        self.acc = vector(0, 0)

    def jump(self):
        # can jump if on a block
        self.rect.x += 1
        collision = pygame.sprite.spritecollide(self, self.game.blocks, False)
        self.rect.x -= 1
        if collision:
            # jump
            self.vel.y = -15

    def update(self):
        # gravity = y value
        self.acc = vector(0, PLAYER_GRAVITY)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # motion
        self.vel += self.acc
        # a=Δv/Δt (equation of motion)
        self.pos += self.vel + 0.5 * self.acc
        # wrap level
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        # collision check position
        self.rect.midbottom = self.pos


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
