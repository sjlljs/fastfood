import pygame
import pyganim
from location import *
import pyganim

# константы
FPS = 20
WIN_WIDTH = 1024
WIN_HEIGHT = 700
FOOD_SPAWN_EVENT = pygame.USEREVENT + 1
FOOD_SPAWN_TIME = 4000


class Game:
    location = None
    window = None
    block_size = 50
    directions = {'up': {'x': 0, 'y': -1}, "down": {'x': 0, 'y': 1}, 'left': {'x': -1, 'y': 0},
                  'right': {'x': 1, 'y': 0}}

    def __init__(self):
        pygame.init()
        pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("Fast Food Dizzy")
        self.window = pygame.display.get_surface()
        self.window_size = self.window.get_size()
        pygame.key.set_repeat(10)
        pygame.event.Event(FOOD_SPAWN_EVENT)
        self.set_food_animation()
        self.set_player_sprite()
        self.location = LabyrinthLocation(self)

    def set_player_sprite(self):
        rects = []
        sprites = pyganim.getImagesFromSpriteSheet(filename='sprites\pacman.png', rows=11, cols=6, rects=rects)
        for sp in sprites:
            sp.convert()
            sp.set_colorkey(sp.get_at((0, 0)), RLEACCEL)
        pl = dict(
            right=[pygame.transform.scale(sprites[i], (self.block_size - 2, self.block_size - 2)) for i in range(6)],
            left=[pygame.transform.scale(sprites[i + 6], (self.block_size - 2, self.block_size - 2)) for i in range(6)],
            up=[pygame.transform.scale(sprites[i + 12], (self.block_size - 2, self.block_size - 2)) for i in range(6)],
            down=[pygame.transform.scale(sprites[i + 18], (self.block_size - 2, self.block_size - 2)) for i in
                  range(6)],
            stand=pygame.transform.scale(sprites[len(sprites) - 1], (self.block_size - 2, self.block_size - 2))
        )
        Dizzy.sprite.update([('pacman', pl)])
        rects = []
        sprites = pyganim.getImagesFromSpriteSheet(filename='sprites\dizzy.png', cols=1, rows=16, rects=rects)
        for sp in sprites:
            sp.convert()
            sp.set_colorkey(sp.get_at((0, 0)), RLEACCEL)
        pl = dict(
            right=[pygame.transform.scale(sprites[i + 12], (self.block_size - 2, self.block_size - 2)) for i in
                   range(4)],
            left=[pygame.transform.scale(sprites[i + 8], (self.block_size - 2, self.block_size - 2)) for i in range(4)],
            up=[pygame.transform.scale(sprites[i], (self.block_size - 2, self.block_size - 2)) for i in range(4)],
            down=[pygame.transform.scale(sprites[i + 4], (self.block_size - 2, self.block_size - 2)) for i in range(4)],
            stand=pygame.transform.scale(sprites[6], (self.block_size - 2, self.block_size - 2))
        )
        Dizzy.sprite.update([('dizzy', pl)])

    def set_food_animation(self):
        Food.anim['burger'] = self.get_anim_from_file('burger.png', cols=1, rows=4)
        Food.anim['pizza'] = self.get_anim_from_file('pizza.png', cols=1, rows=4)
        Food.anim['chicken'] = self.get_anim_from_file('chicken.png', cols=1, rows=4)
        Food.anim['hotdog'] = self.get_anim_from_file('hotdog.png', cols=1, rows=4)
        Food.anim['cocktail1'] = self.get_anim_from_file('cocktail1.png', cols=1, rows=4)
        Food.anim['cocktail2'] = self.get_anim_from_file('cocktail2.png', cols=1, rows=4)
        Food.conductor = pyganim.PygConductor(Food.anim)

    def get_anim_from_file(self, name, cols, rows):
        rects = []
        sprites = pyganim.getImagesFromSpriteSheet(filename='sprites\\' + name, cols=cols, rows=rows,
                                                   rects=rects)
        # sprites=[pygame.transform.scale(sp,(self.block_size - 2, self.block_size - 2)) for sp in sprites]
        for sp in sprites:
            sp.convert()
            sp.set_colorkey(sp.get_at((0, 0)), RLEACCEL)
        anim = pyganim.PygAnimation([(sp, 150) for sp in sprites])
        anim.scale((self.block_size - 2, self.block_size - 2))
        anim.makeTransformsPermanent()
        return anim

    def event(self, _event):
        run = True
        if _event.type == pygame.QUIT or (
                        _event.type == pygame.KEYDOWN and _event.key == pygame.K_ESCAPE):
            # or (_event.type == KEYDOWN and _event.key == K_ESCAPE and
            #            type(self.location) == StartLocation(self).__class__):
            run = False
        elif _event.type == pygame.KEYDOWN and _event.key == pygame.K_0:
            self.location.go_to_next_level()
        return run

    def opposite_direction(self, direct):
        if direct == 'up':
            return 'down'
        elif direct == 'down':
            return "up"
        elif direct == 'left':
            return 'right'
        elif direct == 'right':
            return 'left'
        else:
            return None


def main():
    game = Game()
    clock = pygame.time.Clock()
    # game.location = StartLocation()
    running = True
    while running:  # Основной цикл программы
        # game.location.draw()
        for e in pygame.event.get():  # Обрабатываем события
            running = game.event(e)
            game.location.event(e)
        game.location.update()
        game.location.draw()
        pygame.display.flip()
        clock.tick(FPS)
        # window.blit(bg, (0,0))      # Каждую итерацию необходимо всё перерисовывать
        # pygame.display.update()  # обновление и вывод всех изменений на экран


# ========================================

if __name__ == '__main__':
    main()
