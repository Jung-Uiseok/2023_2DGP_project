from pico2d import load_image, get_events, clear_canvas, update_canvas, pico2d, get_canvas_width
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE

import game_framework
import play_mode
import title_mode


def init():
    global mapselectimage
    global selectimage
    global level1_color
    global level2_color
    global level3_color
    global level4_color

    mapselectimage = load_image('map_select.png')
    selectimage = load_image('select.png')
    level1_color = load_image('level1_color.png')
    level2_color = load_image('level2_color.png')
    level3_color = load_image('level3_color.png')
    level4_color = load_image('level4_color.png')

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
                case pico2d.SDLK_SPACE:
                    game_framework.pop_mode()
                    game_framework.change_mode(play_mode)
                    pass
                case pico2d.SDLK_RIGHT:
                    pass


def draw():
    clear_canvas()
    mapselectimage.draw(400, 400)
    selectimage.draw(100, 440)
    level1_color.draw(100, 440)
    level2_color.draw(300, 440)
    level3_color.draw(500, 440)
    level4_color.draw(700, 440)
    update_canvas()


def pause():
    pass


def resume():
    pass
