from pico2d import load_image


class Pannel:

    def __init__(self):
        self.image = load_image('menu_select.png')

    def draw(self):
        self.image.draw(400, 400)

    def update(self):
        pass
