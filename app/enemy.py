import pygame
from framework.screen import tile_size
from app.state import ActorState

from app.mixins import (ActorStateMixin, 
                        CollisionRectMixin,
                        PhysicsMixin,)

from app.behavior import pacing_behavior, pacing_jumping_behavior
from random import randint

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


        self.speed = 2
        self.behavior = None
        self.behavior_cycle = pacing_jumping_behavior()
        for _ in range(randint(0, 10)): next(self.behavior_cycle)
        self.behavior_frames = 0
        self.behavior_rate = 1

    def update(self):
        self.apply_gravity()
        self.apply_friction()

        if self.behavior_cycle:
            self.behavior_frames += self.behavior_rate 
            if int(self.behavior_frames % 30) == 0:
                self.behavior = next(self.behavior_cycle)
                self.behavior_frames = 0

        if self.behavior:
            self.behavior(self)

        # detect collisions before moving
        self.update_horizontal_rect()
        self.update_vertical_rect()
        self.move()
