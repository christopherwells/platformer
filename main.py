from random import randrange, randint
from os import path
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
        self.game_font = pygame.font.match_font(GAME_FONT)
        self.load_data()
        # load music - music from https://sycamoredrive.bandcamp.com/album/the-waves-the-sea
        # available under cc license https://creativecommons.org/licenses/by-nc-sa/3.0/us/
        pygame.mixer.music.load(
            path.join(self.snd_dir, 'Sycamore Drive - Happiness.ogg'))
        # play music on loop
        pygame.mixer.music.play(loops=-1)

    def load_data(self):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        # high score
        with open(path.join(self.dir, SCORE_FILE), 'r') as f:
            # get high score
            try:
                self.high_score = int(f.read())
            # file empty
            except:
                self.high_score = 0
        # load spritesheets
        self.spritesheet1 = Spritesheet(path.join(img_dir, SPRITESHEET1))
        self.spritesheet2 = Spritesheet(path.join(img_dir, SPRITESHEET2))
        # load sounds
        self.snd_dir = path.join(self.dir, 'snd')

    def new(self):
        # new game
        self.score = 0
        self.all_sprites = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for b in BLOCK_LIST:
            # x,y
            block = Block(self, *b)
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
            system('clear')
            print(self.clock)
            print(self.player.vel)

    def update(self):
        # update
        self.all_sprites.update()

        # collision detection if falling
        if self.player.vel.y > 0:
            collision = pygame.sprite.spritecollide(
                self.player, self.blocks, False)
            if collision:
                # snap to block if player.bottom high enough
                # snap to lowest block first
                lowest = collision[0]
                for c in collision:
                    if c.rect.bottom > lowest.rect.bottom:
                        lowest = collision
                if self.player.pos.y < lowest.rect.centery:
                    self.player.pos.y = lowest.rect.top + 1
                    self.player.vel.y = 0
                    self.player.jumping = False

        # if player reaches 3/4 height
        if self.player.rect.top <= HEIGHT / 4:
            # change y to velocity so the level can move
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for block in self.blocks:
                # move blocks down at same velocity as player
                block.rect.y += max(abs(self.player.vel.y), 2)
                # remove old blocks
                if block.rect.top >= HEIGHT:
                    block.kill()
                    # 10 points per platform gone
                    self.score += 10

        # player hits bottom of screen
        if self.player.rect.bottom > HEIGHT:
            # move sprites up
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                # remove blocks when they hit top of screen
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.blocks) == 0:
            self.playing = False

        # generate new blocks
        while len(self.blocks) < 6:
            w = randrange(64, 128)
            b = Block(self, randrange(0, WIDTH - w), randrange(-64, -32))
            self.blocks.add(b)
            self.all_sprites.add(b)

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
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.player.jump_cut()

    def draw(self):
        # draw events
        self.screen.fill(SKY)
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, 15)

        # flip display after draw events
        pygame.display.flip()

    def show_splash(self):
        self.screen.fill(SKY)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Arrows to move, space to jump.",
                       22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press any key to start.",
                       22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("High Score: " + str(self.high_score),
                       22, WHITE, WIDTH / 2, 15)

        # update display and wait for input
        pygame.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                # wait for quit
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                # or key press
                if event.type == pygame.KEYUP:
                    waiting = False

    def show_go_screen(self):
        # game over
        if not self.running:
            return
        self.screen.fill(SKY)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score),
                       22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press any key to play again.",
                       22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        # new high score
        if self.score > self.high_score:
            self.high_score = self.score
            self.draw_text("New high score!", 22, WHITE,
                           WIDTH / 2, HEIGHT / 2 + 40)
            with open(path.join(self.dir, SCORE_FILE), 'w') as f:
                f.write(str(self.score))
        # show high_score
        else:
            self.draw_text("High score: " + str(self.high_score),
                           22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)

        # update display and wait for input
        pygame.display.flip()
        self.wait_for_key()

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.game_font, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


game = Game()
game.show_splash()
while game.running:
    game.new()
    game.show_go_screen()

pygame.quit()
