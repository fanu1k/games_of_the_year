import os
import pygame
import sys
import time
import math
import random
from pygame.locals import *
from time import sleep

pygame.init()

FPS = 60

scr_size = (width, height) = (800, 600)


clock = pygame.time.Clock()


window = pygame.display.set_mode(scr_size)
pygame.display.set_caption('Ping-Pong')

bg = pygame.image.load('game_bg.png')


font = pygame.font.Font('game_font.ttf', 32)

rect_y = -20
for _ in range(31):
    rect_y += 20
    time.sleep(0.15)
    pygame.draw.rect(window, pygame.Color('red'), (width//2,rect_y, 10, 10))
    pygame.display.update()

def displaytext(text, fontsize, x, y):
    global font
    text = font.render(text, 1, pygame.Color('yellow'))
    textpos = text.get_rect(centerx=x, centery=y)
    window.blit(text, textpos)


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
        if self.rect.left == 0:
            self.rect.centerx = width/2
            self.rect.centery = height/2
            self.movement = [random.randrange(-1, 2, 2)*4, random.randrange(-1, 2, 2)*4]
            self.score = 1

        if self.rect.right == width:
            self.rect.centerx = width/2
            self.rect.centery = height/2
            self.movement = [random.randrange(-1, 2, 2)*4, random.randrange(-1, 2, 2)*4]
            self.score = -1

        self.rect = self.rect.move(self.movement)
        self.checkbounds()

    def draw(self):
        pygame.draw.circle(self.image, self.color, (int(self.rect.width/2),
                                                    int(self.rect.height/2)), int(self.size/2))
        window.blit(self.image, self.rect)


class Bot(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def cpumove(cpu, ball):
        if ball.movement[0] > 0:
            if ball.rect.bottom > cpu.rect.bottom + cpu.rect.height/5:
                cpu.movement[1] = 8
            elif ball.rect.top < cpu.rect.top - cpu.rect.height/5:
                cpu.movement[1] = -8
            else:
                cpu.movement[1] = 0
        else:
            cpu.movement[1] = 0


def main():
    gameOver = False
    paddle = Racket(width/10, height/2, width/60, height/8)
    cpu = Racket(width - width/10, height/2, width/60, height/8)
    ball = Ball(width/2, height/2, 12, [4, 4])

    while not gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return
                if event.key == pygame.K_UP:
                    paddle.movement[1] = -8
                elif event.key == pygame.K_DOWN:
                    paddle.movement[1] = 8
            if event.type == pygame.KEYUP:
                paddle.movement[1] = 0
        Bot.cpumove(cpu, ball)
        window.blit(bg, (0,0))

        paddle.draw()
        cpu.draw()
        ball.draw()
        displaytext(str(paddle.points), 20, width/8, 25)
        displaytext(str(cpu.points), 20, width - width/8, 25)
        if pygame.sprite.collide_mask(paddle, ball):
            ball.movement[0] = -1*ball.movement[0]
            ball.movement[1] = ball.movement[1] - \
                int(0.1*random.randrange(5, 10)*paddle.movement[1])
            if ball.movement[1] > ball.maxspeed:
                ball.movement[1] = ball.maxspeed
            if ball.movement[1] < -1*ball.maxspeed:
                ball.movement[1] = -1*ball.maxspeed
        if pygame.sprite.collide_mask(cpu, ball):
            ball.movement[0] = -1*ball.movement[0]
            ball.movement[1] = ball.movement[1] - int(0.1*random.randrange(5, 10)*cpu.movement[1])
            if ball.movement[1] > ball.maxspeed:
                ball.movement[1] = ball.maxspeed
            if ball.movement[1] < -1*ball.maxspeed:
                ball.movement[1] = -1*ball.maxspeed
        if ball.score == 1:
            cpu.points += 1
            ball.score = 0
        elif ball.score == -1:
            paddle.points += 1
            ball.score = 0
        if cpu.points == 10:
            displaytext('You lost', 80, width/2, 300)
            pygame.display.update()
            sleep(2)
            pygame.quit()
            quit()
        if paddle.points == 10:
            displaytext('You win', 80, width/2, 300)
            pygame.display.update()
            sleep(2)
            pygame.quit()
            quit()
        paddle.update()
        ball.update()
        cpu.update()
        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()
    quit()

def run():
    main()