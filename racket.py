import pygame


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
