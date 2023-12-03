import time

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

PIXEL_PER_METER2 = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH2 = 20.0  # Km / Hour
RUN_SPEED_MPM2 = (RUN_SPEED_KMPH2 * 1000.0 / 60.0)
RUN_SPEED_MPS2 = (RUN_SPEED_MPM2 / 60.0)
RUN_SPEED_PPS2 = (RUN_SPEED_MPS2 * PIXEL_PER_METER2)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8.0


class Ball:
    image = None

    def __init__(self, x=0, y=0):
        if Ball.image == None:
            Ball.image = load_image('tennis_ball2.png')
        self.x, self.y = x, y
        self.dir = 0.0 # radian 값으로 방향을 표시
        self.action = 0
        self.speed = 0.0
        self.frame = 0
        self.state = 'Idle'
        self.start_time = time.time()

        self.tx, self.ty = 0, 0
        self.build_behavior_tree()

    def get_bb(self):
        return self.x - 15, self.y - 15, self.x + 14, self.y + 14
    # sx - 15, sy - 15, sx + 14, sy + 14

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        # self.bt2.run()

    def draw(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        self.image.clip_draw(int(self.frame) * 32, self.action * 32, 32, 32, sx, sy)
        x1, y1, x2, y2 = self.get_bb()
        draw_rectangle(x1-server.background.window_left,y1-server.background.window_bottom,
                       x2-server.background.window_left,y2-server.background.window_bottom)

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if group == 'character:ball':
            # game_world.remove_object(self)
            # self.bt2.run()
            pass

    def set_front_location(self):
        # self.tx = random.randint(int(server.character.x - 20), int(server.character.x + 20))
        # self.ty = random.randint(int(server.character.y + 1000), int(server.character.y + 1200))
        self.tx = 600
        self.ty = 600
        return BehaviorTree.SUCCESS

    def move_slightly_to(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        self.speed = RUN_SPEED_PPS
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time

    def move_to(self, r=0.5):
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def set_random_location(self):
        self.speed = RUN_SPEED_PPS
        # select random location around boy
        self.tx = random.randint(225, 800)
        self.ty = random.randint(560, 750)
        return BehaviorTree.SUCCESS

    def character_swing_front_action(self):
        if server.character.action == 23 - 6:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def character_swing_left_action(self):
        if server.character.action == 23 - 4:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def character_swing_right_action(self):
        if server.character.action == 23 - 2:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL



    def character_serve_action(self):
        landing_time = time.time() - self.start_time
        if server.character.swing_ball and landing_time <= 1.2:
            return BehaviorTree.SUCCESS
        else:
            # game_world.remove_object(self)
            return BehaviorTree.FAIL

    def set_target_location(self, x=None, y=None):
        if not x or not y:
            raise ValueError('Location should be given')
        self.tx, self.ty = x, y
        return BehaviorTree.SUCCESS

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def move_up_to(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        self.speed = RUN_SPEED_PPS2
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time

    def serve_move(self, r=0.5):
        self.move_up_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        # a1 = Action('Set random location', self.set_random_location)
        # a2 = Action('Move to', self.move_to)
        # root = SEQ_wander = Sequence('Wander', a1, a2)
        c1 = Condition('character serve action', self.character_serve_action)
        a1 = Action('set target location', self.set_target_location, server.character.x, server.character.y + 100)
        a2 = Action('serve move', self.serve_move)
        a3 = Action('set target location2', self.set_target_location, server.character.x, server.character.y - 70)
        a4 = Action('serve move2', self.serve_move)
        root1 = SEQ_serve = Sequence('serve', c1, a1, a2, a3, a4)

        c2 = Condition('character swing up action', self.character_swing_front_action)
        a5 = Action('set target location3', self.set_target_location, 500, 600)
        a6 = Action('swing move3', self.move_to)
        SEQ_swing_front = Sequence('swing front', c2, a5, a6)

        c3 = Condition('character swing left action', self.character_swing_left_action)
        a7 = Action('set target location4', self.set_target_location, 500, 600)
        a8 = Action('swing move4', self.move_to)
        SEQ_swing_left = Sequence('swing left', c3, a7, a8)

        c4 = Condition('character swing right action', self.character_swing_right_action)
        a9 = Action('set target location5', self.set_target_location, 500, 600)
        a10 = Action('swing move5', self.move_to)
        SEQ_swing_right = Sequence('swing right', c4, a9, a10)

        root2 = SEL_swing = Selector('swing', SEQ_swing_front, SEQ_swing_left, SEQ_swing_right)

        # c3 = Condition('character swing left action', self.character_swing_left_action)
        # c4 = Condition('character swing right action', self.character_swing_right_action)
        # a2 = Action('set front loaction', self.set_front_location)
        # a3 = Action('move to', self.move_to)
        # root = SEQ_front_move = Sequence('front move', c2, a2, a3)
        # SEQ_left_move = Sequence('left move', c3, a2)
        # SEQ_right_move = Sequence('right move', c4, a2)
        #
        # SEL_swing_move = Selector('up or left or right', SEQ_front_move, SEQ_left_move, SEQ_right_move)
        #
        # SEL_serve_or_swing = Selector('serve or swing', SEQ_serve_move, SEL_swing_move)

        self.bt1 = BehaviorTree(root1)
        self.bt2 = BehaviorTree(root2)
