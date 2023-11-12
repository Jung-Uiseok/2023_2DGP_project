from pico2d import *
import game_framework

import game_world
import item_mode
import title_mode
from ball import Ball
from map import Map
from character import Character


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_i:
            game_framework.push_mode(item_mode)
        else:
            character.handle_event(event)


def init():
    global map
    global ball
    global character

    running = True

    map = Map()
    game_world.add_object(map, 0)
    character = Character()
    game_world.add_object(character, 1)

    # ball = Ball()
    # game_world.add_object(ball, 1)

    game_world.add_collision_pair('character:ball', character, None)
    # game_world.add_collision_pair('character:ball', None, ball)


def finish():
    game_world.clear()


def update():
    game_world.update()
    game_world.handle_collisions()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def pause():
    pass


def resume():
    pass
