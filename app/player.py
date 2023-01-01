import pygame
from framework.screen import tile_size
from app.state import ActorState

from app.mixins import (ActorStateMixin, 
                        CollisionRectMixin,
                        PhysicsMixin,)

class Player(pygame.sprite.Sprite,
             ActorStateMixin,
             CollisionRectMixin,
             PhysicsMixin,):
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.Surface((tile_size, tile_size))
        self.rect = self.image.get_rect(topleft=pos)

        # graphics
        self.image.fill('green')

        self.init_physics_attributes()
        self.init_state_attributes()
        self.init_collision_rects()

    def handle_horizontal_keys(self, keys):
        '''
        Moves the player left and right. At the moment this 
        is trivial, but we could have separate methods for 
        working with different states of the player.
        '''
        if keys[pygame.K_LEFT]:
            self.movement.x = -self.speed
        
        if keys[pygame.K_RIGHT]:
            self.movement.x = self.speed

    def handle_jump_key(self, keys):
        '''
        Moves the player vertically. We do make a special 
        call to update the vertical collision rectangle.
        '''
        illegal_states = (ActorState.JUMPING, ActorState.FALLING)
        if keys[pygame.K_SPACE] and self.state not in illegal_states:
            self.movement.y = -self.jump_force
            # May want to decouple this state change 
            # from the key handler.
            self.state = ActorState.JUMPING
            self.update_vertical_rect()
    
    def update(self):
        '''
        Update the player every clock tick
        '''
        self.apply_gravity()
        self.apply_friction()

        keys = pygame.key.get_pressed()
        self.handle_horizontal_keys(keys)
        self.handle_jump_key(keys)
        
        self.handle_states()

        # detect collisions before moving
        self.update_horizontal_rect()
        self.update_vertical_rect()
        self.move()

