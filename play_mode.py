from pico2d import *
import game_framework

import game_world
import item_mode
import server
import title_mode
from ball import Ball
from map import Map
from character import Character

from background import FixedBackground as Background


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
    # global map
    # global ball
    # global character
    #
    # running = True
    #
    # map = Map()
    # game_world.add_object(map, 0)
    # character = Character()
    # game_world.add_object(character, 1)
    #
    # game_world.add_collision_pair('character:ball', character, None)

    server.background = Background()
    game_world.add_object(server.background, 0)

    server.character = Character()
    game_world.add_object(server.character, 1)
    game_world.add_collision_pair('character:ball', server.character, None)

    # server.ball = Ball()
    # game_world.add_object(server.ball, 1)
    # game_world.add_collision_pair('character:ball', None, server.ball)


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
