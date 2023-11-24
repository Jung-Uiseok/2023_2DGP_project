import random

from pico2d import *
import game_world
import game_framework
import server


PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6


class Ball:
    image = None

    def __init__(self, x=None, y=None, velocity=1):
        if Ball.image == None:
            Ball.image = load_image('tennis_ball2.png')
        # self.x, self.y, self.velocity = x, y, velocity
        self.x = x if x else random.randint(14, 258 * 4 - 13)
        self.y = y if y else random.randint(13, 242 * 4 - 13)
        self.velocity = velocity
        self.frame = 0
        self.action = 0

    def draw(self):
        # self.image.draw(self.x, self.y)
        # draw_rectangle(*self.get_bb())
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        self.image.clip_draw(int(self.frame) * 8, self.action * 32, 32, 32, sx, sy)
        draw_rectangle(sx - 15, sy - 15, sx + 14, sy + 14)

    def update(self):
        # self.y += self.velocity * 70 * game_framework.frame_time

        if self.x < 15 or self.x > 258 * 4 - 14:
            game_world.remove_object(self)
        if self.y < 15 or self.y > 242 * 7 - 14:
            game_world.remove_object(self)

    def get_bb(self):
        return self.x - 15, self.y - 15, self.x + 14, self.y + 14

    def handle_collision(self, group, other):
        if group == 'character:ball':
            pass
