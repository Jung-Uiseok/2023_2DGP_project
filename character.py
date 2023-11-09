from pico2d import load_image, get_time, load_font
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_SPACE

import game_framework


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def time_out(e):
    return e[0] == 'TIME_OUT'


PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6


class Idle:

    @staticmethod
    def enter(character, e):
        if character.face_dir == -1:
            character.action = 1
        elif character.face_dir == 1:
            character.action = 0
        character.dir = 0
        character.frame = 0
        character.wait_time = get_time()

    @staticmethod
    def exit(character, e):
        if space_down(e):
            character.swing()

    @staticmethod
    def do(character):
        character.frame = (character.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        if get_time() - character.wait_time > 2:
            character.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(character):
        character.image.clip_draw(int(character.frame) * 88, character.action * 88, 88, 88, character.x, character.y)


class Run:

    @staticmethod
    def enter(character, e):
        if right_down(e) or left_up(e):  # 오른쪽으로 RUN
            character.action = 3
        elif left_down(e) or right_up(e):  # 왼쪽으로 RUN
            character.action = 7

    @staticmethod
    def exit(character, e):
        if space_down(e):
            character.swing()

    @staticmethod
    def do(character):
        character.frame = (character.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        character.x += RUN_SPEED_PPS * game_framework.frame_time

    @staticmethod
    def draw(character):
        character.image.clip_draw(int(character.frame) * 88, character.action * 88, 88, 88, character.x, character.y)


class StateMachine:
    def __init__(self, character):
        self.character = character
        self.cur_state = Idle
        self.transitions = {}

    def start(self):
        self.cur_state.enter(self.character, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.character)

    def handle_event(self, e):
        for check_evnet, next_state in self.transitions[self.cur_state].items():
            if check_evnet(e):
                self.cur_state.exit(self.character, e)
                self.cur_state = next_state
                self.cur_state.enter(self.character, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.character)


class Character:
    def __init__(self):
        self.x, self.y = 500, 500
        self.frame = 0
        self.action = 3
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('mario1.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.item = 'Ball'
        self.font = load_font('ENCR10B.TTF', 16)

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x - 60, self.y + 50, f'(Time:{get_time():.2f})', (255, 255, 0))
