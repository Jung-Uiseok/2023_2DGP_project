from pico2d import *

class Map:
    def __init__(self):
        self.image = load_image('courts.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(397, 644)