import pygame
from pygame.locals import *
import os
import arkanoid
import pingpong
pygame.init()

bg = pygame.image.load('main_bg.png')
os.environ['SDL_VIDEO_CENTERED'] = '1'

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

clock = pygame.time.Clock()
FPS = 30

font = "game_font.ttf"


def text_format(message, textFont, textSize, textColor):
    newFont = pygame.font.Font(textFont, textSize)
    newText = newFont.render(message, 0, textColor)
    return newText


def main_menu():

    menu = True
    selected = "start"

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = "arkanoid"
                elif event.key == pygame.K_DOWN:
                    selected = "pingpong"
                if event.key == pygame.K_RETURN:
                    if selected == "arkanoid":
                        try:
                            arkanoid.run()
                        except Exception:
                            pass
                    if selected == "pingpong":
                        try:
                            pingpong.run()
                        except Exception:
                            pass

        screen.blit(bg, (0, 0))
        title = text_format("top games", font, 90, pygame.Color('yellow'))
        if selected == "arkanoid":
            text_arkanoid = text_format("arkanoid", font, 75, pygame.Color('white'))
        else:
            text_arkanoid = text_format("arkanoid", font, 75, pygame.Color('black'))
        if selected == "pingpong":
            text_quit = text_format("pingpong", font, 75, pygame.Color('white'))
        else:
            text_quit = text_format("pingpong", font, 75, pygame.Color('black'))

        title_rect = title.get_rect()
        start_rect = text_arkanoid.get_rect()
        quit_rect = text_quit.get_rect()

        screen.blit(title, (screen_width/2 - (title_rect[2]/2), 80))
        screen.blit(text_arkanoid, (screen_width/2 - (start_rect[2]/2), 300))
        screen.blit(text_quit, (screen_width/2 - (quit_rect[2]/2), 360))
        pygame.display.update()
        clock.tick(FPS)
        pygame.display.set_caption("Top games")


try:
    main_menu()
except Exception:
    pass

pygame.quit()
quit()
