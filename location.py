import random
from pygame import *
from pygame import sprite
from wall import Wall
from dizzy import Dizzy
from food import Food
from point import Point
import os
from game import FOOD_SPAWN_EVENT, FOOD_SPAWN_TIME


class Location:
    def __init__(self, game):
        self.game = game
        self.surface = game.window
        self.startx = self.game.block_size
        self.starty = self.game.block_size

    def event(self, _event):
        pass

    def draw(self):
        pass

    def update(self):
        pass


class SelectPlayersMenu(Location):
    def __init__(self, game):
        super().__init__(game)


class LabyrinthLocation(Location):
    # wall_color = Color('green')
    lvl_list = []
    current_level = None
    # level = []
    map = {}
    foods_limit = 0
    LAYER_POINTS = 1
    LAYER_FOODS = 2
    LAYER_PLAYER = 3

    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.search_levels_in_folder()
        self.current_level = 0

        self.init_level()

    def search_levels_in_folder(self):
        files = os.listdir("levels")
        self.lvl_list = [n for n in filter(lambda x: x.endswith('.txt'), files)]
        self.lvl_list.sort()

    def go_to_next_level(self):
        self.current_level += 1
        self.init_level()

    def init_level(self):
        self.wallsGroup = sprite.Group()
        self.playerGroup = sprite.Group()
        self.foodGroup = sprite.Group()
        self.entities = sprite.LayeredUpdates()

        time.set_timer(FOOD_SPAWN_EVENT, FOOD_SPAWN_TIME)
        self.load_level_file(self.lvl_list[self.current_level % len(self.lvl_list)])

        self.buildLevel(self.level)
        self.player = Dizzy(self.startx + 7 * self.game.block_size, self.starty + (9 - 1) * self.game.block_size,
                            game=self.game, shape='dizzy')
        self.entities.add(self.player, layer=self.LAYER_PLAYER)
        self.playerGroup.add(self.player)
        self.player2 = Dizzy(self.startx + 5 * self.game.block_size, self.starty + (9 - 1) * self.game.block_size,
                             game=self.game, shape='pacman')
        self.entities.add(self.player2, layer=self.LAYER_PLAYER)
        self.playerGroup.add(self.player2)

        for i in range(3):
            self.spawn_food()

    def spawn_food(self):
        map_rows = len(self.map)
        map_cols = len(self.map['0'])
        while True:
            x = random.randint(0, map_rows - 1)
            y = random.randint(0, map_cols - 1)
            if self.get_map(x, y) is 0:
                food = Food(self.startx + x * self.game.block_size, self.starty + y * self.game.block_size,
                            self.game)
                food.set_active()
                self.foods_limit -= 1
                self.entities.add(food, layer=self.LAYER_FOODS)
                self.foodGroup.add(food)
                break

    def load_level_file(self, name):
        self.level = list()
        lvl_dir = os.getcwd() + "\\levels\\"
        lvl_flag = False
        self.foods_limit = 3
        for line in open(lvl_dir + name):
            if line.find('foods=') >= 0:
                p = line.partition('foods=')
                self.foods_limit = int(p[len(p) - 1])
            if line.strip() == '#start':
                lvl_flag = True
                continue
            elif line.strip() == '#end':
                lvl_flag = False
                continue
            if lvl_flag is True:
                self.level.append(line.strip())

    def buildLevel(self, descr):
        y = self.starty
        ny = 0
        self.map = dict()
        for row in descr:
            self.map[str(ny)] = dict()
            x = self.startx
            nx = 0
            for el in row:
                # self.map[str(ny)][str(nx)] = 0 if el == ' ' else 1
                self.set_map(nx, ny, 1 if el == '-' else 0)
                if el == '-':
                    wall = Wall(x, y, self.game)
                    self.wallsGroup.add(wall)
                    self.entities.add(wall, layer=self.LAYER_POINTS)
                elif el == 'f':
                    food = Food(x, y, self.game)
                    self.foodGroup.add(food)
                    self.entities.add(food, layer=self.LAYER_FOODS)
                elif el == ' ':
                    point = Point(x, y)
                    self.entities.add(point, layer=self.LAYER_FOODS)
                    self.foodGroup.add(point)
                x += self.game.block_size
                nx += 1
            y += self.game.block_size
            ny += 1

    def get_map(self, x, y):
        row = self.map.get(str(y), None)
        n = row.get(str(x), None) if (row is not None) else None
        return n  # self.map[str(y)][str(x)]

    def set_map(self, x, y, n):
        self.map[str(y)][str(x)] = n

    def get_allowed_directions_on_map(self, map_x, map_y):
        a = list()
        for dir in self.game.directions:
            x = map_x + self.game.directions[dir]['x']
            y = map_y + self.game.directions[dir]['y']
            if self.get_map(x, y) == 0:
                a.append(dir)
        return a

    def isnt_any_player_on_direction(self, x, y, directs):
        coord1 = {'x': self.convert_x_to_mapx(self.player.rect.centerx), 'y': self.convert_y_to_mapy(self.player.rect.centery)}
        coord2 = {'x': self.convert_x_to_mapx(self.player2.rect.centerx), 'y': self.convert_y_to_mapy(self.player2.rect.centery)}
        out = list()
        for direct in directs:
            delta = self.game.directions[direct]
            i = 0
            while True:
                i += 1
                sx = x + i * delta['x']
                sy = y + i * delta['y']
                if self.get_map(str(sx),str(sy)) is not 0:
                    out.append(direct)
                    break
                elif (sx == coord1['x'] and sy == coord1['y']) or (sx == coord2['x'] and sy == coord2['y']):
                    break
        return out

    def draw(self):
        self.surface.fill(Color("#000400"))
        # self.player.draw(self.screen)
        Food.conductor.play()
        self.entities.draw(self.surface)

    def update(self):
        self.entities.update()
        sprite.groupcollide(self.playerGroup, self.foodGroup, False, True)
        if len(self.foodGroup) == 0:
            self.go_to_next_level()

    def event(self, _event):
        if _event.type == FOOD_SPAWN_EVENT:
            self.spawn_food()
            if self.foods_limit <= 0: time.set_timer(FOOD_SPAWN_EVENT, 0)
        pressed_keys = key.get_pressed()
        # if _event.type == KEYDOWN:
        map_x = self.convert_x_to_mapx(self.player.rect.centerx)
        # (self.player.rect.centerx - self.startx) // self.game.block_size
        map_y = self.convert_y_to_mapy(self.player.rect.centery)
        # ((self.player.rect.centery - self.starty) // self.game.block_size)
        if pressed_keys[K_UP]:  # _event.key == K_UP:
            if self.get_map(map_x, map_y - 1) == 0:  # self.map[str(map_y - 1)][str(map_x)] == 0:
                self.player.set_direction('up')
        elif pressed_keys[K_DOWN]:  # _event.key == K_DOWN:
            if self.get_map(map_x, map_y + 1) == 0:  # self.map[str(map_y + 1)][str(map_x)] == 0:
                self.player.set_direction('down')
        elif pressed_keys[K_RIGHT]:  # _event.key == K_RIGHT:
            if self.get_map(map_x + 1, map_y) == 0:  # self.map[str(map_y)][str(map_x + 1)] == 0:
                self.player.set_direction('right')
        elif pressed_keys[K_LEFT]:  # _event.key == K_LEFT:
            if self.get_map(map_x - 1, map_y) == 0:  # self.map[str(map_y)][str(map_x - 1)] == 0:
                self.player.set_direction('left')

        map_x = self.convert_x_to_mapx(self.player2.rect.centerx)
        # (self.player.rect.centerx - self.startx) // self.game.block_size
        map_y = self.convert_y_to_mapy(self.player2.rect.centery)
        # ((self.player.rect.centery - self.starty) // self.game.block_size)
        if pressed_keys[K_w]:  # _event.key == K_UP:
            if self.get_map(map_x, map_y - 1) == 0:  # self.map[str(map_y - 1)][str(map_x)] == 0:
                self.player2.set_direction('up')
        elif pressed_keys[K_s]:  # _event.key == K_DOWN:
            if self.get_map(map_x, map_y + 1) == 0:  # self.map[str(map_y + 1)][str(map_x)] == 0:
                self.player2.set_direction('down')
        elif pressed_keys[K_d]:  # _event.key == K_RIGHT:
            if self.get_map(map_x + 1, map_y) == 0:  # self.map[str(map_y)][str(map_x + 1)] == 0:
                self.player2.set_direction('right')
        elif pressed_keys[K_a]:  # _event.key == K_LEFT:
            if self.get_map(map_x - 1, map_y) == 0:  # self.map[str(map_y)][str(map_x - 1)] == 0:
                self.player2.set_direction('left')

    def convert_x_to_mapx(self, x):
        map_x = (x - self.startx) // self.game.block_size
        return map_x

    def convert_y_to_mapy(self, y):
        map_y = (y - self.starty) // self.game.block_size
        return map_y
