from pygame.font import Font, get_default_font

# Path to font, prstart for now
font_path = get_default_font()

# Font factory for creating fonts of different sizes
def font_factory(size):
    return Font(font_path, size)

# Standard size will be 16 for framework
font_16 = font_factory(16)
