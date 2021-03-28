from random import randint
import pygame
from pygame.locals import *
from settings import *
from sprites import *


class Game:
    def __init__(self):
        # pygame
        pygame.init()
        pygame.mixer.init()
        # window
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        # game
        self.clock = pygame.time.Clock()
        self.running = True

    def new(self):
        # new game
        self.all_sprites = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for b in BLOCK_LIST:
            # x,y,w,h
            block = Block(*b)
            self.all_sprites.add(block)
            self.blocks.add(block)
        self.loop()

    def loop(self):
        # game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.update()
            self.events()
            self.draw()

    def update(self):
        # update
        self.all_sprites.update()
        # collision detection if falling
        if self.player.vel.y > 0:
            collision = pygame.sprite.spritecollide(
                self.player, self.blocks, False)
            if collision:
                self.player.pos.y = collision[0].rect.top + 1
                self.player.vel.y = 0
        # if player reaches 3/4 height
        if self.player.rect.top <= HEIGHT / 4:
            # change y to velocity so the level can move
            self.player.pos.y += abs(self.player.vel.y)
            for block in self.blocks:
                # move blocks down at same velocity as player
                block.rect.y += abs(self.player.vel.y)
                # remove old blocks
                if block.rect.top >= HEIGHT:
                    block.remove()
    def events(self):
        # pygame events
        for event in pygame.event.get():
            # window close event
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            # key presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()

    def draw(self):
        # draw events
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        # flip display after draw events
        pygame.display.flip()

    def show_splash(self):
        pass

    def show_level(self):
        pass

    def game_over(self):
        pass


game = Game()
game.show_splash()
while game.running:
    game.new()
    game.show_level()

pygame.quit()
