from pico2d import *
import game_world
import game_framework


class Ball:
    image = None

    def __init__(self, x = 400, y = 300, velocity = 1):
        if Ball.image == None:
            Ball.image = load_image('tennis_ball.png')
        self.x, self.y, self.velocity = x, y, velocity

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.y += self.velocity * 70 * game_framework.frame_time

        if self.x < 14 or self.x > 258 * 4 - 13:
            game_world.remove_object(self)
        if self.y < 13 or self.y > 242 * 7 - 13:
            game_world.remove_object(self)

    def get_bb(self):
        return self.x - 14, self.y - 13, self.x + 13, self.y + 13

    def handle_collision(self, group, other):
        if group == 'character:ball':
            pass