'''
Behaviors are small functions that modify an entity.
They are meant to be used with itertools.cycle so it
can be looped indefinitely as behavior.
'''
from itertools import cycle
from app.state import Direction, ActorState

def stand(self):
    self.movement.x = 0

def freeze(self):
    self.movement.x = 0
    self.movement.y = 0

def move_left(self):
    self.movement.x = -self.speed

def move_right(self):
    self.movement.x = self.speed

def move_up(self):
    self.movement.y = -self.speed

def move_down(self):
    self.movement.y = self.speed

def face_left(self):
    self.direction = Direction.LEFT

def face_right(self):
    self.direction = Direction.RIGHT

def attack(self):
    self.attack()

def jump(self):
    self.movement.y = -self.speed

def jump_left(self):
    move_left(self)
    jump(self)

def jump_right(self):
    move_right(self)
    jump(self)

# Behavior cycles
def pacing_behavior():
    return cycle([
        stand, 
        move_left, 
        stand, 
        move_right,
    ])

def pacing_jumping_behavior():
    return cycle([
        stand,
        jump_left,
        stand,
        jump_right,
    ])

def up_down_left_right_behavior():
    return cycle([
        freeze,
        move_up,
        freeze,
        move_down,
        freeze,
        move_left,
        freeze,
        move_right,
    ])
