import pygame
from framework.screen import tile_size
from app.state import ActorState

class Enemy(pygame.sprite.Sprite):
    speed = 4
    jump_force = 8
    gravity = 0.5
    friction = 0.5
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.Surface((tile_size, tile_size))
        self.rect = self.image.get_rect(topleft=pos)

        # graphics
        self.image.fill('orange')

        # attributes
        self.movement = pygame.math.Vector2()
        self.state = ActorState.STANDING

        # rectangles for detecting collision
        self.horizontal_rect = self.rect.copy()
        self.horizontal_rect.width = 1
        self.vertical_rect = self.rect.copy()
        self.vertical_rect.height = 1

    def move(self):
        '''
        Update the rectangle based on the movement vector
        '''
        self.rect.x += self.movement.x
        self.rect.y += self.movement.y

    def update_horizontal_rect(self):
        '''
        Update rectangle used for horizontal collision detection
        '''
        if self.movement.x > 0:
            self.horizontal_rect.left = self.rect.right
        else:
            self.horizontal_rect.right = self.rect.left

        self.horizontal_rect.height = self.rect.height - 2 - abs(self.movement.y)

        if self.movement.y > 0:
            self.horizontal_rect.top = self.rect.top + self.movement.y
        if self.movement.y < 0:
            self.horizontal_rect.bottom = self.rect.bottom + self.movement.y
            
    def update_vertical_rect(self):
        '''
        Update rectangle used for vertical collision detection
        '''
        if self.movement.y > 0:
            self.vertical_rect.top = self.rect.bottom + self.movement.y
        else:
            self.vertical_rect.bottom = self.rect.top + self.movement.y

        self.vertical_rect.centerx = self.rect.centerx

        if self.state in (ActorState.STANDING, ActorState.WALKING):
            self.vertical_rect.width = self.rect.width - abs(self.movement.x)

        if self.movement.x > 0:
            self.vertical_rect.left = self.rect.left

        if self.movement.x < 0:
            self.vertical_rect.right = self.rect.right

    def apply_gravity(self):
        '''
        Increase vertical movement by gravity
        '''
        self.movement.y += self.gravity

    def apply_friction(self):
        '''
        Reduce horizontal movement if key isn't held
        Convert the result to integer because of how
        pygame handles negative numbers for movement
        '''
        self.movement.x *= self.friction // 1

    def handle_standing_state(self, keys):
        self.handle_horizontal_keys(keys)
        self.handle_jump_key(keys)
        
        if self.movement.y > self.gravity:
            self.state = ActorState.FALLING

    def handle_walking_state(self, keys):
        self.handle_horizontal_keys(keys)
        self.handle_jump_key(keys)
        
        if self.movement.x == 0:
            self.state = ActorState.WALKING

        if self.movement.y < 0:
            self.state = ActorState.JUMPING

        if self.movement.y > self.gravity:
            self.state = ActorState.FALLING

    def handle_jumping_state(self, keys):
        self.handle_horizontal_keys(keys)

        if self.movement.y > self.gravity:
            self.state = ActorState.FALLING

    def handle_falling_state(self, keys):
        self.handle_horizontal_keys(keys)

        if self.movement.y <= self.gravity:
            self.state = ActorState.STANDING

    def update(self):
        self.apply_gravity()
        self.apply_friction()

        # detect collisions before moving
        self.update_horizontal_rect()
        self.update_vertical_rect()
        self.move()
