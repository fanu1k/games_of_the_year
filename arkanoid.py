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

font = pygame.font.Font('game_font.ttf', 36)

screen = pygame.display.set_mode([800, 600])

scores = 0


def displaytext(text, x, y, color, flag):
    global font
    text = font.render(text, 1, color)
    textpos = text.get_rect(centerx=x, centery=y)
    if flag:
        textpos.top = 300
    screen.blit(text, textpos)


def music(number):
    if number == 1:
        wall_hit_sound.play(0)
    elif number == 2:
        lose_life_sound.play(0)
    else:
        destroy_sound.play(0)


class Bonus(pygame.sprite.Sprite):

    def __init__(self, coord):
        super().__init__()

        self.image = pygame.Surface([15, 15])
        bonus = rnd(1, 7)
        if bonus == 1:
            self.image.fill(pygame.Color("green"))
            self.skill = 'balls'
        if bonus == 2:
            self.image.fill(pygame.Color("white"))
            self.skill = '+width'
        if bonus == 3:
            self.image.fill(pygame.Color("pink"))
            self.skill = 'slow'
        if bonus in 4:
            self.image.fill(pygame.Color("gray"))
            self.skill = 'fast'
        if bonus == 5:
            self.image.fill(pygame.Color("purple"))
            self.skill = 'life'
        if bonus == 6:
            self.image.fill(pygame.Color("blue"))
            self.skill = '-width'
        if bonus == 7:
            self.image.fill(pygame.Color("red"))
            self.skill = 'fireball'
        self.rect = self.image.get_rect()
        self.rect.x = coord[0]
        self.rect.y = coord[-1]

    def update(self):
        self.rect.y += 3

    def bonus_skill(self):
        return self.skill


class Block(pygame.sprite.Sprite):

    def __init__(self, color, x, y, lifes):

        super().__init__()

        self.image = pygame.Surface([block_width, block_height])

        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.coordinat = [x, y]
        self.rect.x = x
        self.rect.y = y
        self.lifes = lifes
        if rnd(0, 100) < 50:
            self.bonus = True
        else:
            self.bonus = False

    def bonused(self):
        return self.bonus

    def coord(self):
        return self.coordinat

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

    direction = 220

    width = 10
    height = 10

    def __init__(self, x=0.0, fire=False):
        super().__init__()
        self.fire = fire
        self.image = pygame.Surface([self.width, self.height])
        if self.fire:
            color = pygame.Color('red')
        else:
            color = pygame.Color('yellow')
        self.image.fill(color)
        self.x = x
        self.y = 270.0
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

    def isfire(self):
        return self.fire


class Player(pygame.sprite.Sprite):

    def __init__(self, width=75):

        super().__init__()

        self.width = width if width >= 15 else 15
        self.height = 15
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((pygame.Color('purple')))

        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

        self.rect.x = 0
        self.rect.y = self.screenheight-self.height

    def update(self, new_pos=True):
        if new_pos:
            pos = pygame.mouse.get_pos()
        else:
            pos = [10000, ]
        self.rect.x = pos[0]
        if self.rect.x > self.screenwidth - self.width:
            self.rect.x = self.screenwidth - self.width


