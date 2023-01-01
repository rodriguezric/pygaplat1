import pygame
from framework.screen import tile_size

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.Surface((tile_size, tile_size))
        self.rect = self.image.get_rect(topleft=pos)

        self.image.fill('orange')

    def update(self):
        pass
