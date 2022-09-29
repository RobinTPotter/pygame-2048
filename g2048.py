#! /usr/bin/python3

import pygame as pg
import threading

class Colours():
    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)
    darkBlue = (0,0,128)
    white = (255,255,255)
    black = (0,0,0)
    pink = (255,200,200)
    yellow = (255,255,0)

class Gogo():
    def __init__(self, size=(640, 480)):
        self.clock = pg.time.Clock()
        self.working = True
        self.ww=size[0]
        self.wh=size[1]
        self.thread = threading.Thread(target=self.gogo)
        pg.font.init()
        self.w,self.h = 4,4
        self.cw, self.ch = 40,40
        self.init()
        self.align()
        print(self.grid)
        #print(self.find_next(nx,ny))
        self.my_font = pg.font.SysFont('Comic Sans MS', 20)
        self.thread.start()
        
    def align(self):        
        gh = self.h*(self.ch+2)-2
        gw = self.w*(self.cw+2)-2
        self.ox, self.oy = self.ww/2 - gw/2, self.wh/2 - gh/2

    def init(self):
        self.grid = [[0 for _ in range(self.w)] for _ in range(self.h)]
        nx, ny = self.add_number()
        print (nx,ny)
   
    def get_working(self):
        return self.working
            
    def what_next(self,x,y, dx=1, dy=0):
        print (f"find next on {x} {y}")
        nx = x
        ny = y

        current = self.grid[y][x] 

        while True:
            lx = nx
            ly = ny
            nx = nx+dx
            ny = ny+dy
            print(f"last {lx},{ly} try {nx},{ny} current {current}")
            try:
                if nx<0 or ny<0: raise IndexError()
                possible = self.grid[ny][nx]
                print(f"possible found {possible} with {nx}{ny}")
            except:
                print(f"exception {lx} {ly} being set")
                self.grid[y][x]  =0 
                self.grid[ly][lx] = current
                return

            if possible==0:
                print(f"zero found")
                continue
            elif possible==current:
                print(f"match found")
                self.grid[y][x]  =0 
                self.grid[ny][nx] += current
                return
            else:
                print("blockage")
                self.grid[y][x]  =0 
                self.grid[ly][lx] = current
                return


    
    def sweep(self,dx,dy):
        print(f"sweep {dx} {dy}")
        if dx==1:
            sx = self.w-1 
            ex = -1
            sy = 0
            ey = self.h
            ddx = -1
            ddy = 1
        elif dx==-1:
            sx = 0
            ex = self.w
            sy = 0
            ey = self.h
            ddx = 1
            ddy = 1
        elif dy==1:
            sx = 0
            ex = self.w
            sy = self.h-1
            ey = -1
            ddx = 1
            ddy = -1
        elif dy==-1:
            sx = 0
            ex = self.w
            sy = 0
            ey = self.h
            ddx = 1
            ddy = 1
            #start right to left
            #  top to bottom
        for yy in range(sy, ey, ddy):
            for xx in range(sx,ex ,ddx):
                if self.grid[yy][xx]>0:
                    self.what_next(xx,yy,dx,dy)
                        
     
       
        self.add_number()

    def add_number(self):
        loop = self.w*self.h
        target = None
        while target is None:
            loop -=1
            import random
            x,y = random.randint(0,self.w-1), random.randint(0,self.h-1)
            target = self.grid[y][x]
            if target!=0: target=None
            if loop==0:
                print("no holes")
                return
        self.grid[y][x] = 2
        print (f"add new to {x} {y}")
        return x,y  

    def draw(self):
        #print("draw")
        pg.draw.rect(self.screen, Colours.darkBlue, pg.Rect(0,0,self.ww,self.wh))
        for row in range(len(self.grid)):
                for column in range(len(self.grid[row])):
                    px, py = column*(self.cw+2)+self.ox, row*(self.ch+2)+self.oy
                    pg.draw.rect(self.screen, Colours.white, pg.Rect(px,py,self.cw,self.ch), 1)
                    cell = self.grid[row][column]
                    if cell>0:
                        number_colour = Colours.yellow
                        text_surface = self.my_font.render(str(cell), False, number_colour)
                        self.screen.blit(text_surface, (px+self.cw/2-text_surface.get_width()/2,py+self.ch/2-text_surface.get_height()/2))


    def gogo(self):
        print('gogo')
        pg.init()
        self.screen = pg.display.set_mode([self.ww,self.wh])
        while self.get_working():
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.working = False
                if event.type == pg.KEYDOWN:
                    print(event.key)
                    if event.key==1073741903:
                        # right
                        self.sweep(1,0)
                    if event.key==1073741904:
                        # left
                        self.sweep(-1,0)
                    if event.key==1073741905:
                        # down
                        self.sweep(0,1)
                    if event.key==1073741906:
                        # up
                        self.sweep(0,-1)
                    if event.key==99:
                        self.init()

            self.draw()

            self.clock.tick(40)
            pg.display.flip()
        
        pg.display.quit()
        
        return

if __name__=='__main__':
    print('boo')
    g=Gogo()




