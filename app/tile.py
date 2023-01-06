import pygame

from app.mixins import PhysicsMixin
from app.behavior import up_down_left_right_behavior

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

class MovingTile(Tile, 
                 PhysicsMixin,):
    def __init__(self, pos, color):
        super().__init__(pos, color)
        self.init_physics_attributes()

        self.gravity = 0
        self.speed = 2

        self.behavior = None
        self.behavior_cycle = up_down_left_right_behavior
        self.behavior_frames = 0
        self.behavior_rate = 1

    def update(self):
        if self.behavior_cycle:
            self.behavior_frames += 1
            if self.behavior_frames % 30 == 0:
                self.behavior = next(self.behavior_cycle)
                self.behavior_frames = 0

        if self.behavior:
            self.behavior(self)

        self.move()

def create_colored_tile(color): 
    '''
    Used for generating colored tiles from level data
    '''
    return lambda pos: Tile(pos=pos, color=color)
