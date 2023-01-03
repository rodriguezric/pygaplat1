import pygame
from app.state import Direction

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, direction, color='white'):
        super().__init__()
        
        self.image = pygame.Surface((8,8,))
        self.rect = self.image.get_rect(topleft=pos)
        
        # graphics
        self.image.fill(color)

        self.direction = direction

        # attributes
        self.frame = 0
        self.speed = 6
        self.life = 1

    def move(self):
        '''
        Move depending on the direction
        '''
        if self.direction == Direction.LEFT:
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

    def decay(self):
        '''
        Every frame increment self.frame
        When 30 frames pass, decrement life
        When life is <= 0, kill yourself
        '''
        self.frame += 1

        if self.frame % 30 == 0:
            self.frame = 0
            self.life -= 1
    
        if self.life <= 0:
            self.kill()

    def update(self):
        '''
        Update the projectile every clock tick
        '''
        self.decay()
        self.move() 
