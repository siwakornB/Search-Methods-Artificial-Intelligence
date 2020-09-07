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
SCREEN.fill(BLACK)
pygame.display.set_caption("Test")


def main():
    FPS = 60
    CLOCK = pygame.time.Clock()

    puzzle_gen()
    while True:
        CLOCK.tick(2)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

def drawGrid(arr):
    blockSize = 80 #Set the size of the grid block
    for x in range(5):
        for y in range(5):
            #rect = pygame.Rect(x*blockSize, y*blockSize,blockSize, blockSize)
            #pygame.draw.rect(SCREEN, WHITE, rect, 1)
            textsurface = myfont.render(arr[x][y], True, (255, 255, 255)) #text / Anti aliasing / color (in this case it's white)
            SCREEN.blit(textsurface,(x*blockSize+20,y*blockSize+20))

def puzzle_gen():
    words = ['cat', 'bear', 'tiger', 'lion']
    table = [['0' for i in range(5)] for i in range(5)]
    result = create_panel(height=5, width=5, words_value_list=words)
    position = ""

    display_panel(result.get('panel'))
    #convert into 2d array
    for i in range(0,5):
        for j in range(0, 5):
            table[i][j] = result.get('panel').cells[i,j]
    drawGrid(table)
    #initial search
    def BFS(PosX,PosY,string):
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
    for i in range(0,5):
        for j in range(0,5):
            print('Root:',i,j)
            BFS(i,j,"")

main()