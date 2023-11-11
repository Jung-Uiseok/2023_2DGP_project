from pico2d import load_image, get_events, clear_canvas, update_canvas
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE

import game_framework
import play_mode


def init():
    global titleimage

    titleimage = load_image('title.png')


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
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(play_mode)


def draw():
    clear_canvas()
    titleimage.draw(258 * 2, 242 * 2, titleimage.w * 7, titleimage.h * 7)
    update_canvas()


def pause():
    pass


def resume():
    pass
