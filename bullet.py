import pygame
from pygame.locals import *
import settings
import image
from sprite import Sprite

class Bullet(Sprite):
    """A class to manage the bullets shot by the ship"""

    def __init__(self, x, y, speed, size):
        super().__init__(image.bullet[size],x,y,v=speed,direction=[0,-1])
        self.damage = size
