import math

from pico2d import load_image, get_time, load_font, draw_rectangle, clamp
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_SPACE, SDLK_UP, SDLK_DOWN, SDLK_s

import game_framework
import game_world
import server
from ball import Ball
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def upkey_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP


def upkey_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_UP


def downkey_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN


def downkey_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def space_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_SPACE


def skey_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s


def skey_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_s


def time_out(e):
    return e[0] == 'TIME_OUT'


PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6


class Idle:

    @staticmethod
    def enter(character, e):
        character.action = 23
        character.speed = 0
        character.dir = 0

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        pass


class RunRight:
    @staticmethod
    def enter(character, e):
        character.action = 23 + 3
        character.speed = RUN_SPEED_PPS
        character.dir = 0

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        pass


class RunRightUp:
    @staticmethod
    def enter(character, e):
        character.action = 23 + 4
        character.speed = RUN_SPEED_PPS
        character.dir = math.pi / 4.0

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        pass


class RunRightDown:
    @staticmethod
    def enter(character, e):
        character.action = 23 + 2
        character.speed = RUN_SPEED_PPS
        character.dir = - math.pi / 4.0

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        pass


class RunLeft:
    @staticmethod
    def enter(character, e):
        character.action = 23 + 7
        character.speed = RUN_SPEED_PPS
        character.dir = math.pi

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        pass


class RunLeftUp:
    @staticmethod
    def enter(character, e):
        character.action = 23 + 6
        character.speed = RUN_SPEED_PPS
        character.dir = math.pi * 3.0 / 4.0

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        pass


class RunLeftDown:
    @staticmethod
    def enter(character, e):
        character.action = 23 + 8
        character.speed = RUN_SPEED_PPS
        character.dir = - math.pi * 3.0 / 4.0

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        pass


class RunUp:
    @staticmethod
    def enter(character, e):
        character.action = 23 + 5
        character.speed = RUN_SPEED_PPS
        character.dir = math.pi / 2.0

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        pass


class RunDown:
    @staticmethod
    def enter(character, e):
        character.action = 23 + 9
        character.speed = RUN_SPEED_PPS
        character.dir = - math.pi / 2.0

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        pass


class SwingFront:

    @staticmethod
    def enter(character, e):
        character.action = 23 - 6
        character.speed = 0
        character.dir = 0
        character.swing_time = get_time()

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        if get_time() - character.swing_time > 0.5:
            character.state_machine.handle_event(('TIME_OUT', 0))
        pass


class SwingLeft:

    @staticmethod
    def enter(character, e):
        character.action = 23 - 4
        character.speed = 0
        character.dir = 0
        character.swing_time = get_time()

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        if get_time() - character.swing_time > 0.5:
            character.state_machine.handle_event(('TIME_OUT', 0))
        pass


class SwingRight:

    @staticmethod
    def enter(character, e):
        character.action = 23 - 2
        character.speed = 0
        character.dir = 0
        character.swing_time = get_time()

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        if get_time() - character.swing_time > 0.5:
            character.state_machine.handle_event(('TIME_OUT', 0))
        pass


class Serve:

    @staticmethod
    def enter(character, e):
        if skey_down(e):
            character.swing_ball()
        character.action = 23 - 8
        character.speed = 0
        character.dir = 0
        character.swing_time = get_time()

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        if get_time() - character.swing_time > 0.5:
            character.state_machine.handle_event(('TIME_OUT', 0))
        pass


