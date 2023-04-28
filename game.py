import pygame as pg
from settings import Settings
from laser import Lasers, LaserType
from alien import Aliens
from ship import Ship
from sound import Sound
from scoreboard import Scoreboard
from vector import Vector
from barrier import Barriers
import sys

pg.joystick.init()
joysticks = [pg.joystick.Joystick(i) for i in range(pg.joystick.get_count())]


class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        size = self.settings.screen_width, self.settings.screen_height   # tuple
        self.screen = pg.display.set_mode(size=size)
        pg.display.set_caption("Alien Invasion")

        self.sound = Sound(bg_music="sounds/startrek.wav")
        self.scoreboard = Scoreboard(game=self)

        self.ship_lasers = Lasers(settings=self.settings, type=LaserType.SHIP)
        self.alien_lasers = Lasers(settings=self.settings, type=LaserType.ALIEN)
        
        self.barriers = Barriers(game=self)
        self.ship = Ship(game=self)
        self.aliens = Aliens(game=self)
        self.settings.initialize_speed_settings()

    def handle_events(self):
        keys_dir = {pg.K_w: Vector(0, -1), pg.K_UP: Vector(0, -1), 
                    pg.K_s: Vector(0, 1), pg.K_DOWN: Vector(0, 1),
                    pg.K_a: Vector(-1, 0), pg.K_LEFT: Vector(-1, 0),
                    pg.K_d: Vector(1, 0), pg.K_RIGHT: Vector(1, 0)}
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game_over()

            # BEGINNING OF HARDWARE INTEGRATION
            # This segment deals with button pushes. A will fire a laser, and B will quit the game
            elif event.type == pg.JOYBUTTONDOWN:
                if event.button == 0:
                    self.ship.open_fire()
                if event.button == 1:
                    self.game_over()

            # This will stop firing when A is unreleased
            elif event.type == pg.JOYBUTTONUP:
                if event.button == 0:
                    self.ship.cease_fire()

            # This controls movement with the joystick. The ship can move left and right with joystick controls.
            elif event.type == pg.JOYAXISMOTION:
                if event.axis == 0:
                    if event.value >= 0.95:
                        self.ship.v += self.settings.ship_speed * keys_dir[pg.K_d]
                    if event.value <= -0.95:
                        self.ship.v += self.settings.ship_speed * keys_dir[pg.K_a]
                    if -0.95 < event.value < 0.95:
                        self.ship.v = Vector()
            # END OF HARDWARE INTEGRATION

            elif event.type == pg.KEYDOWN:
                key = event.key
                if key in keys_dir:
                    self.ship.v += self.settings.ship_speed * keys_dir[key]
                elif key == pg.K_SPACE:
                    self.ship.open_fire()
            elif event.type == pg.KEYUP:
                key = event.key
                if key in keys_dir:
                    self.ship.v = Vector()
                elif key == pg.K_SPACE:
                    self.ship.cease_fire()

    def reset(self):
        print('Resetting game...')
        # self.lasers.reset()    # handled by ship for ship_lasers and by aliens for alien_lasers
        self.barriers.reset()
        self.ship.reset()
        self.aliens.reset()
        self.scoreboard.reset()

    def game_over(self):
        print('All ships gone: game over!')
        self.sound.gameover()
        pg.quit()
        sys.exit()

    def play(self):
        self.sound.play_bg()
        while True:     
            self.handle_events() 
            self.screen.fill(self.settings.bg_color)
            self.ship.update()
            self.aliens.update()
            self.barriers.update()
            # self.lasers.update()    # handled by ship for ship_lasers and by alien for alien_lasers
            self.scoreboard.update()
            pg.display.flip()


def main():
    g = Game()
    g.play()


if __name__ == '__main__':
    main()
