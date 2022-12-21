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
    '''
    Post event to stop running a scene. This will effectively
    set the running value to False in a scene that uses it.
    '''
    pygame.event.post(pygame.event.Event(STOPRUNNING))

def quit_game():
    '''
    Call both pygame.quit() and sys.exit() to cleanly exit game
    '''
    pygame.quit()
    sys.exit()

cursor_text = Text(">")
cursor_height = 20
def handle_cursor_event(event, cursor, menu_list):
    if not event.type == KEYDOWN:
        return cursor

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

def handle_quit_event(event):
    if event.type == QUIT:
        quit_game()

def menu_scene(title_text=None, menu_list=None, background_color='black'):
    '''
    Creates a menu scene with a cursor interface.
    title_text is the text that will be shown in the middle of the scene.
    menu_list is a list of tuples, where the first element is a text obj
        and the second object is a function to call when pressing enter
    background_color is the color of the scene.
    '''
    cursor = 0

    running = True
    while running:
        for event in pygame.event.get():
            handle_quit_event(event)

            if event.type == STOPRUNNING:
                running = False

            cursor = handle_cursor_event(event, cursor, menu_list)
        
        screen.fill(background_color)
        center_text(title_text, HEIGHT//3)

        for (idx, (text, _)) in enumerate(menu_list):
            draw_text(text, WIDTH//2-20, HEIGHT//2 + (idx*cursor_height))

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
            handle_quit_event(event)

            if not event.type == KEYDOWN:
                continue
            if not event.key == K_RETURN:
                continue
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
    menu_list = [(Text("CONTINUE"), stop_running),
                 (Text("QUIT"), quit_game),]

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
            coordinates = (tile_size * col_idx, tile_size * row_idx)

            tile_fn = tile_dict.get(tile_key)
            if tile_fn:
                tiles.add(tile_fn(coordinates))

            hazzard_fn = hazzard_dict.get(tile_key)
            if hazzard_fn:
                hazzards.add(hazzard_fn(coordinates))
        
            goal_fn = goal_dict.get(tile_key)
            if goal_fn:
                goals.add(goal_fn(coordinates))
    
    running = True

    def handle_keydown_event(event):
        if not event.type == KEYDOWN:
            return
        if event.key == K_ESCAPE:
            pause_scene()
        if event.key == K_SPACE:
            player.sprite.jump()
    
    def handle_next_level_event(event):
        if not event.type == NEXTLEVEL:
            return

        if level_idx == len(level_files)-1:
            # we beat the game
            end_scene() 
        else:
            # next level
            game_scene(level_idx+1)

    def handle_horizontal_collision(sprite):
        if player.sprite.movement.x != 0:
            if sprite.rect.colliderect(player.sprite.horizontal_rect):
                if player.sprite.movement.x > 0:
                    player.sprite.rect.right = sprite.rect.left
                if player.sprite.movement.x < 0:
                    player.sprite.rect.left = sprite.rect.right
                player.sprite.movement.x = 0

    def handle_vertical_collision(sprite):
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

    def handle_tile_collisions():
        for sprite in tiles.sprites():
            handle_horizontal_collision(sprite)
            handle_vertical_collision(sprite)

    while running:
        for event in pygame.event.get():
            
            handle_keydown_event(event)
            handle_next_level_event(event)

        screen.fill('black')

        tiles.draw(screen)
        hazzards.draw(screen)
        goals.draw(screen)

        handle_tile_collisions()
                
        player.draw(screen)
        player.update()

        if pygame.sprite.spritecollide(player.sprite, hazzards, False):
            lose_scene()

        if pygame.sprite.spritecollide(player.sprite, goals, False):
            pygame.event.post(pygame.event.Event(NEXTLEVEL))

        pygame.display.flip()
        clock.tick(60)

def end_scene():
    running = True

    main_text = Text('THE END')
    scrolling_text = ScrollingText('YOU BEAT THE GAME!')
    enter_text = Text('PRESS ENTER TO TRY AGAIN')

    def handle_keydown_event(event):
        if not event.type == KEYDOWN:
            return
        if not event.key == K_RETURN:
            return
        if not scrolling_text.finished:
            scrolling_text.fill()
        else:
            running = False
            game_scene(0)
            return

    while running:
        for event in pygame.event.get():
            handle_quit_event(event)
            handle_keydown_event(event)

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
                 (Text("QUIT"), quit_game),]

    menu_scene(title_text, menu_list, 'red')

