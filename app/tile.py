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

def create_colored_tile(color): 
    '''
    Used for generating colored tiles from level data
    '''
    return lambda pos: Tile(pos=pos, color=color)
