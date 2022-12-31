import pygame
from framework.screen import tile_size
from app.state import PlayerState

class Player(pygame.sprite.Sprite):
    speed = 4
    jump_force = 8
    gravity = 0.5
    friction = 0.5
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.Surface((tile_size, tile_size))
        self.rect = self.image.get_rect(topleft=pos)

        # graphics
        self.image.fill('green')

        # attributes
        self.movement = pygame.math.Vector2()
        self.state = PlayerState.STANDING

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

        if self.state in (PlayerState.STANDING, PlayerState.WALKING):
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
        if keys[pygame.K_SPACE]:
            self.movement.y = -self.jump_force
            # May want to decouple this state change 
            # from the key handler.
            self.state = PlayerState.JUMPING
            self.update_vertical_rect()

    def handle_standing_state(self, keys):
        self.handle_horizontal_keys(keys)
        self.handle_jump_key(keys)
        
        if self.movement.y > self.gravity:
            self.state = PlayerState.FALLING

    def handle_walking_state(self, keys):
        self.handle_horizontal_keys(keys)
        self.handle_jump_key(keys)
        
        if self.movement.x == 0:
            self.state = PlayerState.WALKING

        if self.movement.y < 0:
            self.state = PlayerState.JUMPING

        if self.movement.y > self.gravity:
            self.state = PlayerState.FALLING

    def handle_jumping_state(self, keys):
        self.handle_horizontal_keys(keys)

        if self.movement.y > self.gravity:
            self.state = PlayerState.FALLING

    def handle_falling_state(self, keys):
        self.handle_horizontal_keys(keys)

        if self.movement.y <= self.gravity:
            self.state = PlayerState.STANDING

    def key_inputs(self):
        keys = pygame.key.get_pressed()
        { # Register states to handler methods
            PlayerState.STANDING: self.handle_standing_state,
            PlayerState.WALKING: self.handle_walking_state,
            PlayerState.JUMPING: self.handle_jumping_state,
            PlayerState.FALLING: self.handle_falling_state,
        }.get(self.state)(keys)
    
    def update(self):
        '''
        Update the player every clock tick
        '''
        self.apply_gravity()
        self.apply_friction()

        # handles inputs based on player state
        self.key_inputs()

        # detect collisions before moving
        self.update_horizontal_rect()
        self.update_vertical_rect()
        self.move()

