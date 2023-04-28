import pygame as pg 
from vector import Vector 
from random import randint 


class Util:
    @staticmethod       # if random_sizes() is used, must call random_posn_velocity() * after * calling random_sizes()
    def random_posn_velocity(game, width, height):   
        left = randint(0, game.window_width - width)
        top = randint(0, game.window_height - height)
        max_v = game.max_v
        vx = game.speed * randint(1, max_v)
        vy = game.speed * randint(1, max_v)
        vxsign = randint(0, 1)
        vysign = randint(0, 1)
        vx *= (1 if vxsign == 0 else -1)
        vy *= (1 if vysign == 0 else -1)
        return pg.Rect(left, top, width, height), Vector(vx, vy)
    
    @staticmethod
    def random_color(min_rgb=50, max_rgb=255):
        color = (randint(min_rgb, max_rgb), randint(min_rgb, max_rgb), randint(min_rgb, max_rgb))
        return color

    @staticmethod
    def random_sizes(game, min_width=10, max_width=50, min_height=10, max_height=50):
        w = randint(min_width, game.window_width - max_width)
        h = randint(min_height, game.window_height - max_height)
        return w, h
    
    @staticmethod
    def clamp(posn, rect, settings):
        left, top = posn.x, posn.y
        width, height = rect.width, rect.height
        left = max(0, min(left, settings.screen_width - width))
        top = max(0, min(top, settings.screen_height - height))
        return Vector(x=left, y=top), pg.Rect(left, top, width, height)
