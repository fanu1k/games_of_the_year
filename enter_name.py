import pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
font = pygame.font.Font('game_font.ttf', 65)

def displaytext(text, x, y, color):
    text = font.render(text, 1, color)
    textpos = (x, y)
    screen.blit(text, textpos)

def main():
    player_name = ''
    bg = pygame.image.load('data/enter_name_bg.jpg')
    runGame = True
    while runGame:
        screen.blit(bg, (0, 0))
        displaytext('Enter your name and press "Enter"', 30, 60, pygame.Color('green'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runGame = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return player_name
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode
        displaytext(player_name, 100, 300, pygame.Color('purple'))
        pygame.display.flip()
    pygame.quit()