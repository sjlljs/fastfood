from pygame import sprite, Surface, Color
import pyganim
import random


class Food(sprite.Sprite):
    direction = None
    __step_count = 0
    active = False
    anim = {}
    conductor = None

    def __init__(self, x, y, game, shape=None):
        super().__init__()
        self.game = game
        if shape is None:
            all_shapes = list(self.anim.keys())
            n = random.randint(0, len(all_shapes) - 1)
            self.shape = all_shapes[n]
            self.image = self.anim[self.shape]._images[0]
            # self.image = Surface((self.game.block_size - 1, self.game.block_size - 1))
            # self.image.fill(Color('orange'))
        # draw.circle(self.image, Color('yellow'), (int(self.game.block_size / 2), int(self.game.block_size / 2)), int(self.game.block_size / 2), 0)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.set_normal_speed()

    def set_normal_speed(self):
        self.steps = 7
        self.step_val = self.game.block_size // self.steps

    def set_active(self):
        self.active = True

    def set_nonactive(self):
        self.active = False

    @property
    def step_status(self):
        if self.__step_count > 0:
            return True
        else:
            return False

    def set_direction(self, dir):
        if self.__step_count > 0:
            return False
        delta = self.game.directions.get(dir, None)
        if delta is None:
            return False
        self.direction = dir
        self.__step_count = self.steps

    @property
    def map_x(self):
        return (self.rect.centerx - self.game.location.startx) // self.game.block_size

    @property
    def map_y(self):
        return (self.rect.centery - self.game.location.starty) // self.game.block_size

    def update(self):
        if self.active is True:
            self.image = self.anim[self.shape].getCurrentFrame()
        if not self.active:
            return False
        if self.direction is None:
            directs = self.game.location.get_allowed_directions_on_map(self.map_x, self.map_y)
            select_direct = directs[random.randint(0, len(directs) - 1)]
            self.set_direction(select_direct)
        elif self.__step_count == 0:
            directs = self.game.location.get_allowed_directions_on_map(self.map_x, self.map_y)
            directs = self.game.location.isnt_any_player_on_direction(x=self.map_x, y=self.map_y, directs=directs)
            if len(directs) == 2 and self.direction in directs:
                self.set_direction(self.direction)
            elif len(directs) == 2:
                opp = self.game.opposite_direction(self.direction)
                if opp in directs: directs.remove(opp)
                self.set_direction(directs[0])
            elif len(directs) == 1:
                self.set_direction(directs[0])
            else:
                opp = self.game.opposite_direction(self.direction)
                if opp in directs: directs.remove(opp)
                if len(directs)==0:
                    select_direct=None
                else:
                    select_direct = directs[random.randint(0, len(directs) - 1)]
                self.set_direction(select_direct)
        delta = self.game.directions.get(self.direction, None)
        if delta is None:
            self.direction = None
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
            self.__step_count = 0
        return self.__step_count
