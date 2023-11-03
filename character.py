from pico2d import load_image


class Character:
    def __init__(self):
        self.x, self.y = 500, 500
        self.frame = 0
        self.action = 3
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('baby-mario-3.png')
    pass