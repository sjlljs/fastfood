from pygame import *
import pyganim


class Dizzy(sprite.Sprite):
    directions = {'up': {'x': 0, 'y': -1}, "down": {'x': 0, 'y': 1}, 'left': {'x': -1, 'y': 0},
                  'right': {'x': 1, 'y': 0}}
    __direction = None
    __step_count = 0
    color = Color('red')
    anim = {}
    sprite = {}

    def __init__(self, x, y, game, shape):
        super().__init__()
        self.anim = {}
        self.game = game
        self.set_image(shape)
        self.set_rect(x, y)
        # self.image = Surface((self.game.block_size - 1, self.game.block_size - 1))
        # self.image.fill(self.color)
        # draw.circle(self.image, Color('yellow'), (int(self.game.block_size / 2), int(self.game.block_size / 2)), int(self.game.block_size / 2), 0)

        self.set_normal_speed()

    def set_image(self, shape):
        self.shape = shape
        self.image = self.sprite[self.shape]['stand']

    def set_rect(self, x, y):
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def set_normal_speed(self):
        self.steps = 7
        self.step_val = self.game.block_size // self.steps

    def set_direction(self, dir):
        if self.__step_count > 0:
            return False
        delta = self.directions.get(dir, None)
        if delta is None:
            return False
        self.__direction = dir
        self.__step_count = self.steps

    def update(self):
        if self.__step_count == 0 or self.__direction is None:
            return False
        delta = self.directions.get(self.__direction, None)
        if delta is None:
            self.__direction = None
            self.__step_count = 0
            return False
        if self.__step_count > 1:
            self.rect.move_ip(delta['x'] * self.step_val, delta['y'] * self.step_val)
            self.__step_count -= 1
        elif self.__step_count == 1:
            last_step = self.game.block_size - self.step_val * (self.steps - 1)
            self.rect.move_ip(delta['x'] * last_step, delta['y'] * last_step)
            self.__step_count = 0
        else:
            self.__direction = None
            self.__step_count = 0
        self.image = self.sprite[self.shape][self.__direction][self.__step_count % len(self.sprite[self.shape][
                                                                                           self.__direction])]  # self.anim[self.__direction].getFrame(self.__step_count % len(self.anim[self.__direction]._images))
        return self.__step_count
