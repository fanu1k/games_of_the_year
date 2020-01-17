import os
import pygame
import sys
import time
import math
import random
import shelve
from pygame.locals import *
from time import sleep
from pygame import mixer
pygame.init()
mixer.init()

FPS = 60

scr_size = (width, height) = (800, 600)


clock = pygame.time.Clock()


window = pygame.display.set_mode(scr_size)
bg = pygame.image.load('data/game_bg.png')


font = pygame.font.Font('game_font.ttf', 45)

wall_hit_sound = mixer.Sound('sounds/wall.wav')
racket_hit_sound = mixer.Sound('sounds/racket.wav')
lose_sound = mixer.Sound('sounds/lose.wav')


def music(number):
    global wall_hit_sound
    global racket_hit_sound
    if number == 1:
        wall_hit_sound.play(0)
    elif number == 2:
        lose_sound.play(0)
    else:
        racket_hit_sound.play(0)


def displaytext(text, fontsize, x, y):
    global font
    text = font.render(text, 1, pygame.Color('yellow'))
    textpos = text.get_rect(centerx=x, centery=y)
    window.blit(text, textpos)


def countdown_animation():
    global font
    beep = pygame.mixer.Sound('sounds/beep1.wav')
    count = 3
    while count > 0:
        window.fill(pygame.Color('black'))
        font_size = font.size(str(count))
        textpos = [width/2 - font_size[0]/2, height/2 - font_size[1]/2]
        window.blit(font.render(str(count), True, pygame.Color(
            'orange'), pygame.Color('black')), textpos)
        pygame.display.flip()
        beep.play()
        count -= 1
        pygame.time.delay(1000)


class Racket(pygame.sprite.Sprite):
    def __init__(self, x, y, sizex, sizey):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.sizex = sizex
        self.sizey = sizey
        self.color = pygame.Color('purple')
        self.image = pygame.Surface((sizex, sizey), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        pygame.draw.rect(self.image, self.color, (0, 0, sizex, sizey))
        self.rect = self.image.get_rect()
        self.rect.left = self.x
        self.rect.top = self.y
        self.points = 0
        self.movement = [0, 0]

    def checkbounds(self):
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > height:
            self.rect.bottom = height
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width

    def update(self):
        self.rect = self.rect.move(self.movement)
        self.checkbounds()

    def draw(self):
        window.blit(self.image, self.rect)


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, size, movement=[0, 0]):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.size = size
        self.color = pygame.Color('white')
        self.movement = movement
        self.image = pygame.Surface((size, size), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, self.color, (int(self.rect.width/2),
                                                    int(self.rect.height/2)), int(size/2))
        self.rect.centerx = x
        self.rect.centery = y
        self.maxspeed = 10
        self.score = 0
        self.movement = movement

    def checkbounds(self):
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > height:
            self.rect.bottom = height
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width

    def update(self):
        if self.rect.top == 0 or self.rect.bottom == height:
            self.movement[1] = -1*self.movement[1]
            music(1)
        if self.rect.left == 0:
            self.rect.centerx = width/2
            self.rect.centery = height/2
            self.movement = [random.randrange(-1, 2, 2) * 4, random.randrange(-1, 2, 2) * 4]
            self.score = 1
            music(2)

        if self.rect.right == width:
            self.rect.centerx = width/2
            self.rect.centery = height/2
            self.movement = [random.randrange(-1, 2, 2)*4, random.randrange(-1, 2, 2)*4]
            self.score = -1
            music(2)

        self.rect = self.rect.move(self.movement)
        self.checkbounds()

    def draw(self):
        pygame.draw.circle(self.image, self.color, (int(self.rect.width/2),
                                                    int(self.rect.height/2)), int(self.size/2))
        window.blit(self.image, self.rect)


class Bot(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def second_playerRacketmove(second_playerRacket, ball):
        if ball.movement[0] > 0:
            if ball.rect.bottom > second_playerRacket.rect.bottom + second_playerRacket.rect.height/5:
                second_playerRacket.movement[1] = 8
            elif ball.rect.top < second_playerRacket.rect.top - second_playerRacket.rect.height/5:
                second_playerRacket.movement[1] = -8
            else:
                second_playerRacket.movement[1] = 0


def main(gametype):
    pause = False
    countdown_animation()
    gameOver = False
    window.fill(pygame.Color('black'))
    pygame.display.set_caption('Ping-Pong')
    first_playerRacket = Racket(width/10, height/2, width/60, height/8)
    second_playerRacket = Racket(width - width/10, height/2, width/60, height/8)
    ball = Ball(width/2, height/2, 12, [4, 4])
    while not gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = False if pause else True
                if event.key == pygame.K_q:
                    return
                if event.key == pygame.K_w:
                    first_playerRacket.movement[1] = -8
                elif event.key == pygame.K_s:
                    first_playerRacket.movement[1] = 8
                if gametype == 2:
                    if event.key == pygame.K_UP:
                        second_playerRacket.movement[1] = -8
                    elif event.key == pygame.K_DOWN:
                        second_playerRacket.movement[1] = 8

            if event.type == pygame.KEYUP:
                first_playerRacket.movement[1] = 0
                if gametype == 2:
                    second_playerRacket.movement[1] = 0
        if pause:
            continue
        if gametype == 1:
            Bot.second_playerRacketmove(second_playerRacket, ball)
        window.blit(bg, (0, 0))
        displaytext('Press "Q" to exit', 8, 120, 580)
        displaytext('Press "ESC" to pause', 8, 640, 580)
        first_playerRacket.draw()
        second_playerRacket.draw()
        ball.draw()
        displaytext(str(first_playerRacket.points), 20, width/8, 25)
        displaytext(str(second_playerRacket.points), 20, width - width/8, 25)
        if pygame.sprite.collide_mask(first_playerRacket, ball):
            ball.movement[0] = -1*ball.movement[0]
            ball.movement[1] = ball.movement[1] - \
                int(0.1*random.randrange(5, 10)*first_playerRacket.movement[1])
            if ball.movement[1] > ball.maxspeed:
                ball.movement[1] = ball.maxspeed
            if ball.movement[1] < -1*ball.maxspeed:
                ball.movement[1] = -1*ball.maxspeed
            music(0)
        if pygame.sprite.collide_mask(second_playerRacket, ball):
            ball.movement[0] = -1*ball.movement[0]
            ball.movement[1] = ball.movement[1] - \
                int(0.1*random.randrange(5, 10)*second_playerRacket.movement[1])
            if ball.movement[1] > ball.maxspeed:
                ball.movement[1] = ball.maxspeed
            if ball.movement[1] < -1*ball.maxspeed:
                ball.movement[1] = -1*ball.maxspeed
            music(0)
        if ball.score == 1:
            second_playerRacket.points += 1
            ball.score = 0
        elif ball.score == -1:
            first_playerRacket.points += 1
            ball.score = 0
        if second_playerRacket.points == 10:
            displaytext('The second player won', 80, width/2, 300)
            pygame.display.update()
            sleep(2)
            return
        if first_playerRacket.points == 10:
            displaytext('The first player won', 80, width/2, 300)
            pygame.display.update()
            sleep(2)
            return
        first_playerRacket.update()
        ball.update()
        second_playerRacket.update()
        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()
    quit()


def run(gametype):
    main(gametype)
