#import necessary lib
import pygame as pg

pg.init()
#for memory tracer
import tracemalloc

from Dfs import DFS
#for maze_gen
#from maze_generator import*
from Grid import *
from A_star import A_Star

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0,0,255)
DARKGRAY = (40, 40, 40)
LIGHTGRAY = (90, 90, 90)
DIMWHITE = (200,200,200)


WIDTH,HEIGHT = 1366,768
SCREEN = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption("DFS vs A Star")
blockSize = 20
walls = [(10, 7), (11, 7), (12, 7), (13, 7), (14, 7), (15, 7), (16, 7), (7, 7), (6, 7), (5, 7), (5, 5),(5, 6), (1, 6),
     (2, 6), (3, 6), (5, 10), (5, 11), (5, 12), (5, 9), (5, 8), (12, 8),(12, 9), (12, 10), (12, 11), (15, 14), (15, 13), (15, 12),
       (15, 11), (15, 10), (17, 7), (18, 7),(18, 10),  (19, 10), (14, 4), (14, 5), (14, 6), (14, 0), (14, 1), (9, 2),
           (9, 1), (7, 3), (8, 3), (10, 3), (9, 3), (11, 3), (2, 5), (2, 4), (2, 3), (2, 2), (2, 0), (2, 1), (0, 11),
            (1, 11), (2, 11), (6, 12), (7, 12),(10, 12), (11, 12), (12, 12), (5, 3), 
            (6, 3), (5, 4), (5, 16), (4, 16), (8, 16), (6, 16), (8, 18), (10, 17),
              (9, 17), (8, 17), (11, 17), (15, 18), (14, 17), (13, 17), (12, 17), (3, 16), (2, 16), (1, 16), (7, 14),
               (7, 15), (7, 16), (12, 15), (13, 15), (14, 15), (15, 15), (17, 2), (19, 2), (18, 2), (19, 15), (18, 14),
                (18, 15), (17, 15), (9, 10), (8, 10), (7, 10), (9, 5), (8, 5), (7, 5), (11, 1), (11, 0), (4, 0), (4, 1),
                 (17, 4), (19, 5), (19, 4), (18, 4), (11, 5), (12, 5), (2, 7), (0, 14), (1, 14), (2, 14), (0, 12), (0, 13),
                  (0, 18), (0, 19), (15, 17), (4, 17), (4, 18), (16, 8), (11, 9), (18, 16)]

#pg.font.init()
myfont = pg.font.SysFont("comicsans",40)
litfont = pg.font.SysFont("comicsansms",30)

def main():
    #in-game config
    GAME = True
    FPS = 600
    CLOCK = pg.time.Clock()

    #define button
    BState = 'START'
    StartResetButton = pg.Rect((WIDTH*2//7)+250, HEIGHT//5, 110, 50)
    StartResetButton_status = True
    grid = Grid(20, 20,blockSize)
    
    grid.walls = walls.copy()

    def draw():
        SCREEN.fill(BLACK)
            
        #pg.draw.rect(Surface, color, Rect(x,y,w,h), thickness=0)
        #maze map
        for x in range(20):
            for y in range(20):
                pg.draw.rect(SCREEN,LIGHTGRAY,(y*blockSize+blockSize,x*blockSize+blockSize,blockSize,blockSize),1)
                pg.draw.rect(SCREEN,LIGHTGRAY,(y*blockSize+blockSize+900,x*blockSize+blockSize,blockSize,blockSize),1)
        pg.draw.rect(SCREEN, DIMWHITE,(blockSize, blockSize,20*blockSize,20*blockSize), 4)
        pg.draw.rect(SCREEN, DIMWHITE,(blockSize+900, blockSize,20*blockSize,20*blockSize), 4)
        #visited
        for v in dfs.get_visited():
            rect = pg.Rect((v[0]*blockSize+blockSize+2,v[1]*blockSize+blockSize+2),
                    (blockSize-4, blockSize-4))
            pg.draw.rect(SCREEN, LIGHTGRAY, rect)
        for v in a_s.get_closed():
            #print(v)
            rect = pg.Rect((v[0]*blockSize+blockSize+902,v[1]*blockSize+blockSize+2),
                    (blockSize-4, blockSize-4))
            pg.draw.rect(SCREEN, LIGHTGRAY, rect)
        #path
        for i,p in enumerate(dfs.get_path()[-10:]):
            rect = pg.Rect((p[0]*blockSize+blockSize+5+(7-i),p[1]*blockSize+blockSize+5+(7-i)),
                    (blockSize-10-(8-i),blockSize-10-(8-i)))
            pg.draw.rect(SCREEN, GREEN, rect)
        
        #for walker
        pos_list=dfs.get_pos()
        for key in pos_list:
            if key == 'walk':
                color = BLUE
            else:
                color = RED
            for pos in pos_list[key]:
                rect = pg.Rect((pos[0]*blockSize+blockSize+2,pos[1]*blockSize+blockSize+2),
                    (blockSize-4, blockSize-4))
                pg.draw.rect(SCREEN, color, rect)
        pos_list=a_s.get_pos()
        for key in pos_list:
            if key == 'walk':
                color = BLUE
            else:
                color = RED
            for pos in pos_list[key]:
                rect = pg.Rect((pos[0]*blockSize+blockSize+902,pos[1]*blockSize+blockSize+2),
                    (blockSize-4, blockSize-4))
                pg.draw.rect(SCREEN, color, rect)
        
        #game button
        pg.draw.rect(SCREEN, (255, 255, 0), StartResetButton)
        SCREEN.blit(litfont.render(BState, True, (255,0,0)), StartResetButton)
        
        grid.draw(SCREEN)
        pg.display.update()
    
        
    #####################################################
    start = [0,0]
    goal = [[19,19],[10,10],[3,2]]
    dfs = DFS(start,goal,grid)
    a_s = A_Star(start,goal,grid)
    timer = pg.time.get_ticks()
    timer2 = pg.time.get_ticks()
    while GAME:
        CLOCK.tick(FPS)
        t1 = pg.time.get_ticks() - timer
        t2 = pg.time.get_ticks() - timer2
        if t1 > 10 and not dfs.is_done() and dfs.is_pause():
            timer = pg.time.get_ticks()
            dfs.search(grid)
        if t2 > 10 and not a_s.is_done() and a_s.is_pause():
            timer2 = pg.time.get_ticks()
            a_s.search(grid)
        draw()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                #pg.quit()
                GAME = False
            elif event.type == pg.MOUSEBUTTONDOWN:          #button click
                if event.button == 1:                           #1 is the left mouse button, 2 is middle, 3 is right
                    if StartResetButton.collidepoint(event.pos):
                        if StartResetButton_status:
                            print("------------------------START----------------------------")
                            StartResetButton_status = not StartResetButton_status
                            BState = 'RESET'
                            dfs.pause()
                            a_s.pause()
                        else:
                            print("------------------------RESET----------------------------")
                            StartResetButton_status = not StartResetButton_status
                            BState = 'START'
                            dfs.reset()
                            a_s.reset()
                    
                    #color = color_active if active else color_inactive
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    dfs.pause()
                    a_s.pause()


def test():
    a,b = Node([0,0]),Node([0,0])
    print(a.position == b.position)



main()