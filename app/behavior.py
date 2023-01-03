'''
Behaviors are small functions that modify an entity.
They are meant to be used with itertools.cycle so it
can be looped indefinitely as behavior.
'''
from itertools import cycle

def stand(self):
    self.movement.x = 0

def move_left(self):
    self.movement.x = -self.speed

def move_right(self):
    self.movement.x = self.speed

pacing_behavior = cycle([stand, 
                         move_left, 
                         stand, 
                         move_right,])
