from random import choice
from os import system
import pygame
from settings import *
vector = pygame.math.Vector2


class Spritesheet:
    # load and parse spritesheet
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert()

    def get_image(self, x, y, w, h):
        image = pygame.Surface((w, h))
        # take from spritesheet and blit to (0,0) of image
        image.blit(self.spritesheet, (0, 0), (x, y, w, h))
        image = pygame.transform.scale(
            image, (round(w // 1.6), round(h // 1.6)))
        return image


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        # animation
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        # sprite
        self.load_images()
        self.image = self.standing_frame
        self.rect = self.image.get_rect()
        self.rect.center = (40, HEIGHT - 100)
        # physics
        self.pos = vector(40, HEIGHT - 100)
        self.vel = vector(0, 0)
        self.acc = vector(0, 0)

    def load_images(self):
        # standing images
        self.standing_frame = self.game.spritesheet2.get_image(
            512, 1280, 128, 256)
        self.standing_frame.set_colorkey(BLACK)
        # walking right images
        self.walking_frames_right = [
            self.game.spritesheet2.get_image(512, 512, 128, 256),
            self.game.spritesheet2.get_image(512, 256, 128, 256)
        ]
        # use right images but reversed
        self.walking_frames_left = []
        for frame in self.walking_frames_right:
            frame.set_colorkey(BLACK)
            self.walking_frames_left.append(
                pygame.transform.flip(frame, True, False))
        # jump images
        self.jumping_frame = self.game.spritesheet2.get_image(
            768, 1536, 128, 256)
        self.jumping_frame.set_colorkey(BLACK)
        # falling image right
        self.falling_frame_right = self.game.spritesheet2.get_image(
            512, 768, 128, 256)
        self.falling_frame_right.set_colorkey(BLACK)
        # falling image left
        self.falling_frame_left = pygame.transform.flip(
            self.falling_frame_right, True, False)
        self.falling_frame_left.set_colorkey(BLACK)

    def jump(self):
        # can jump if on a block
        self.rect.x += 2
        collision = pygame.sprite.spritecollide(self, self.game.blocks, False)
        self.rect.x -= 2
        # can jump
        if collision and not self.jumping and not self.walking:
            self.jumping = True
            self.vel.y = PLAYER_JUMP
        # moving before jump gives a boost
        if collision and not self.jumping and self.walking:
            self.jumping = True
            self.vel.y = PLAYER_JUMP * 1.08

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def update(self):
        self.animate()
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
        # player.vel.x = 0 if value is low enough
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        # wrap side of screen
        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2

        # block collision check position
        self.rect.midbottom = self.pos

    def animate(self):
        # get ticks since init
        now = pygame.time.get_ticks()

        # if there is no velocity, then player is idle
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False

        # walking animation
        if self.walking:
            if now - self.last_update > ANIMATION_SPEED:
                self.last_update = now
                # change animation frame, adjust image rect
                self.current_frame = (
                    self.current_frame + 1) % len(self.walking_frames_left)
                bottom = self.rect.bottom
                # moving right
                if self.vel.x > 0:
                    self.image = self.walking_frames_right[self.current_frame]
                # moving left
                else:
                    self.image = self.walking_frames_left[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # idle animation
        if not self.jumping and not self.walking:
            if now - self.last_update > ANIMATION_SPEED:
                self.last_update = now
                # current frame will be standing frame
                self.current_frame = (
                    self.current_frame + 1)
                # change animation frame, adjust image rect
                bottom = self.rect.bottom
                self.image = self.standing_frame
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # falling animation
        if self.vel.y > 0:
            # moving right
            if self.vel.x > 0:
                self.last_update = now
                self.current_frame += 1
                # change animation frame, adjust image rect
                bottom = self.rect.bottom
                self.image = self.falling_frame_right
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
            # moving left
            else:
                self.last_update = now
                self.current_frame += 1
                # change animation frame, adjust image rect
                bottom = self.rect.bottom
                self.image = self.falling_frame_left
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        # sprite
        images = [
            self.game.spritesheet1.get_image(630, 140, 70, 70),
            self.game.spritesheet1.get_image(0, 0, 70, 70)
        ]
        self.image = choice(images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
