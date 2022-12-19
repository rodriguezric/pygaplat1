import pygame
font = pygame.font.Font(None, 16)

def debug(text, pos):
    screen = pygame.display.get_surface()
    text_surf = font.render(text, False, 'white')
    text_rect = text_surf.get_rect(topleft=pos)
    screen.blit(text_surf, text_rect)
