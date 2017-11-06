from pygame import *


class Wall(sprite.Sprite):
    def __init__(self, x, y, game):
        super().__init__()
        self.game = game
        self.image = Surface((self.game.block_size, self.game.block_size))
        self.image.fill(Color('green'))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
