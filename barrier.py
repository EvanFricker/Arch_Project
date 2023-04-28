import pygame as pg
from pygame.sprite import Sprite, Group


class BarrierPiece(Sprite):
    def __init__(self, game, rect):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.rect = rect

    def hit(self):
        print('BarrierPiece hit!')
        self.kill()

    def update(self): pass

    def draw(self):
        pg.draw.rect(self.screen, pg.Color(60, 60, 60), self.rect)


class Barrier(Sprite):    # not a real Barrier class -- should be made up of many tiny Sprites
                          # you will not get credit for this class unless it is updated to tiny Sprites
    color = 200, 200, 200
    black = 0, 0, 0
    health_colors = {4: pg.Color(0, 255, 0),
                     3: pg.Color(255, 255, 0),
                     2: pg.Color(255, 128, 0),
                     1: pg.Color(255, 0, 0),
                     0: pg.Color(0, 0, 0)}

    def __init__(self, game, width, height, deltax, deltay, x, y):
        super().__init__()
        self.game = game
        self.screen = game.screen
        # self.rect = rect

        self.width, self.height = width, height
        self.x, self.y = x, y
        self.deltax, self.deltay = deltax, deltay
        self.settings = game.settings
        self.ship_lasers = game.ship_lasers
        self.alien_lasers = game.alien_lasers
        self.barrier_pieces = Group()
        self.create_barrier_pieces()

    def create_barrier_pieces(self):
        left, top = 0, 0
        for i in range(int(self.height/self.deltax)):
            for j in range(int(self.width/self.deltay)):
                rect = pg.Rect(self.x + left + j * self.deltax, 
                               self.y + top + i * self.deltay, 
                               self.deltax, self.deltay)
                self.barrier_pieces.add(BarrierPiece(game=self.game, rect=rect))


    def reset(self):
        self.barrier_pieces.empty()
        self.create_barrier_pieces()

    def is_dead(self): return self.health == 0

    def update(self): 
        _ = pg.sprite.groupcollide(self.barrier_pieces, self.ship_lasers.lasers, True, True)
        _ = pg.sprite.groupcollide(self.barrier_pieces, self.alien_lasers.lasers, True, True)
        self.draw()

    def draw(self):
        for bp in self.barrier_pieces:
            bp.draw()


BARRIER_WIDTH = 80
BARRIER_HEIGHT = 40

class Barriers:
    positions = [(BARRIER_WIDTH * x + BARRIER_WIDTH / 2.0, 600) for x in range(0, 14, 2)]
    def __init__(self, game):
        self.game = game
        self.settings = game.settings
        self.barriers = Group()
        self.create_barriers()

    def create_barriers(self):     
        width = self.settings.screen_width / 10
        height = 8.0 * width / 4.0
        top = self.settings.screen_height - 2.1 * height
                
        barriers = [Barrier(game=self.game, 
                            width=BARRIER_WIDTH, height=BARRIER_HEIGHT, 
                            deltax=20, deltay=20, 
                            x=x, y=y - 50) for x, y in Barriers.positions]
        for barrier in barriers:
            self.barriers.add(barrier)

    def hit(self): pass 
    
    def reset(self):
        for barrier in self.barriers:
            barrier.reset()

    def update(self):
        for barrier in self.barriers:
            barrier.update()

    def draw(self):
        for barrier in self.barriers: 
            barrier.draw()

