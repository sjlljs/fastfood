import unittest
from unittest.mock import *
from wall import Wall
from location import *
from game import Game
from pygame import *
from dizzy import Dizzy
from food import Food


class DizzyTestCase(unittest.TestCase):
    def setUp(self):
        self.x = 20
        self.y = 30
        self.game = MagicMock()
        self.game.block_size = 20
        Dizzy.set_image = MagicMock()
        Dizzy.set_rect=MagicMock()
        self.dizzy = Dizzy(self.x, self.y, self.game, '')
        self.dizzy.rect=Rect(x=self.x,y=self.y)

    def test_dizzy_has_image(self):
        self.assertIsInstance(self.dizzy.image, Surface)

    def test_center_coords_are_correct(self):
        self.assertEqual((self.x, self.y), self.dizzy.rect.center)

    def test_dizzy_can_move_up(self):
        self.dizzy.set_direction('up')
        yc = self.y
        for i in range(self.dizzy.steps):
            res = self.dizzy.update()
            self.assertEqual(self.x, self.dizzy.rect.centerx)
            self.assertLess(self.dizzy.rect.centery, yc)
            yc = self.dizzy.rect.centery
        res = self.dizzy.update()
        self.assertEqual((self.x, yc), self.dizzy.rect.center)

    def test_dizzy_can_move_down(self):
        self.dizzy.set_direction('down')
        yc = self.y
        for i in range(self.dizzy.steps):
            res = self.dizzy.update()
            self.assertEqual(self.x, self.dizzy.rect.centerx)
            self.assertGreater(self.dizzy.rect.centery, yc)
            yc = self.dizzy.rect.centery
        self.dizzy.update()
        self.assertEqual((self.x, yc), self.dizzy.rect.center)

    def test_dizzy_can_move_left(self):
        self.dizzy.set_direction('left')
        xc = self.x
        for i in range(self.dizzy.steps):
            res = self.dizzy.update()
            self.assertEqual(self.y, self.dizzy.rect.centery)
            self.assertLess(self.dizzy.rect.centerx, xc)
            xc = self.dizzy.rect.centerx
        self.dizzy.update()
        self.assertEqual((xc, self.y), self.dizzy.rect.center)

    def test_dizzy_can_move_right(self):
        self.dizzy.set_direction('right')
        xc = self.x
        for i in range(self.dizzy.steps):
            res = self.dizzy.update()
            self.assertEqual(self.y, self.dizzy.rect.centery)
            self.assertGreater(self.dizzy.rect.centerx, xc)
            xc = self.dizzy.rect.centerx
        self.dizzy.update()
        self.assertEqual((xc, self.y), self.dizzy.rect.center)

    def test_dizzy_has_nonzero_step_params(self):
        self.assertEqual(self.dizzy.steps, 5)
        self.assertGreater(self.dizzy.step_val, 0)


class FoodTestCase(unittest.TestCase):
    def setUp(self):
        pass


class WallTestCase(unittest.TestCase):
    def setUp(self):
        self.x = 5
        self.y = 7
        self.game = MagicMock()
        self.game.block_size = 20
        self.wall = Wall(self.x, self.y, self.game)

    def test_wall_has_image(self):
        self.assertIsInstance(self.wall.image, Surface)

    def test_center_coords_are_correct(self):
        self.assertEqual((self.x, self.y), self.wall.rect.center)


class LabyrinthTestCase(unittest.TestCase):
    def setUp(self):
        self.game = MagicMock()
        self.game.directions = Game.directions
        self.game.block_size = 20
        m_init = MagicMock()
        with patch('location.LabyrinthLocation.init_level', m_init):
            self.location = LabyrinthLocation(self.game)

    @patch("os.getcwd")
    def test_load_level_from_file(self, mock_os):
        file = '#start\n---\n- -\n---\n#end'
        m = mock_open(read_data=file)
        m.return_value.__iter__ = lambda self: self
        m.return_value.__next__ = lambda self: self.readline()
        with patch('builtins.open', m):
            self.location.load_level_file('hhh')
        assert m.called
        self.assertEqual(self.location.level, ['---', '- -', '---'])

    def test_build_correct_number_of_blocks(self):
        self.location.buildLevel(['-- --'])
        self.assertEqual(len(self.location.wallsGroup), 4)

    def test_level_draw_horizontal(self):
        x = None
        y = None
        self.location.buildLevel(['---'])
        self.assertEqual(len(self.location.wallsGroup), 3)
        for wall in self.location.wallsGroup:
            if x is None:
                x = wall.rect.centerx
                y = wall.rect.centery
                continue
            self.assertEqual(y, wall.rect.centery)
            self.assertNotEqual(x, wall.rect.centerx)
            x = wall.rect.centerx

    def test_level_map_horizontal(self):
        self.location.buildLevel(['---'])
        self.assertEqual(len(self.location.map), 1)
        self.assertEqual(len(self.location.map['0']), 3)
        self.assertEqual(self.location.map, {'0': {'0': 1, '1': 1, '2': 1}})

    def test_level_draw_vertical(self):
        x = None
        y = None
        self.location.buildLevel(['-', '-', '-'])
        self.assertEqual(len(self.location.wallsGroup), 3)
        for wall in self.location.wallsGroup:
            if x is None:
                x = wall.rect.centerx
                y = wall.rect.centery
                continue
            self.assertEqual(x, wall.rect.centerx)
            self.assertNotEqual(y, wall.rect.centery)
            y = wall.rect.centery

    def test_level_map_vertical(self):
        self.location.buildLevel(['-', '-', '-'])
        self.assertEqual(len(self.location.map), 3)
        self.assertEqual(self.location.map, {'0': {'0': 1}, '1': {'0': 1}, '2': {'0': 1}})

    def test_map_get_directions(self):
        self.location.buildLevel(['---', '- -', '   ', '- -'])
        directs = self.location.get_allowed_directions_on_map(1, 1)
        self.assertEqual(directs, ['down', ])
        directs = self.location.get_allowed_directions_on_map(1, 2)
        self.assertEqual(directs.sort(), ['down', 'up', 'right', 'left'].sort())
        directs = self.location.get_allowed_directions_on_map(1, 3)
        self.assertEqual(directs, ['up', ])
        directs = self.location.get_allowed_directions_on_map(0, 2)
        self.assertEqual(directs, ['right', ])
        directs = self.location.get_allowed_directions_on_map(2, 2)
        self.assertEqual(directs, ['left', ])

    def test_if_food_see_any_playes(self):
        self.location.buildLevel(['---', '- -', '   ', '- -'])
        self.location.convert_x_to_mapx = MagicMock(return_value=1)
        self.location.convert_y_to_mapy = MagicMock(return_value=1)
        self.location.player = MagicMock()
        self.location.player2 = MagicMock()
        directs = self.location.get_allowed_directions_on_map(1, 3)
        directs2 = self.location.isnt_any_player_on_direction(1, 3, directs)
        self.assertEqual(directs2, [])
        directs = self.location.get_allowed_directions_on_map(1, 2)
        directs2 = self.location.isnt_any_player_on_direction(1, 2, directs)
        self.assertEqual(directs2.sort(), ['down', 'left', 'right'].sort())


if __name__ == '__main__':
    unittest.main()
