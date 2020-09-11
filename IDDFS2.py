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

position = ""

table = [['A', 'B', 'C', 'D', 'E'],
         ['F', 'G', 'H', 'I', 'J'],
         ['K', 'L', 'M', 'N', 'O'],
         ['P', 'Q', 'R', 'S', 'T'],
         ['U', 'V', 'W', 'X', 'Y']]
words = ['cat', 'bear', 'tiger', 'lion']

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

    result = create_panel(height=5, width=5, words_value_list=words)

    display_panel(result.get('panel'))
    #convert into 2d array


def circle(PosX,PosY):
    #for i in range(0,5):
        #for j in range(0,5):
            #screen.blit(my_image, another_position)
    pygame.draw.circle(SCREEN, (0,255,0), (PosY*blockSize+blockSize//2,PosX*blockSize+blockSize//2), blockSize//4,2)
            #print('Root:',i,j)
            #DFS(i,j,"")

def s():
    for level in range(1, 5):
        for row in range(0, 5):
            for column in range(0, 5):
                # print('___Root:',row,column)
                print('-------------------------------------------')
                print('level: ', level, ' row: ', row, ' column: ', column)
                print('4-min(row,column)', 4 - min(row, column))
                IDDFS(row, column, "", 0, min(level, 4 - min(row, column)))
                print('-------------------------------------------')

def IDDFS(row,column,string,tmp_round,last_round):

    if tmp_round < last_round:
        print('round: ', last_round)
        print("\n-NorthEast: ")
        IDDFSSearch(row, column, string, 'NorthEast', tmp_round, last_round)
        print("\n-East: ")
        IDDFSSearch(row, column, string, 'East', tmp_round, last_round)
        print("\n-SouthEast: ")
        IDDFSSearch(row, column, string, 'SouthEast', tmp_round, last_round)
        print("\n-South: ")
        IDDFSSearch(row, column, string, 'South', tmp_round, last_round)
        print('----------')

def IDDFSSearch(row,column,string,dir,tmp_round,last_round):
    if(tmp_round <= last_round):
        if(row >= 0 and row <= 4):
            if (column >= 0 and column <= 4):
                print(table[row][column], end=" ")
                #string = string + table[row][column]    #Stack
                #print(string)
                #redraw(row, column)
                #time.sleep(0.5)
                # print(tmp_round,last_round,end = " ")
                # print(row,column,end = "\n")
                if string in words:                     #หาว่า string(stack)ที่ได้จากการ Search ตรงกับคำที่อยู่ใน list หรือไม่
                    global position
                    if string not in position:          #ใช้ในการเลือก Save ประโยคที่่ไม่ซ้ำกับประโยคที่มีอยู่แล้ว
                        if(dir == 'NorthEast'):
                            position = position + string + " at " + str(row+len(string)-1) + ',' + str(column-len(string)+1) + ' direction: NorthEast' +'\n'
                        if(dir == 'East'):
                            position = position + string + " at " + str(row) + ',' + str(column - len(string) + 1) + ' direction: East' +'\n'
                        if(dir == 'South'):
                            position = position + string + " at " + str(row - len(string)+1) + ',' + str(column) + ' direction: South' +'\n'
                        if (dir == 'SouthEast'):
                            position = position + string + " at " + str(row - len(string) + 1) + ',' + str(column - len(string) + 1) + ' direction: SouthEast' +'\n'
                if(dir == 'NorthEast'):
                    IDDFSSearch(row-1, column+1, string, dir ,tmp_round+1,last_round)
                if (dir == 'East'):
                    IDDFSSearch(row, column+1, string, dir,tmp_round+1,last_round)
                if (dir == 'South'):
                    IDDFSSearch(row+1, column, string, dir,tmp_round+1,last_round)
                if (dir == 'SouthEast'):
                    IDDFSSearch(row + 1, column+1, string, dir,tmp_round+1,last_round)
for level in range(1,5):
    for row in range(0,5):
        for column in range(0,5):
            #print('___Root:',row,column)
            print('-------------------------------------------')
            print('level: ',level,' row: ',row,' column: ',column)
            print('4-min(row,column)',4-min(row,column))
            IDDFS(row,column,"",0,min(level,4-min(row,column)))
            print('-------------------------------------------')
# print(position)