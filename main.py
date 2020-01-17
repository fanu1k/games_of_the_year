import pygame
from pygame.locals import *
import os
import operator
import leaders
from pygame import mixer
import arkanoid
import pingpong
import sqlite3
pygame.init()

bg = pygame.image.load('data/main_bg.png')
os.environ['SDL_VIDEO_CENTERED'] = '1'

font = 'game_font.ttf'

menu_sound = mixer.Sound('sounds/move.wav')

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


def upload_leader_board():
    conn = sqlite3.connect('leaders_base.db')
    c = conn.cursor()
    result = c.execute("""SELECT * FROM leaders""").fetchall()
    conn.commit()
    conn.close()
    leaders = {}
    for i in result:
        leaders[i[0]] = i[1]
    leaders = sorted(leaders.items(), key=lambda kv: kv[1])
    leaders.reverse()
    return leaders


def main_menu():
    global font
    menu = True
    selected = "start"
    first_button = 'arkanoid'
    second_button = "pingpong"
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = first_button
                elif event.key == pygame.K_DOWN:
                    selected = second_button
                menu_sound.play(0)
                if event.key == pygame.K_RETURN:
                    if selected == "arkanoid":
                        first_button = 'Start game'
                        second_button = 'Leaders bord'
                    if selected == "pingpong":
                        first_button = '1 player'
                        second_button = '2 players'
                    if selected == 'Start game':
                        arkanoid.run()
                    if selected == 'Leaders bord':
                        leaders.main(upload_leader_board())
                    if selected == '1 player':
                        pingpong.run(1)
                    if selected == '2 players':
                        pingpong.run(2)
                if event.key == pygame.K_q and first_button == 'arcanoid':
                    menu = False
                if event.key == pygame.K_q:
                    if first_button == '1 player' or first_button == 'Start game':
                        first_button = 'arkanoid'
                        second_button = 'pingpong'
                    else:
                        menu = False
        screen.blit(bg, (0, 0))
        title = text_format("top games", font, 90, pygame.Color('yellow'))
        if selected == first_button:
            text_arkanoid = text_format(first_button, font, 75, pygame.Color('white'))
        else:
            text_arkanoid = text_format(first_button, font, 75, pygame.Color('black'))
        if selected == second_button:
            text_quit = text_format(second_button, font, 75, pygame.Color('white'))
        else:
            text_quit = text_format(second_button, font, 75, pygame.Color('black'))

        title_rect = title.get_rect()
        start_rect = text_arkanoid.get_rect()
        quit_rect = text_quit.get_rect()

        screen.blit(title, (screen_width/2 - (title_rect[2]/2), 80))
        screen.blit(text_arkanoid, (screen_width/2 - (start_rect[2]/2), 300))
        screen.blit(text_quit, (screen_width/2 - (quit_rect[2]/2), 360))
        pygame.display.update()
        clock.tick(FPS)
        pygame.display.set_caption("Top games")

    pygame.quit()
    quit()


if __name__ == '__main__':
        main_menu()
