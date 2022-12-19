from pygame.time import Clock

def scene(fn):
    ''' Scene decorator to reduce boilerplate ''' 
    def wrapper():
        running = True
        clock = Clock()
        fn()
    return wrapper()
        
