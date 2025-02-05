
import pygame

class Entity:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.momentum_x = 0
        self.momentum_y = 0
        
    def update(self):
        self.x += self.momentum_x
        self.y += self.momentum_y
        self.momentum_x *= 0.98
        self.momentum_y *= 0.98
    
    def draw(self):
        pass