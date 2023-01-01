import pygame
from framework.screen import tile_size
from app.state import ActorState

from app.mixins import (ActorStateMixin, 
                        CollisionRectMixin,
                        PhysicsMixin,)

class Enemy(pygame.sprite.Sprite,
             ActorStateMixin,
             CollisionRectMixin,
             PhysicsMixin,):
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.Surface((tile_size, tile_size))
        self.rect = self.image.get_rect(topleft=pos)

        # graphics
        self.image.fill('red')

        self.init_physics_attributes()
        self.init_state_attributes()
        self.init_collision_rects()

    def update(self):
        self.apply_gravity()
        self.apply_friction()

        # detect collisions before moving
        self.update_horizontal_rect()
        self.update_vertical_rect()
        self.move()
