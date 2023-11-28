from pico2d import open_canvas, close_canvas
import game_framework

import title_mode as start_mode
# import play_mode as start_mode

# open_canvas(1032, 968)
open_canvas(800, 800)
game_framework.run(start_mode)
close_canvas()
