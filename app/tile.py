import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__()
        self.image = pygame.Surface((32,32,))
        self.rect = self.image.get_rect(topleft=pos)
        self.image.fill(color)

class DialogTile(Tile):
    def __init__(self, pos, color, text_id):
        super().__init__(pos, color)
        self.text_id = text_id

def create_white_tile(pos):
    return Tile(pos, color='white')

def create_green_tile(pos):
    return Tile(pos, color='green')

def create_blue_tile(pos):
    return Tile(pos, color='blue')

def create_red_tile(pos):
    return Tile(pos, color='red')

