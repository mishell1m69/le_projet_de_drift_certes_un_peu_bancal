import random
import pygame
import constants as ct

def update_particle_list(lst):
    for l,p in reversed(list(enumerate(lst))):
        if p.update():
            lst.pop(l)
            
def draw_particle_list(lst,cam_x,cam_y):
    for p in lst:
        p.draw(cam_x,cam_y)
        
        
class drift_mark:
    def __init__(self,x,y,lifespan,type):
        self.x = x
        self.y = y
        self.lifespan = lifespan
        self.rect = pygame.Rect(self.x-2,self.y-2,4,4) if type=="outer" else pygame.Rect(self.x-1,self.y-1,2,2)
        self.col = ct.COL2 if type=="outer" else ct.COL1 
        
    def draw(self,cam_x,cam_y):
        pygame.draw.rect(ct.RENDER_BUFFER, self.col, self.rect.move(-cam_x,-cam_y))
        
    def update(self):
        self.lifespan-=1
        if self.lifespan <= 0:
            return True
        return False
    
    
class snow:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.lifespan = random.randint(50,200)
        self.col = random.choice([ct.COL1,ct.COL2])
        
    def draw(self,cam_x,cam_y):
        
        if self.lifespan>150:
            ct.RENDER_BUFFER.set_at((self.x-cam_x-1,self.y-cam_y-1), self.col)
            ct.RENDER_BUFFER.set_at((self.x-cam_x+1,self.y-cam_y+1), self.col)
            ct.RENDER_BUFFER.set_at((self.x-cam_x+1,self.y-cam_y-1), self.col)
            ct.RENDER_BUFFER.set_at((self.x-cam_x-1,self.y-cam_y+1), self.col)
            ct.RENDER_BUFFER.set_at((self.x-cam_x,self.y-cam_y), self.col)
        
        elif self.lifespan>100:
            ct.RENDER_BUFFER.set_at((self.x-cam_x-1,self.y-cam_y), self.col)
            ct.RENDER_BUFFER.set_at((self.x-cam_x+1,self.y-cam_y), self.col)
            ct.RENDER_BUFFER.set_at((self.x-cam_x,self.y-cam_y-1), self.col)
            ct.RENDER_BUFFER.set_at((self.x-cam_x,self.y-cam_y+1), self.col)
            
        elif self.lifespan>50:
            ct.RENDER_BUFFER.set_at((self.x-cam_x,self.y-cam_y), self.col)
            ct.RENDER_BUFFER.set_at((self.x-cam_x+1,self.y-cam_y+1), self.col)
            
        else:
            ct.RENDER_BUFFER.set_at((self.x-cam_x,self.y-cam_y), self.col)
        
    def update(self):
        self.lifespan-=1
        self.x+=random.randint(-1,2)
        self.y+=random.randint(1,3)
        if self.lifespan <= 0:
            return True
        return False
        
        
        