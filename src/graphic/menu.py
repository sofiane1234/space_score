import pygame

class Menu(pygame.sprite.Sprite):
    def __init__(self, pos, img):
        super().__init__()
        self.pos = pos
        self.img = img