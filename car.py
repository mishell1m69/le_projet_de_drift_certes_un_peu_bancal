
import pygame
import entities as e
import tools as t
import constants as ct
import math
import particles as p
import random

class Car():
    
    def __init__(self,x,y):
        self.back = e.Entity(x-20,y) #center between both back wheels
        self.front = e.Entity(x+20,y) #center between both front wheels
        self.back_direction_vector = [1,0] #direction vector : where the back wheels (the whole car) are facing
        self.front_wheel_angle = 0 #angle of the front wheel in RAD
        self.front_direction_vector = [1,0] #direction of the front wheel
        self.center_of_mass = e.Entity(x,y) #center between both front wheels
        self.is_drifting = False #Bool, is drifting or not
        self.actual_front_direction = [0,0] #direction of the front wheel based on the plan, not the car
        self.speed_mult = 0.3 #how much the car should accelerate
        self.last_wheel_update = 0 #counts the amount of frames before the last update of the wheels angle
        self.drift_particles_outer = [] #the list of outer drifting particles of this car
        self.drift_particles_inner = [] #the list of inner drifting particles of this car
        self.img = pygame.image.load("car.png").convert()
        


    def update(self):
        self.back.update()
        self.front.update()
        self.center_of_mass.update()
        
        self.front_direction_vector = t.angle_to_vec(self.front_wheel_angle)
        self.back_direction_vector = t.normalize(t.getvect(self.back.x,self.back.y,self.front.x,self.front.y))
        
        if self.last_wheel_update>10:
            self.front_wheel_angle *= 0.9
        if abs(self.front_wheel_angle)<0.1:
            self.front_wheel_angle = 0
        self.last_wheel_update += 1
        
        
        front_back_vect = t.getvect(self.back.x,self.back.y,self.front.x,self.front.y)
        self.input()
        self.actual_front_direction = t.angle_to_vec(t.vec_to_angle(self.back_direction_vector )+self.front_wheel_angle)
        self.back.momentum_x = (self.back.momentum_x + self.center_of_mass.momentum_x)/2
        self.back.momentum_y = (self.back.momentum_y + self.center_of_mass.momentum_y)/2
        self.front.momentum_x = (self.front.momentum_x + self.center_of_mass.momentum_x)/2 + self.actual_front_direction[0] * t.dist(0,0,self.front.momentum_x,self.front.momentum_y)/5
        self.front.momentum_y = (self.front.momentum_y + self.center_of_mass.momentum_y)/2 + self.actual_front_direction[1] * t.dist(0,0,self.front.momentum_x,self.front.momentum_y)/5
        
        
        front_back_vect = t.normalize(front_back_vect,25)
        
        self.front.x = self.back.x + front_back_vect[0]
        self.front.y = self.back.y + front_back_vect[1]
        self.center_of_mass.x = self.back.x + front_back_vect[0]/2
        self.center_of_mass.y = self.back.y + front_back_vect[1]/2

        if abs(abs(t.vec_to_angle(self.back_direction_vector))-abs(t.vec_to_angle([self.front.momentum_x,self.front.momentum_y]))) > 0.4 and t.dist(0,0,self.front.momentum_x,self.front.momentum_y)>1:
            car_perp = t.perp_vec(self.back_direction_vector)
            car_perp_x = car_perp[0]*7
            car_perp_y = car_perp[1]*7
            
            
            back_speed = t.dist(0,0,self.back.momentum_x,self.back.momentum_y)
            for i in range(int(back_speed)):
                a = -i*self.back.momentum_x/back_speed
                b = -i*self.back.momentum_y/back_speed
                
            
                lifespan = random.randint(100,110)
                self.drift_particles_outer.append(p.drift_mark(self.front.x+car_perp_x+a,self.front.y+car_perp_y+b,lifespan,"outer"))
                self.drift_particles_inner.append(p.drift_mark(self.front.x+car_perp_x+a,self.front.y+car_perp_y+b,lifespan,"inner"))
                
                lifespan = random.randint(100,110)
                self.drift_particles_outer.append(p.drift_mark(self.front.x-car_perp_x+a,self.front.y-car_perp_y+b,lifespan,"outer"))
                self.drift_particles_inner.append(p.drift_mark(self.front.x-car_perp_x+a,self.front.y-car_perp_y+b,lifespan,"inner"))
                
                lifespan = random.randint(100,110)
                self.drift_particles_outer.append(p.drift_mark(self.back.x+car_perp_x+a,self.back.y+car_perp_y+b,lifespan,"outer"))
                self.drift_particles_inner.append(p.drift_mark(self.back.x+car_perp_x+a,self.back.y+car_perp_y+b,lifespan,"inner"))
                
                lifespan = random.randint(100,110)
                self.drift_particles_outer.append(p.drift_mark(self.back.x-car_perp_x+a,self.back.y-car_perp_y+b,lifespan,"outer"))
                self.drift_particles_inner.append(p.drift_mark(self.back.x-car_perp_x+a,self.back.y-car_perp_y+b,lifespan,"inner"))
            
        p.update_particle_list(self.drift_particles_outer)
        p.update_particle_list(self.drift_particles_inner)

        
    
    def draw(self,cam_x,cam_y):
        
        p.draw_particle_list(self.drift_particles_outer,cam_x,cam_y)
        p.draw_particle_list(self.drift_particles_inner,cam_x,cam_y)
        
        t.line(self.back.x-cam_x,self.back.y-cam_y,self.front.x-cam_x,self.front.y-cam_y,ct.COL2)
        #t.line(self.front.x-cam_x,self.front.y-cam_y,self.front.x+self.actual_front_direction[0]*10-cam_x,self.front.y+self.actual_front_direction[1]*10-cam_y,(255,0,0)) #debug, show wheel direction
        ct.RENDER_BUFFER.blit(self.img, (self.center_of_mass.x-cam_x-20, self.center_of_mass.y-cam_y-20), pygame.Rect(40*int(t.vec_to_angle(self.back_direction_vector)/(2*math.pi) *7 + 4.25),0,40,40))
        
    
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_z]:
            self.back.momentum_x+=self.back_direction_vector[0]*self.speed_mult
            self.back.momentum_y+=self.back_direction_vector[1]*self.speed_mult
            self.center_of_mass.momentum_x+=self.back_direction_vector[0]*self.speed_mult
            self.center_of_mass.momentum_y+=self.back_direction_vector[1]*self.speed_mult
        if keys[pygame.K_LEFT] and self.front_wheel_angle>-1 or keys[pygame.K_q] and self.front_wheel_angle>-1:
            self.last_wheel_update = 0
            self.front_wheel_angle-=0.1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.back.momentum_x-=self.back_direction_vector[0]*self.speed_mult
            self.back.momentum_y-=self.back_direction_vector[1]*self.speed_mult
            self.center_of_mass.momentum_x-=self.back_direction_vector[0]*self.speed_mult
            self.center_of_mass.momentum_y-=self.back_direction_vector[1]*self.speed_mult
        if keys[pygame.K_RIGHT] and self.front_wheel_angle<1 or keys[pygame.K_d] and self.front_wheel_angle<1:
            self.last_wheel_update = 0
            self.front_wheel_angle+=0.1
            