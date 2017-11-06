from pygame import *


class Point(sprite.Sprite):
    size = 6

    def __init__(self, x, y):
        super().__init__()
        # self.x = x
        # self.y = y
        color = Color('yellow')
        self.image = Surface((self.size, self.size))
        draw.circle(self.image, color, (int(self.size / 2), int(self.size / 2)), int(self.size / 2), 0)

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)