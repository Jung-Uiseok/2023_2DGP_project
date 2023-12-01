from pico2d import *
import game_framework

import game_world
import item_mode
import server
import title_mode
from ball import Ball
from map import Map
from character import Character

from background3 import FixedBackground as Background3


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.push_mode(item_mode)
        else:
            server.character.handle_event(event)


def init():

    server.background3 = Background3()
    game_world.add_object(server.background3, 0)

    server.character = Character()
    game_world.add_object(server.character, 1)
    game_world.add_collision_pair('character:ball', server.character, None)


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
