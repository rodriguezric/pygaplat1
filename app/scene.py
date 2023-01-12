import pygame
import sys

from pygame.sprite import Sprite
from pygame.locals import *

from framework.screen import screen, WIDTH, HEIGHT, tile_size
from framework.text import Text, ScrollingText, center_text, draw_text

# Event for determining which level to load
NEXTLEVEL = pygame.USEREVENT + 1

# Event for setting running=False
STOPRUNNING = pygame.USEREVENT + 2

from os import walk
_, __, level_files = list(walk('levels'))[0]
level_files = [f'levels/{x}' for x in sorted(level_files)]

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
    '''
    Returns a new cursor value based on KEYDOWN event and the
    length of the menu_list. When the user presses return, it
    calls the function in menu_list at the cursor index. when
    the users presses up or down, it increases or decreases
    the cursor value.
    '''
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
            if event.type == STOPRUNNING:
                running = False

            cursor = handle_cursor_event(event, cursor, menu_list)
            handle_quit_event(event)
        
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
    from app.enemy import Enemy
    from app.projectile import Projectile

    # Player sprites
    player = pygame.sprite.GroupSingle()
    player.add(Player((50,50)))
    player_projectiles = pygame.sprite.Group()

    # Enemy sprites
    enemies = pygame.sprite.Group()

    # Tile sprites
    from app.tile import Tile, DialogTile, MovingTile, create_colored_tile
    tiles = pygame.sprite.Group()
    hazzards = pygame.sprite.Group()
    goals = pygame.sprite.Group()
    dialogs = pygame.sprite.Group()
    collided_dialogs = []

    import csv
    with open(level_files[level_idx]) as f:
        level = ((x, y, v) for y, _ in enumerate(tuple(csv.reader(f))) 
                           for x, v in enumerate(_))

    tile_dict = {'1': create_colored_tile('white'),}
    hazzard_dict = {'2': create_colored_tile('firebrick'),}
    goal_dict = {'D': create_colored_tile('blue'),}

    for x, y, key in level:
        pos = (tile_size * x, tile_size * y)
        
        tile_fn = tile_dict.get(key)
        if tile_fn:
            tiles.add(tile_fn(pos=pos))
        
        hazzard_fn = hazzard_dict.get(key)
        if hazzard_fn:
            hazzards.add(hazzard_fn(pos=pos))
         
        goal_fn = goal_dict.get(key)
        if goal_fn:
            goals.add(goal_fn(pos=pos))
        
        if key.startswith('E'):
            _, text_id = key.split(':')
            dialogs.add(DialogTile(text_id=text_id,
                                   color='yellow', 
                                   pos=pos,))

        if key == 'M':
            enemies.add(Enemy(pos=pos))
    
    running = True

    def handle_keydown_event(event):
        if not event.type == KEYDOWN:
            return
        if event.key == K_ESCAPE:
            pause_scene()
        if event.key == K_LSHIFT:
            player_projectiles.add(Projectile(pos=player.sprite.weapon_pos, 
                                              direction=player.sprite.direction))
        if event.key == K_RETURN:
            if collided_dialogs:
                with open(f'texts/{collided_dialogs[0].text_id}.txt') as f:
                    lines = [line.strip() for line in f.readlines()]
                    show_dialogue(lines)
    
    def handle_next_level_event(event):
        if not event.type == NEXTLEVEL:
            return
        if level_idx >= len(level_files)-1:
            # we beat the game
            end_scene() 
        else:
            # next level
            game_scene(level_idx+1)

    def handle_horizontal_collision(source: Sprite, target: Sprite):
        if source.movement.x == 0:
            return
        if not target.rect.colliderect(source.horizontal_rect):
            return 
        if source.movement.x > 0:
            source.rect.right = target.rect.left
        if source.movement.x < 0:
            source.rect.left = target.rect.right
        source.movement.x = 0

    def handle_vertical_collision(source: Sprite, target: Sprite):
        if source.movement.y == 0:
            return
        if not target.rect.colliderect(source.vertical_rect):
            return
        if source.movement.y > 0:
            source.rect.bottom = target.rect.top
        else:
            source.rect.top = target.rect.bottom
        source.movement.y = 0

    def handle_drawing():
        tiles.draw(screen)
        hazzards.draw(screen)
        goals.draw(screen)
        dialogs.draw(screen)

    def handle_tile_collisions():
        for tile_sprite in tiles.sprites():
            handle_horizontal_collision(source=player.sprite, target=tile_sprite)
            handle_vertical_collision(source=player.sprite, target=tile_sprite)

            for enemy_sprite in enemies.sprites():
                handle_horizontal_collision(source=enemy_sprite, target=tile_sprite)
                handle_vertical_collision(source=enemy_sprite, target=tile_sprite)

    time_past = Text('')
    while running:
        for event in pygame.event.get():
            handle_next_level_event(event)
            handle_keydown_event(event)
            handle_quit_event(event)

        screen.fill('black')

        handle_drawing()
        handle_tile_collisions()

        tiles.update()
                
        player.draw(screen)
        player.update()
        player_projectiles.draw(screen)
        player_projectiles.update()

        enemies.draw(screen)
        enemies.update()

        if pygame.sprite.spritecollide(player.sprite, hazzards, False):
            lose_scene()

        if pygame.sprite.spritecollide(player.sprite, enemies, False):
            lose_scene()

        if pygame.sprite.spritecollide(player.sprite, goals, False):
            pygame.event.post(pygame.event.Event(NEXTLEVEL))

        collided_dialogs = pygame.sprite.spritecollide(player.sprite, dialogs, False)

        projectile_collisions = pygame.sprite.groupcollide(
            player_projectiles, 
            enemies, 
            False, 
            False,
        )

        for projectile in projectile_collisions.keys():
            projectile.kill()

        for collided_enemies in projectile_collisions.values():
            for enemy in collided_enemies:
                enemy.kill()

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
            handle_keydown_event(event)
            handle_quit_event(event)

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

