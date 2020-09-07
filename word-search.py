#import necessary lib
import pygame
import os 
import random
import time
#import puzzel generetor
from word_search_puzzle.utils import display_panel
from word_search_puzzle.algorithms import create_panel

pygame.font.init()
myfont = pygame.font.SysFont("comicsans",40)


BLACK = (0, 0, 0)
WHITE = (200, 200, 200)


WIDTH,HEIGHT = 400,400
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Test")


blockSize = 80 #Set the size of the grid block
def redraw(PosX,PosY):    
    SCREEN.fill(BLACK)

    drawGrid()
    circle(PosX,PosY)

    pygame.display.update()

def main():
    FPS = 60
    CLOCK = pygame.time.Clock()

    puzzle_gen()


    while True:
        CLOCK.tick(FPS)
        s()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

def drawGrid():
    for x in range(5):
        for y in range(5):
            #rect = pygame.Rect(x*blockSize, y*blockSize,blockSize, blockSize)
            #pygame.draw.rect(SCREEN, WHITE, rect, 1)
            textsurface = myfont.render(table[x][y], True, (255, 255, 255)) #text / Anti aliasing / color (in this case it's white)
            SCREEN.blit(textsurface,(y*blockSize+30,x*blockSize+30))

def puzzle_gen():
    global words,table
    words = ['cat', 'bear', 'tiger', 'lion']
    table = [['0' for i in range(5)] for i in range(5)]
    result = create_panel(height=5, width=5, words_value_list=words)

    display_panel(result.get('panel'))
    #convert into 2d array
    for i in range(0,5):
        for j in range(0, 5):
            table[i][j] = result.get('panel').cells[i,j]

def circle(PosX,PosY):    
    #for i in range(0,5):
        #for j in range(0,5):            
            #screen.blit(my_image, another_position)
    pygame.draw.circle(SCREEN, (0,255,0), (PosY*blockSize+blockSize//2,PosX*blockSize+blockSize//2), blockSize//4,2)
            #print('Root:',i,j)
            #DFS(i,j,"")

def s():
    for i in range(0,5):
        for j in range(0, 5):
            print('Root:',i,j)
            DFS(i,j,"")

#initial search
def DFS(PosX,PosY,string):
    position = ""
    print("NorthEast: ", end="")
    search(PosX, PosY, string, 'NorthEast', position)
    print()
    print("East: ",end="")
    search(PosX,PosY,string,'East', position)
    print()
    print("SouthEast: ", end="")
    search(PosX,PosY,string,'SouthEast', position)
    print()
    print("South: ", end="")
    search(PosX,PosY,string,'South', position)
    print()
    
#recursion
def search(PosX,PosY,string,dir,position):
    if(PosX >= 0 and PosX <= 4):
        if (PosY >= 0 and PosY <= 4):
            #print(table[PosX][PosY], end=" ")
            string = string + table[PosX][PosY]
            print(string)
            redraw(PosX,PosY)
            time.sleep(0.5)
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