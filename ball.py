import random

from pico2d import *
import game_world
import game_framework
import server
from behavior_tree import BehaviorTree

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class Ball:
    image = None

    def __init__(self, x=0, y=0, velocity=1):
        if Ball.image == None:
            Ball.image = load_image('tennis_ball2.png')
        # self.x, self.y, self.velocity = x, y, velocity
        self.x = x if x else random.randint(14, 258 * 4 - 13)
        self.y = y if y else random.randint(13, 242 * 4 - 13)
        self.velocity = velocity
        self.frame = 0
        self.action = 0
        self.tx, self.ty = 0, 0
        self.build_behavior_tree()

    def draw(self):
        # self.image.draw(self.x, self.y)
        # draw_rectangle(*self.get_bb())
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        self.image.clip_draw(int(self.frame) * 8, self.action * 32, 32, 32, sx, sy)
        draw_rectangle(sx - 15, sy - 15, sx + 14, sy + 14)

    def update(self):
        # self.y += self.velocity * 70 * game_framework.frame_time
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.bt.run()
        if self.x < 15 or self.x > 258 * 4 - 14:
            game_world.remove_object(self)
        if self.y < 15 or self.y > 242 * 7 - 14:
            game_world.remove_object(self)

    def get_bb(self):
        return self.x - 15, self.y - 15, self.x + 14, self.y + 14

    def handle_collision(self, group, other):
        if group == 'character:ball':
            pass

    def set_target_location(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def move_slightly_to(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        self.speed = RUN_SPEED_PPS
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time

    def move_to(self, r=0.5):
        self.state = 'Walk'
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def set_random_location(self):
        # select random location around boy
        self.tx = random.randint(int(server.character.x) - 600, int(server.character.x) + 600)
        self.ty = random.randint(int(server.character.y) - 400, int(server.character.y) + 400)
        return BehaviorTree.SUCCESS