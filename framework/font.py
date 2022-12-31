from pygame.font import Font, get_default_font

# Font factory for creating fonts of different sizes
def font_factory(size):
    return Font('fonts/prstart.ttf', size)

# Standard size will be 16 for framework
font_16 = font_factory(16)
font_32 = font_factory(32)
