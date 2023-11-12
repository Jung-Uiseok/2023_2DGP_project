from pico2d import *

import game_world
import play_mode
import title_mode

import game_framework
from pannel import Pannel


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.pop_mode()
        elif event.type == SDL_KEYDOWN:
            match event.key:
                case pico2d.SDLK_0:
                    pass
                case pico2d.SDLK_1:
                    pass
                case pico2d.SDLK_2:
                    pass


def init():
    global pannel

    pannel = Pannel()
    game_world.add_object(pannel, 3)


def update():
    game_world.update()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.remove_object(pannel)


def pause():
    pass


def resume():
    pass
