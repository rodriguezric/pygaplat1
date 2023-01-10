import pygame
import sys
pygame.init()

from app.scene import level_editor_scene

level_idx = int(sys.argv[1]) if len(sys.argv) > 1 else 0
pygame.display.set_caption(f'Level Editor: {level_idx}')

level_editor_scene(level_idx=level_idx)
pygame.quit()
