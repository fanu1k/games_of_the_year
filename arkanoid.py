import math
import pygame
from pygame import mixer
from random import randint as rnd
from time import sleep
pygame.init()
mixer.init()

block_width = 25
block_height = 15

bg = pygame.image.load('arkanoid_bg.png')

wall_hit_sound = mixer.Sound('arcanoid_wall.wav')
destroy_sound = mixer.Sound('arcanoid_brick.wav')
lose_life_sound = mixer.Sound('lose.wav')


def music(number):
    if number == 1:
        wall_hit_sound.play(0)
    elif number == 2:
        lose_life_sound.play(0)
    else:
        destroy_sound.play(0)

class Bonus(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([block_width, block_height])

        self.image.fill(pygame.Color('blue'))

        self.rect = self.image.get_rect()

        self.rect.x = 50
        self.rect.y = 50
    
    def update(self, pos):
        self.pos = pos
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        


class Block(pygame.sprite.Sprite):

    def __init__(self, color, x, y, lifes):

        super().__init__()

        self.image = pygame.Surface([block_width, block_height])

        self.image.fill(color)

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        self.lifes = lifes
        if rnd(0,100) < 100:
            self.bonus = True
        else:
            self.bonus = False
    def bonused(self):
        return True if self.bonus else False

    def kill_life(self):
        self.lifes -= 1
        if self.lifes == 1:
            self.image.fill(pygame.Color('red'))
        elif self.lifes == 2:
            self.image.fill(pygame.Color('green'))
        elif self.lifes == 3:
            self.image.fill(pygame.Color('orange'))
        return self.lifes


class Ball(pygame.sprite.Sprite):

    x = 0.0
    y = 170.0

    direction = 220

    width = 10
    height = 10

    def __init__(self):
        super().__init__()

        self.image = pygame.Surface([self.width, self.height])

        self.image.fill(pygame.Color('yellow'))

        self.rect = self.image.get_rect()

        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

        self.speed = 7

    def nxt_lvl(self, lvl):
        self.speed = 7 + 1 * lvl

    def bounce(self, diff):

        self.direction = (180 - self.direction) % 360
        self.direction -= diff

    def update(self):

        direction_radians = math.radians(self.direction)

        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)

        self.rect.x = self.x
        self.rect.y = self.y
        if self.y <= 0:
            self.bounce(0)
            self.y = 1
            music(1)
        if self.x <= 0:
            self.direction = (360 - self.direction) % 360
            self.x = 1
            music(1)
        if self.x > self.screenwidth - self.width:
            self.direction = (360 - self.direction) % 360
            self.x = self.screenwidth - self.width - 1
            music(1)
        if self.y > 600:
            music(2)
            return True
        else:
            return False


class Player(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.width = 75
        self.height = 15
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((pygame.Color('purple')))

        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

        self.rect.x = 0
        self.rect.y = self.screenheight-self.height

    def update(self):

        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]
        if self.rect.x > self.screenwidth - self.width:
            self.rect.x = self.screenwidth - self.width


def main(lvl):
    global font
    pygame.init()

    life = 3

    screen = pygame.display.set_mode([800, 600])

    pygame.display.set_caption('Arkanoid')

    pygame.mouse.set_visible(0)

    font = pygame.font.Font('game_font.ttf', 36)

    background = pygame.Surface(screen.get_size())

    blocks = pygame.sprite.Group()
    balls = pygame.sprite.Group()
    allsprites = pygame.sprite.Group()
    two_lvl_blocks = pygame.sprite.Group()
    three_lvl_blocks = pygame.sprite.Group()
    bonuses = pygame.sprite.Group()
    player = Player()
    allsprites.add(player)

    bonus = Bonus()

    ball = Ball()
    allsprites.add(ball)
    balls.add(ball)
    ball.nxt_lvl(lvl)

    top = 80

    blockcount = 32

    for row in range(5):
        for column in range(0, blockcount):

            if rnd(0, 100) < (7 * lvl):
                block = Block(pygame.Color('orange'), column *
                              (block_width + 2) + 1, top, 3)
                three_lvl_blocks.add(block)
            elif rnd(0, 100) < (10 * lvl):
                block = Block(pygame.Color('green'), column *
                              (block_width + 2) + 1, top, 2)
                two_lvl_blocks.add(block)
            else:
                block = Block(pygame.Color('red'), column *
                              (block_width + 2) + 1, top, 1)
                blocks.add(block)
            allsprites.add(block)
        top += block_height + 2

    clock = pygame.time.Clock()

    game_over = False

    exit_program = False

    while not exit_program:
        screen.blit(bg, (0, 0))
        screen.blit(font.render('Press "Q" to exit', 1, pygame.Color('yellow')), (10, 560))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return None
            if event.type == pygame.QUIT:
                exit_program = True

        if not game_over:
            player.update()
            game_over = ball.update()

        if game_over:
            if life:
                life -= 1
                game_over = False
                ball.kill()
                ball = Ball()
                ball.nxt_lvl(lvl)
                allsprites.add(ball)
                balls.add(ball)
                text = font.render(f"Lifes - {life}", True, pygame.Color('green'))
                textpos = text.get_rect(centerx=background.get_width() / 2)
                textpos.top = 300
                screen.blit(text, textpos)
                pygame.display.flip()
                sleep(0.75)
            else:
                text = font.render("Game Over", True, pygame.Color('white'))
                textpos = text.get_rect(centerx=background.get_width() / 2)
                textpos.top = 300
                screen.blit(text, textpos)
                pygame.display.flip()
                sleep(0.75)
                return False

        if pygame.sprite.spritecollide(player, balls, False):

            diff = (player.rect.x + player.width / 2) - \
                (ball.rect.x + ball.width / 2)
            ball.rect.y = screen.get_height() - player.rect.height - ball.rect.height - 1
            ball.bounce(diff)
            music(1)

        deadblocks = pygame.sprite.spritecollide(ball, blocks, False)
        two_lvl_deadblocks = pygame.sprite.spritecollide(ball, two_lvl_blocks, False)
        three_lvl_deadblocks = pygame.sprite.spritecollide(ball, three_lvl_blocks, False)

        if len(deadblocks) > 0:
            ball.bounce(0)
            music(0)
            for i in range(len(deadblocks)):
                if deadblocks[i].kill_life() == 0:
                    if deadblocks[i].bonused():
                        bonus.update([50, 50])
                    deadblocks[i].kill()
        if len(two_lvl_deadblocks) > 0:
            ball.bounce(0)
            music(0)
            for i in range(len(two_lvl_deadblocks)):
                if two_lvl_deadblocks[i].kill_life() == 0:
                    two_lvl_deadblocks[i].kill()
        if len(three_lvl_deadblocks) > 0:
            ball.bounce(0)
            music(0)
            for i in range(len(three_lvl_deadblocks)):
                if three_lvl_deadblocks[i].kill_life() == 0:
                    three_lvl_deadblocks[i].kill()

        if len(blocks) + len(two_lvl_blocks) + len(three_lvl_blocks) == 0:
            return True

        allsprites.draw(screen)
        clock.tick(30)
        pygame.display.flip()

    pygame.quit()


def run():
    for i in range(0, 10):
        tmp = main(0)
        if not tmp:
            break