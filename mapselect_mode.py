from pico2d import load_image, get_events, clear_canvas, update_canvas, pico2d
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE

import game_framework
import play_mode
import title_mode


def init():
    global mapselectimage

    mapselectimage = load_image('mapselect1.png')

def finish():
    # global image
    # del image
    pass


def update():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        elif event.type == SDL_KEYDOWN:
            match event.key:
                case pico2d.SDLK_1:
                    game_framework.pop_mode()
                    game_framework.change_mode(play_mode)
                    pass
                case pico2d.SDLK_2:
                    pass
                case pico2d.SDLK_2:
                    pass
                case pico2d.SDLK_4:
                    pass


def draw():
    clear_canvas()
    mapselectimage.draw(258 * 2, 242 * 2, mapselectimage.w * 4, mapselectimage.h * 4)
    update_canvas()


def pause():
    pass


def resume():
    pass
