#import necessary lib
import pygame
import os 
import random
import time
#import puzzel generetor
from word_search_puzzle.utils import display_panel
from word_search_puzzle.algorithms import create_panel

pygame.font.init()
myfont = pygame.font.SysFont("comicsans",30)


BLACK = (0, 0, 0)
WHITE = (200, 200, 200)


WIDTH,HEIGHT = 800,800
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Test")

blockSize = 80 #Set the size of the grid block

class DFS():
    def __init__(self):
        self.run = True #initial with running state
        self.rootx = 0 #just for keeping root
        self.rooty = 0
        self.x = 0  #for keeping recent search
        self.y = 0
        self.string = ''
        self.dir = 0 #0-3 for directory
        self.directory = ['NorthEast','East','SouthEast','South']
        self.path = []  #in case of highlighting word
    
    def nextRoot(self):
        if(self.y < 9):
            self.rooty += 1
        elif(self.x < 9):
            self.rooty = 0
            self.rootx += 1
        else:
            self.run = False
        print('Root' + ':' + table[self.rootx][self.rooty])

    def search(self):
        print('x =',self.x,'y = ',self.y,'dir = ',self.dir)
        self.redraw()
        if(self.x >= 0 and self.x <= 9):
            if (self.y >= 0 and self.y <= 9):
                print(self.directory[self.dir] + ':' + table[self.x][self.y])
                self.string = self.string + table[self.x][self.y]
                print(self.string)
                if self.string in words:
                    print("------------------------------------------------------")
                    self.path.append(self.string)
                if (self.dir == 0):
                    #search(PosX-1, PosY+1, string, dir, position)
                    self.x,self.y =  self.x-1,self.y+1
                elif (self.dir == 1):
                    #search(PosX, PosY+1, string, dir, position)
                    self.y =  self.y+1
                elif (self.dir == 2):
                    #search(PosX+1, PosY, string, dir, position)
                    self.x,self.y =  self.x+1,self.y+1
                elif (self.dir == 3):
                    #search(PosX + 1, PosY+1, string, dir, position)
                    self.x =  self.x+1
            else:
                self.dir += 1
                self.x,self.y = self.rootx,self.rooty
                self.string = ''
        else:
            self.dir += 1
            self.x,self.y = self.rootx,self.rooty
            self.string = ''
        if(self.dir > 3):
            self.dir = 0
            self.nextRoot()

    def circle(self):
        pygame.draw.circle(SCREEN, (0,255,0), (self.y*blockSize+blockSize//4,self.x*blockSize+blockSize//4+5), blockSize//4,2)

    
    def redraw(self):
        SCREEN.fill(BLACK)
        drawGrid()
        self.circle()

        pygame.display.update()

def main():
    FPS = 60
    CLOCK = pygame.time.Clock()
    timer = pygame.time.get_ticks()

    puzzle_gen()
    dfs = DFS()

    while True:
        CLOCK.tick(FPS)
        t = pygame.time.get_ticks() - timer
        #print(t)
        if( t > 300):
            dfs.search()
            timer = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

def drawGrid():
    for x in range(10):
        for y in range(10):
            #rect = pygame.Rect(x*blockSize, y*blockSize,blockSize, blockSize)
            #pygame.draw.rect(SCREEN, WHITE, rect, 1)
            textsurface = myfont.render(table[x][y], True, (255, 255, 255)) #text / Anti aliasing / color (in this case it's white)
            SCREEN.blit(textsurface,(y*blockSize+15,x*blockSize+15))

def puzzle_gen():
    global words,table
    words = ['cat', 'bear', 'tiger', 'lion']
    table = [['0' for i in range(10)] for i in range(10)]
    result = create_panel(height=10, width=10, words_value_list=words)

    display_panel(result.get('panel'))
    #convert into 2d array
    for i in range(0,10):
        for j in range(0, 10):
            table[i][j] = result.get('panel').cells[i,j]
    


def s():
    for i in range(0,5):
        for j in range(0, 5):
            print('Root:',i,j)
            DFS(i,j,"")

#initial search
def DFStt(PosX,PosY,string):
    position = ""
    print("NorthEast: ", end="")
    #search(PosX, PosY, string, 'NorthEast', position)
    state.append(PosX, PosY, string, 'NorthEast', position)
    print()
    print("East: ",end="")
    #search(PosX,PosY,string,'East', position)
    print()
    print("SouthEast: ", end="")
    #search(PosX,PosY,string,'SouthEast', position)
    print()
    print("South: ", end="")
    #search(PosX,PosY,string,'South', position)
    print()
    
#recursion
def searchtt(PosX,PosY,string,dir,position):
    if(PosX >= 0 and PosX <= 4):
        if (PosY >= 0 and PosY <= 4):
            #print(table[PosX][PosY], end=" ")
            string = string + table[PosX][PosY]
            print(string)
            redraw(PosX,PosY)
            if string in words:
                print("------------------------------------------------------")
            if (dir == 'NorthEast'):
                search(PosX-1, PosY+1, string, dir, position)
            if (dir == 'East'):
                search(PosX, PosY+1, string, dir, position)
            if (dir == 'South'):
                search(PosX+1, PosY, string, dir, position)
            if (dir == 'SouthEast'):
                search(PosX + 1, PosY+1, string, dir, position)

main()