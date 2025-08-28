import pygame
from numpy.linalg import norm
from math import sin,cos,pi
import math
import settings

class Sprite(pygame.sprite.Sprite):
	#class for all sprites
    def __init__(self, image, x=0, y=0, v=0, direction=[0,0], constraints = None, reflection = False):
        super().__init__()
        self.x = x
        self.y = y
        self.v = v
        self.direction = direction
        self.constraints = constraints
        self.reflection = reflection
        self._norm = norm(direction)
        self.set_image(image)        

    def set_image(self, image):
        self.surface = image.surface
        self.w = image.w
        self.h = image.h
        self.rect = pygame.Rect(int(self.x),int(self.y),self.w,self.h)

    def change_image(self, image):
        #changes the image preserving the center of the sprite
        center = self.rect.center
        self.set_image(image)
        self.rect.center = center
        self.change_position(self.rect.x,self.rect.y)
        

    def change_direction(self, x, y):
        self.direction = [x,y]
        self._norm = norm(self.direction)

    def turn_direction(self, phi):
        """turns the direction of the sprite counter-clockwise, angle measured in radians"""
        self.change_direction(self.direction[0]*cos(phi)+self.direction[1]*sin(phi),-self.direction[0]*sin(phi)+self.direction[1]*cos(phi))

    def change_position(self, x, y):
        if self.constraints is None:
            self.x,self.y = x,y
        else:
            x_clamp = min(max(x,self.constraints.x),self.constraints.right-self.w)
            y_clamp = min(max(y,self.constraints.y),self.constraints.bottom-self.h) 
            if self.reflection:
                if x != x_clamp:
                    self.x = 2*x_clamp-x
                    self.direction[0] *= -1
                else:
                    self.x = x_clamp
                if y != y_clamp:
                    self.y = 2*y_clamp-y
                    self.direction[1] *= -1
                else:
                    self.y = y_clamp
            else:
                self.x,self.y = x_clamp,y_clamp
        self.rect.x,self.rect.y = int(self.x),int(self.y)

    def update(self,dt):
        if self._norm != 0 and self.v != 0:
            newx = self.x+dt*self.v*self.direction[0]/self._norm
            newy = self.y+dt*self.v*self.direction[1]/self._norm
            self.change_position(newx,newy)

    def blit(self, screen):
        screen.blit(self.surface, self.rect)