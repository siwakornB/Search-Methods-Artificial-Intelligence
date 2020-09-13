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
level = 0
tmp = 0

table = [['A', 'B', 'C', 'D', 'E'],
         ['F', 'G', 'H', 'I', 'J'],
         ['K', 'L', 'M', 'N', 'O'],
         ['P', 'Q', 'R', 'S', 'T'],
         ['U', 'V', 'W', 'X', 'Y']]
words = ['AB', 'QR', 'NJ', 'TY']
test = [[0 for i in range(4)] for j in range(4)]
test2 = [[[0 for i in range(1)] for j in range(2)] for j in range(4)]
print(test)
print(test2)


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
    global level

    for level in range(0, 5):
        for row in range(0, 5):
            for column in range(0, 5):
                # print('___Root:',row,column)
                #print('-------------------------------------------')
                #print('level: ', level, ' row: ', row, ' column: ', column)
                #print('4-min(row,column)', 4 - min(row, column))
                IDDFS(row, column, "", 0, min(level, 4 - min(row, column)))
                #print('-------------------------------------------')
    print(position)
    print(test)

def IDDFS(row,column,string,tmp_round,last_round):
    #print('tmp_round: ', tmp_round,' last_round: ', last_round)
    #print('level: ', level, ' row: ', row, ' column: ', column)
    if ((column == 4 and row == 4) or (tmp_round == last_round)):       #access Last node and node which children node = 0
        #print(table[row][column], end=" ")
        # string = string + table[row][column]    #Stack
        # print(string)
        redraw(row, column)
        time.sleep(0)

    if tmp_round < last_round:
        if(column !=4 and row != 0):
            #print("\n-NorthEast: ")
            IDDFSSearch(row, column, string, 'NorthEast', tmp_round, last_round)
        if(column != 4):
            #print("\n-East: ")
            IDDFSSearch(row, column, string, 'East', tmp_round, last_round)
        if (row!= 4 and column != 4):
            #print("\n-SouthEast: ")
            IDDFSSearch(row, column, string, 'SouthEast', tmp_round, last_round)
        if(row != 4):
            #print("\n-South: ")
            IDDFSSearch(row, column, string, 'South', tmp_round, last_round)
        #print('----------')

def IDDFSSearch(row,column,string,dir,tmp_round,last_round):
    #global position
    global test
    global tmp
    if(tmp_round <= last_round):
        if(row >= 0 and row <= 4):
            if (column >= 0 and column <= 4):
                #print(table[row][column], end=" ")
                string = string + table[row][column]    #Stack
                #print(string)
                redraw(row, column)
                time.sleep(0)
                # print(tmp_round,last_round,end = " ")
                # print(row,column,end = "\n")
                if string in words:                     #หาว่า string(stack)ที่ได้จากการ Search ตรงกับคำที่อยู่ใน list หรือไม่
                    #if string not in test:          #ใช้ในการเลือก Save ประโยคที่่ไม่ซ้ำกับประโยคที่มีอยู่แล้ว
                    if not any(string in s for s in test):
                        print(tmp)
                        test[tmp][0] = string
                        if(dir == 'NorthEast'):
                            #position = position + string + " at " + str(row+len(string)-1) + ',' + str(column-len(string)+1) + ' direction: NorthEast' +'\n'
                            test[tmp][1] = str(row+len(string)-1) + ',' + str(column-len(string)+1)
                        if(dir == 'East'):
                            #position = position + string + " at " + str(row) + ',' + str(column - len(string) + 1) + ' direction: East' +'\n'
                            test[tmp][1] = str(row) + ',' + str(column - len(string) + 1)
                        if(dir == 'South'):
                            #position = position + string + " at " + str(row - len(string)+1) + ',' + str(column) + ' direction: South' +'\n'
                            test[tmp][1] = str(row - len(string)+1) + ',' + str(column)
                        if (dir == 'SouthEast'):
                            #position = position + string + " at " + str(row - len(string) + 1) + ',' + str(column - len(string) + 1) + ' direction: SouthEast' +'\n'
                            test[tmp][1] = str(row - len(string) + 1) + ',' + str(column - len(string)+1)
                        test[tmp][2] = str(row) + ',' + str(column)
                        test[tmp][3] = dir
                        tmp+=1

                if(dir == 'NorthEast'):
                    IDDFSSearch(row-1, column+1, string, dir ,tmp_round+1,last_round)
                if (dir == 'East'):
                    IDDFSSearch(row, column+1, string, dir,tmp_round+1,last_round)
                if (dir == 'South'):
                    IDDFSSearch(row+1, column, string, dir,tmp_round+1,last_round)
                if (dir == 'SouthEast'):
                    IDDFSSearch(row + 1, column+1, string, dir,tmp_round+1,last_round)
# for level in range(0,5):
#     for row in range(0,5):
#         for column in range(0,5):
#             #print('___Root:',row,column)
#             print('-------------------------------------------')
#             #print('level: ',level,' row: ',row,' column: ',column)
#             print('4-min(row,column)',4-min(row,column))
#             IDDFS(row,column,"",0,min(level,4-min(row,column)))
#             print()
# print(position)
main()