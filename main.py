"""The game's main file"""
#Library import

#C:\Users\Admin\AppData\Roaming\Python\Python313\Scripts\pyinstaller.exe --onefile -w main.py to get .exe

import pygame
import time

import constants as ct
import car as c
import particles as p
import random






class App:

    def __init__(self):
        """
        Called on game startup, all basic stuff
        """
        

        #Creating basics of the game
        self.screen_mult = 6
        self.screen_size = (ct.GAME_DRAW_SIZE_X * self.screen_mult, ct.GAME_DRAW_SIZE_Y * self.screen_mult)
        pygame.init()
        self.running = True
        ct.RENDER_BUFFER = pygame.Surface((ct.GAME_DRAW_SIZE_X, ct.GAME_DRAW_SIZE_Y), pygame.OPENGL)
        ct.CLOCK = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.screen_size)
        self.snow_particles = []
        self.floor = pygame.image.load("desnow.png").convert()
        #pygame.mouse.set_visible(False)
        
        self.playing = True
        pygame.mixer.init()
        #pygame.mixer.music.load("loop.mp3")
        #pygame.mixer.music.play(5)
        
        self.cam_x = 0
        self.cam_y = 0
        
        self.player = c.Car(100,100)

        #Starting game loop
        self.loop()

    def loop(self):
        """
        Global game loop
        """
        while self.running:
            ct.CLOCK.tick(30)
            
            self.update()
            self.draw()



        pygame.quit()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.playing = not self.playing
            elif event.type == pygame.QUIT:
                self.running = False
        if self.playing:
            self.cam_x = self.player.front.x-160
            self.cam_y = self.player.front.y-90
            self.snow_particles.append(p.snow(self.cam_x+random.randint(-10,330),self.cam_y+random.randint(-10,20)))
            p.update_particle_list(self.snow_particles)
            self.player.update()

    def draw(self):
        """called anytime the game will try to refresh screen
        """
        ct.RENDER_BUFFER.fill(ct.COL1)
        self.draw_floor()
        self.player.draw(self.cam_x,self.cam_y)
        p.draw_particle_list(self.snow_particles,self.cam_x,self.cam_y)
        pygame.transform.scale_by(ct.RENDER_BUFFER, self.screen_mult, self.screen)
        pygame.display.update()

    def draw_floor(self):
        for x in range(int((self.cam_x-128)/128)*128,int((self.cam_x+449)/128)*128,128):
            for y in range(int((self.cam_y-128)/128)*128,int((self.cam_y+309)/128)*128,128):
                r = int(hash(str(x))+hash(str(y)))%20
                if r<1:
                    ct.RENDER_BUFFER.blit(self.floor, (x-self.cam_x,y-self.cam_y), pygame.Rect(0,0,128,128))


        

if __name__ == '__main__':
    App()