def chunk(L: list, size: int):
    return [L[i:i+size] for i in range(0, len(L), size)]
    
def show_dialogue(lines: list):
    from framework.font import font_16
    scrolling_dialog = chunk([ScrollingText(x, font=font_16) for x in lines], 6)
    chunk_idx = 0 
    text_idx = 0 
    surf = pygame.Surface((WIDTH, tile_size*4))
    rect = surf.get_rect(midbottom=screen.get_rect().midbottom)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == K_RETURN:
                if not scrolling_dialog[chunk_idx][-1].finished:
                    for x in scrolling_dialog[chunk_idx]: 
                        x.fill() 
                else:
                    chunk_idx += 1
                    text_idx = 0

        surf.fill('black')
        screen.blit(surf, rect)

        if chunk_idx == len(scrolling_dialog):
            break

        if not scrolling_dialog[chunk_idx][text_idx].finished:
            scrolling_dialog[chunk_idx][text_idx].inc()
        else:
            if text_idx < len(scrolling_dialog[chunk_idx]) - 1:
                text_idx += 1

        for idx, scrolling_text in enumerate(scrolling_dialog[chunk_idx]):
            draw_text(scrolling_text, x=8, y=8 + idx * (16+4) + rect.top)


        pygame.display.update()
        clock.tick(5)

def level_editor_scene(level_idx=0):
    from app.enemy import Enemy

    # Enemy sprites
    enemies = pygame.sprite.Group()

    # Tile sprites
    from app.tile import Tile, DialogTile, MovingTile, create_colored_tile
    tiles = pygame.sprite.Group()
    hazzards = pygame.sprite.Group()
    goals = pygame.sprite.Group()
    dialogs = pygame.sprite.Group()

    sprite_groups = [tiles, hazzards, goals, dialogs, enemies]

    import csv
    with open(level_files[level_idx]) as f:
        level_dict = {(x, y): v for y, _ in enumerate(tuple(csv.reader(f))) 
                           for x, v in enumerate(_)}

    tile_dict = {'1': create_colored_tile('white'),}
    hazzard_dict = {'2': create_colored_tile('firebrick'),}
    goal_dict = {'D': create_colored_tile('blue'),}

    def read_level_file(level_idx: int) -> dict:
        import csv

        with open(level_files[level_idx]) as f:
            level_dict = {(x, y): v for y, _ in enumerate(tuple(csv.reader(f))) 
                               for x, v in enumerate(_)}

        return level_dict

    def save_level_file(level_idx: int, level_dict: dict):
        import csv

        L = [['0'] * 16 for _ in range(12)] 
        for (x, y) , v in level_dict.items():
            L[y][x] = v

        with open(level_files[level_idx], 'w') as f:
            level_writer = csv.writer(f)
            for row in L:
                level_writer.writerow(row)

    def update_level(level_dict):
        for sprite_group in sprite_groups:
            sprite_group.empty() 

        for (x, y), key in level_dict.items():
            pos = (tile_size * x, tile_size * y)
            
            tile_fn = tile_dict.get(key)
            if tile_fn:
                tiles.add(tile_fn(pos=pos))
            
            hazzard_fn = hazzard_dict.get(key)
            if hazzard_fn:
                hazzards.add(hazzard_fn(pos=pos))
             
            goal_fn = goal_dict.get(key)
            if goal_fn: goals.add(goal_fn(pos=pos))
            
            if key.startswith('E'):
                _, text_id = key.split(':')
                dialogs.add(DialogTile(text_id=text_id,
                                       color='yellow', 
                                       pos=pos,))

            if key == 'M':
                enemies.add(Enemy(pos=pos))

    level_dict = read_level_file(level_idx)
    update_level(level_dict)


    tile_value_text = Text('TILE: ')
    tile_value = '1'
    tile_keys = [pygame.K_1,
                 pygame.K_2,
                 pygame.K_3,
                 pygame.K_4,
                 pygame.K_5]
    tile_lookup_dict = dict(zip(tile_keys, list("12DM") + ["E:0"]))

    def paint_tile(pos, tile_value):
        x, y = pos
        i = x // tile_size
        j = y // tile_size
        
        # if in editable area
        if 1 < i < 15 and 1 < j < 11:
            level_dict[(i, j)] = tile_value
            update_level(level_dict)

    running = True
    while running:
        for event in pygame.event.get():
            handle_quit_event(event)

            if not event.type == KEYDOWN:
                continue

            if event.key in tile_keys:
                tile_value = tile_lookup_dict.get(event.key)

            if event.key == pygame.K_s:
                save_level_file(level_idx=level_idx, 
                                level_dict=level_dict)

        screen.fill('black')

        tiles.draw(screen)
        enemies.draw(screen)
        hazzards.draw(screen)
        goals.draw(screen)
        dialogs.draw(screen)

        # right click
        if pygame.mouse.get_pressed() == (0, 0, 1):
            paint_tile(pos=pygame.mouse.get_pos(), 
                        tile_value='0')

        if pygame.mouse.get_pressed() == (1, 0, 0):
            paint_tile(pos=pygame.mouse.get_pos(), 
                        tile_value=tile_value)

        draw_text(tile_value_text, 
                  x=tile_size, 
                  y=tile_size * 13)

        pygame.display.update()
        clock.tick(60)