class StateMachine:

    def __init__(self, character):
        self.character = character
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: RunRight, left_down: RunLeft, left_up: Idle, right_up: Idle, upkey_down: RunUp,
                   downkey_down: RunDown, upkey_up: Idle, downkey_up: Idle, space_down: SwingFront, skey_down: Serve},
            RunRight: {right_up: Idle, left_down: Idle, upkey_down: RunRightUp, upkey_up: RunRightDown,
                       downkey_down: RunRightDown, downkey_up: RunRightUp, space_down: SwingRight},
            RunRightUp: {upkey_up: RunRight, right_up: RunUp, left_down: RunUp, downkey_down: RunRight,
                         space_down: SwingRight},
            RunUp: {upkey_up: Idle, left_down: RunLeftUp, downkey_down: Idle, right_down: RunRightUp,
                    left_up: RunRightUp, right_up: RunLeftUp, space_down: SwingFront},
            RunLeftUp: {right_down: RunUp, downkey_down: RunLeft, left_up: RunUp, upkey_up: RunLeft,
                        space_down: SwingLeft},
            RunLeft: {left_up: Idle, upkey_down: RunLeftUp, right_down: Idle, downkey_down: RunLeftDown,
                      upkey_up: RunLeftDown, downkey_up: RunLeftUp, space_down: SwingLeft},
            RunLeftDown: {left_up: RunDown, downkey_up: RunLeft, upkey_down: RunLeft, right_down: RunDown,
                          space_down: SwingLeft},
            RunDown: {downkey_up: Idle, left_down: RunLeftDown, upkey_down: Idle, right_down: RunRightDown,
                      left_up: RunRightDown, right_up: RunLeftDown, space_down: SwingFront},
            RunRightDown: {right_up: RunDown, downkey_up: RunRight, left_down: RunDown, upkey_down: RunRight,
                           space_down: SwingRight},
            SwingFront: {time_out: Idle, right_down: RunRight, left_down: RunLeft, upkey_down: RunUp, downkey_down: RunDown},
            SwingLeft: {time_out: Idle, right_down: RunRight, left_down: RunLeft, upkey_down: RunUp, downkey_down: RunDown},
            SwingRight: {time_out: Idle, right_down: RunRight, left_down: RunLeft, upkey_down: RunUp, downkey_down: RunDown},
            Serve: {time_out: Idle, right_down: RunRight, left_down: RunLeft, upkey_down: RunUp, downkey_down: RunDown, space_down: SwingFront}
        }


    def start(self):
        self.cur_state.enter(self.character, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.character)
        self.character.frame = (self.character.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        self.character.x += math.cos(self.character.dir) * self.character.speed * game_framework.frame_time
        self.character.y += math.sin(self.character.dir) * self.character.speed * game_framework.frame_time

    def handle_event(self, e):
        for check_evnet, next_state in self.transitions[self.cur_state].items():
            if check_evnet(e):
                self.cur_state.exit(self.character, e)
                self.cur_state = next_state
                self.cur_state.enter(self.character, e)
                return True

        return False


class Character:

    def __init__(self):
        self.frame = 0
        self.action = 0
        # self.face_dir = 2
        self.dir = 0
        self.image = load_image('mario1234.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.ball_count = 1
        self.font = load_font('ENCR10B.TTF', 16)
        self.x, self.y = 630, 270
        # self.x, self.y = server.background.w // 2, server.background.h // 2

    def swing_ball(self, x=500, y=600):
        if self.ball_count > 0:
            self.ball_count -= 1
            ball = Ball(self.x, self.y)
            game_world.add_object(ball)
            game_world.add_collision_pair('character:ball', None, ball)

    def swing_front(self):
        pass

    def update(self):
        self.state_machine.update()
        # self.x = clamp(30, self.x, 990)
        self.x = clamp(30, self.x, server.background.w - 50)
        # self.y = clamp(250, self.y, 850)
        self.y = clamp(250, self.y, server.background.h - 50)

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        # self.state_machine.draw()
        # draw_rectangle(*self.get_bb())
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        self.image.clip_draw(int(self.frame) * 88, self.action * 88, 88, 88, sx, sy, 88 * 3, 88 * 3)
        x1, y1, x2, y2 = self.get_bb()
        draw_rectangle(x1-server.background.window_left,y1-server.background.window_bottom,
                       x2-server.background.window_left,y2-server.background.window_bottom)
        self.font.draw(sx - 60, sy + 50, f'({int(self.x)}, {int(self.y)})', (255, 255, 0))

    def get_bb(self):
        return self.x - 25, self.y - 70, self.x + 25, self.y + 15

    def handle_collision(self, group, other):
        if group == 'character:ball':
            # self.ball_count += 1
            pass


