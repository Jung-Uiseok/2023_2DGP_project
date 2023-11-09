from pico2d import *

open_canvas(258 * 4, 242 * 4)

image = load_image('court1.png')
# character = load_image('baby-mario.gif')
character = load_image('mario1.png')


running = True


def handle_event():
    global running

    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and SDLK_ESCAPE:
            running = False


frame = 0

for x in range(0, 258 * 4, 5):
    clear_canvas()
    image.draw_now(258 * 2, 242 * 2, image.w * 4, image.h * 4)
    character.clip_draw(frame * 88, 0, 88, 88, x, 190, 88, 88)
    update_canvas()

    handle_event()
    if not running:
        break

    frame = (frame + 1) % 2
    delay(0.05)
close_canvas()
