from pico2d import *

class Map:
    def __init__(self):
        self.image = load_image('court2.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(258 * 2, 242 * 2)