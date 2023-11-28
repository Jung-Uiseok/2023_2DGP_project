from pico2d import *

import random
import math
import game_framework
import game_world
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
import play_mode

import server

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 60.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8.0


class Ball:
    image = None

    def __init__(self, x=0, y=0, size=1.0):
        if Ball.image == None:
            Ball.image = load_image('tennis_ball2.png')
        self.x, self.y, self.size = x, y, size
        self.dir = 0.0 # radian 값으로 방향을 표시
        self.action = 0
        self.speed = 0.0
        self.frame = 0
        self.state = 'Idle'

        self.tx, self.ty = 0, 0
        self.build_behavior_tree()

    # def __getstate__(self):
    #     state = {'name': self.name, 'x': self.x, 'y': self.y, 'size': self.size}
    #     return state
    #
    # def __setstate__(self, state):
    #     self.__init__()
    #     self.__dict__.update(state)

    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.bt.run()

    def draw(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        self.image.clip_draw(int(self.frame) * 32, self.action * 32, 32, 32, sx, sy)
        draw_rectangle(sx - 15, sy - 15, sx + 14, sy + 14)

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if group == 'character:ball':
            # game_world.remove_object(self)
            pass


    def set_target_location(self, x=None, y=None):
        if not x or not y:
            raise ValueError('Location should be given')
        self.tx, self.ty = x, y
        return BehaviorTree.SUCCESS

    def distance_less_than(self, x1, y1, x2, y2, r):
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
        self.speed = RUN_SPEED_PPS
        # select random location around boy
        self.tx = random.randint(110, 900)
        self.ty = random.randint(500, 750)
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        a1 = Action('Set random location', self.set_random_location)
        a2 = Action('Move to', self.move_to)
        root = SEQ_wander = Sequence('Wander', a1, a2)
        self.bt = BehaviorTree(root)