def main(lvl):
    pause = False
    global font
    global scores
    pygame.init()

    life = 3

    pygame.display.set_caption('Arkanoid')

    pygame.mouse.set_visible(0)

    background = pygame.Surface(screen.get_size())

    blocks = pygame.sprite.Group()
    balls = pygame.sprite.Group()
    allsprites = pygame.sprite.Group()
    two_lvl_blocks = pygame.sprite.Group()
    three_lvl_blocks = pygame.sprite.Group()
    bonuses = pygame.sprite.Group()

    player = Player()
    allsprites.add(player)

    ball = Ball()
    allsprites.add(ball)
    balls.add(ball)
    ball.nxt_lvl(lvl)

    top = 80

    blockcount = 30

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
        displaytext('Press "Q" to exit', 110, 570,
                    pygame.Color('yellow'), False)
        displaytext(f'lifes - {life}', 730, 50, pygame.Color('red'), False)
        displaytext(f'scores: {str(scores)}', 70, 50, pygame.Color('white'), False)
        displaytext(f'Press "ESC" to pause', 660, 570, pygame.Color('yellow'), False)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return None
                if event.key == pygame.K_ESCAPE:
                    pause = False if pause else True
            if event.type == pygame.QUIT:
                exit_program = True

        if not game_over:
            if not pause:
                player.update()
                for bal in balls:
                    tmp = bal.update()
                    if tmp:
                        bal.kill()
                        game_over = tmp
                bonuses.update()

        if game_over:
            game_over = False
            if len(balls) == 0:
                if life:
                    life -= 1
                    for i in balls:
                        i.kill()
                    ball = Ball()
                    ball.nxt_lvl(lvl)
                    allsprites.add(ball)
                    balls.add(ball)
                    displaytext(f"Lifes - {life}", 400, 300, pygame.Color('green'), True)
                    pygame.display.flip()
                    sleep(0.75)
                    scores -= 100
                else:
                    displaytext("Game Over", 400, 300,
                                pygame.Color('white'), True)
                    pygame.display.flip()
                    sleep(0.75)
                    return False

        collide_ball = pygame.sprite.spritecollide(player, balls, False)
        if len(collide_ball) > 0:
            diff = 0
            collide_ball[-1].rect.y = screen.get_height() - \
                player.rect.height - collide_ball[-1].rect.height - 1
            collide_ball[-1].bounce(diff)
            music(1)

        deadbonus = pygame.sprite.spritecollide(player, bonuses, True)

        if len(deadbonus) > 0:
            bonus = deadbonus[0]
            if bonus.bonus_skill() == 'balls':
                for _ in range(3):
                    ball = Ball(rnd(10, 790))
                    allsprites.add(ball)
                    balls.add(ball)
                    ball.nxt_lvl(lvl)
                    ball.bounce(rnd(0, 360))
            elif bonus.bonus_skill() == '-width':
                player.update(False)
                width = player.width
                player.kill()
                player = Player(width - 15)
                allsprites.add(player)
                player.update()
            elif bonus.bonus_skill() == '+width':
                player.update(False)
                width = player.width
                player.kill()
                player = Player(width + 15)
                allsprites.add(player)
                player.update()
            elif bonus.bonus_skill() == 'fireball':
                ball = Ball(rnd(10, 790), fire=True)
                allsprites.add(ball)
                balls.add(ball)
                ball.nxt_lvl(lvl)
                ball.bounce(rnd(0, 360))
            elif bonus.bonus_skill() == 'slow':
                for ball in balls:
                    ball.speed -= 2
            elif bonus.bonus_skill() == 'fast':
                for ball in balls:
                    ball.speed += 2
            elif bonus.bonus_skill() == 'life':
                life += 1

        for ball in balls:
            deadblocks = pygame.sprite.spritecollide(ball, blocks, False)
            two_lvl_deadblocks = pygame.sprite.spritecollide(
                ball, two_lvl_blocks, False)
            three_lvl_deadblocks = pygame.sprite.spritecollide(
                ball, three_lvl_blocks, False)
            if (len(deadblocks) + len(two_lvl_deadblocks) + len(three_lvl_deadblocks)) > 0:
                scores += 10
                if not ball.isfire():
                    ball.bounce(0)
                    music(0)
                break

        if len(deadblocks) > 0:
            for i in range(len(deadblocks)):
                if deadblocks[i].kill_life() == 0:
                    if deadblocks[i].bonused():
                        bonus = Bonus(deadblocks[i].coord())
                        bonuses.add(bonus)
                        allsprites.add(bonus)
                    deadblocks[i].kill()

        if len(two_lvl_deadblocks) > 0:
            for i in range(len(two_lvl_deadblocks)):
                if two_lvl_deadblocks[i].kill_life() == 0:
                    if two_lvl_deadblocks[i].bonused():
                        bonus = Bonus(two_lvl_deadblocks[i].coord())
                        bonuses.add(bonus)
                        allsprites.add(bonus)
                    two_lvl_deadblocks[i].kill()
        if len(three_lvl_deadblocks) > 0:
            for i in range(len(three_lvl_deadblocks)):
                if three_lvl_deadblocks[i].kill_life() == 0:
                    if three_lvl_deadblocks[i].bonused():
                        bonus = Bonus(three_lvl_deadblocks[i].coord())
                        bonuses.add(bonus)
                        allsprites.add(bonus)
                    three_lvl_deadblocks[i].kill()

        if len(blocks) == 0:
            displaytext(f"lvl {lvl + 2}", 400, 300, pygame.Color('white'), True)
            pygame.display.flip()
            sleep(1)
            return True

        allsprites.draw(screen)
        clock.tick(30)
        pygame.display.flip()

    pygame.quit()


def run():
    for i in range(0, 10):
        tmp = main(i)
        if not tmp:
            break
run()