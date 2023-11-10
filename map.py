from pico2d import *

class Map:
    def __init__(self):
        self.image = load_image('court1.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(258 * 2, 242 * 2, self.image.w * 4, self.image.h * 4)