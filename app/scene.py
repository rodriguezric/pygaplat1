import pygame
import sys
from pygame.locals import *

from framework.screen import screen, WIDTH, HEIGHT, tile_size
from framework.text import Text, ScrollingText, center_text, draw_text

# Event for determining which level to load
NEXTLEVEL = pygame.USEREVENT + 1

# Event for setting running=False
STOPRUNNING = pygame.USEREVENT + 2

level_files = ['level1.csv',
               'level2.csv',
               'level3.csv',]

def stop_running():
    pygame.event.post(pygame.event.Event(STOPRUNNING))

def quit_game():
    pygame.quit()
    sys.exit()

cursor_text = Text(">")
cursor_height = 20
def cursor_event_handler(event, cursor, menu_list):
    if event.type == KEYDOWN:
        if event.key == K_RETURN:
            menu_list[cursor][1]()

        if event.key == K_UP:
            cursor -= 1
            if cursor < 0:
                cursor = len(menu_list) - 1

        if event.key == K_DOWN:
            cursor += 1
            if cursor > len(menu_list) - 1:
                cursor = 0

    return cursor

def menu_scene(title_text=None, menu_list=None, background_color='black'):
    cursor = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                quit_game()

            if event.type == STOPRUNNING:
                running = False

            cursor = cursor_event_handler(event, cursor, menu_list)
        
        screen.fill(background_color)
        center_text(title_text, HEIGHT//3)

        for (idx, (text, _)) in enumerate(menu_list):
            draw_text(text, WIDTH//2-20, HEIGHT//2 + idx*cursor_height)

        draw_text(cursor_text, WIDTH//2-40, HEIGHT//2 + (cursor*cursor_height))
        pygame.display.flip()

clock = pygame.time.Clock()
def main_scene():
    running = True

    main_text = Text('PYGAPLAT1')
    scrolling_text = ScrollingText('WELCOME TO THE FIRST EDITION')
    enter_text = Text('PRESS ENTER TO BEGIN')
    cursor = 0
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                quit_game()

            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if not scrolling_text.finished:
                        scrolling_text.fill()
                    else:
                        running = False
                        game_scene(0)
                        return

        screen.fill('black')

        center_text(main_text, HEIGHT//3)
        center_text(scrolling_text, HEIGHT//3+20)
        if scrolling_text.finished:
            center_text(enter_text)

        scrolling_text.inc()
        pygame.display.flip()
        clock.tick(5)

def pause_scene():
    title_text = Text("PAUSE")
    menu_list = [(Text("CONTINUE"), lambda: stop_running()),
                 (Text("QUIT"), lambda: quit_game()),]

    menu_scene(title_text, menu_list, 'black')


def game_scene(level_idx):
    from app.player import Player
    player = pygame.sprite.GroupSingle()
    player.add(Player((50,50)))


    from app.tile import create_white_tile, create_red_tile, create_blue_tile
    tiles = pygame.sprite.Group()
    hazzards = pygame.sprite.Group()
    goals = pygame.sprite.Group()

    import csv
    level = []
    with open(level_files[level_idx]) as f:
        level = list(csv.reader(f))

    tile_dict = {'1': create_white_tile,}
    hazzard_dict = {'2': create_red_tile,}
    goal_dict = {'D': create_blue_tile,}


    for row_idx, row in enumerate(level):
        for col_idx, tile_key in enumerate(row):
            tile_fn = tile_dict.get(tile_key)
            if tile_fn:
                tiles.add(tile_fn((tile_size*col_idx, tile_size*row_idx)))

            hazzard_fn = hazzard_dict.get(tile_key)
            if hazzard_fn:
                hazzards.add(hazzard_fn((tile_size*col_idx, tile_size*row_idx)))
        
            goal_fn = goal_dict.get(tile_key)
            if goal_fn:
                goals.add(goal_fn((tile_size*col_idx, tile_size*row_idx)))
    
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                quit_game()
            
            if event.type == KEYDOWN:
                # Pause the game on Escape
                if event.key == K_ESCAPE:
                    pause_scene()
                if event.key == K_SPACE:
                    player.sprite.jump()

            if event.type == NEXTLEVEL:
                if level_idx == len(level_files)-1:
                    # we beat the game
                    end_scene() 
                else:
                    # next level
                    game_scene(level_idx+1)
                

        screen.fill('black')

        tiles.draw(screen)
        hazzards.draw(screen)
        goals.draw(screen)


        for sprite in tiles.sprites():
            '''
            Horizontal
            Make a copy of the player's rectangle to represent horizontal
            collisions. Set the width of that rectangle to the horizontal
            movement of the player. If the player is moving left, attach
            the new rectangle to the left. Vice versa for right. 
            To prevent vertical collisions, subtract the vertical speed
            of the player from the collision rectangle.
            '''
            if player.sprite.movement.x != 0:
                if sprite.rect.colliderect(player.sprite.horizontal_rect):
                    if player.sprite.movement.x > 0:
                        player.sprite.rect.right = sprite.rect.left
                    if player.sprite.movement.x < 0:
                        player.sprite.rect.left = sprite.rect.right
                    player.sprite.movement.x = 0
            

            # Vertical
            if abs(player.sprite.movement.y) > player.sprite.gravity:
                player.sprite.is_on_floor = False

            if player.sprite.movement.y != 0:
                if sprite.rect.colliderect(player.sprite.vertical_rect):
                    if player.sprite.movement.y > 0:
                        player.sprite.rect.bottom = sprite.rect.top
                        player.sprite.is_on_floor = True
                    else:
                        player.sprite.rect.top = sprite.rect.bottom
                    player.sprite.movement.y = 0
                
        player.draw(screen)
        player.update()

        if pygame.sprite.spritecollide(player.sprite, hazzards, False):
            lose_scene()
            return

        if pygame.sprite.spritecollide(player.sprite, goals, False):
            pygame.event.post(pygame.event.Event(NEXTLEVEL))

        pygame.display.flip()
        clock.tick(60)

def end_scene():
    running = True

    main_text = Text('THE END')
    scrolling_text = ScrollingText('YOU BEAT THE GAME!')
    enter_text = Text('PRESS ENTER TO TRY AGAIN')

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                quit_game()

            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if not scrolling_text.finished:
                        scrolling_text.fill()
                    else:
                        running = False
                        game_scene(0)
                        return

        screen.fill('black')

        center_text(main_text, HEIGHT//3)
        center_text(scrolling_text, HEIGHT//3+20)
        if scrolling_text.finished:
            center_text(enter_text)

        scrolling_text.inc()
        pygame.display.flip()
        clock.tick(5)

def lose_scene():
    title_text = Text("YOU LOSE!")
    menu_list = [(Text("TRY AGAIN"), lambda: game_scene(0)),
                 (Text("QUIT"), lambda: quit_game()),]

    menu_scene(title_text, menu_list, 'red')

