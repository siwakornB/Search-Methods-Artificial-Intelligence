#import necessary lib
import pygame
import os 
import random
import time
#import puzzel generetor
from word_search_puzzle.utils import display_panel
from word_search_puzzle.algorithms import create_panel
#for memory tracer
import tracemalloc

pygame.font.init()
myfont = pygame.font.SysFont("comicsans",40)


BLACK = (0, 0, 0)
WHITE = (200, 200, 200)

start_status = 0
reset_status = 0
InputBox_status = 0

WIDTH,HEIGHT = 1000,800
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Test")

blockSize = 80 #Set the size of the grid block
table = [['C','O','N','N','E','C','T','I','O','N'],
            ['F','C','E','L','L','P','H','O','N','E'],
            ['A','R','Z','T','S','P','E','E','C','H'],
            ['C','B','T','M','A','L','U','J','G','G'],
            ['I','A','L','I','F','I','U','G','B','I'],
            ['A','S','E','N','I','H','C','A','M','P'],
            ['L','L','H','P','B','E','J','O','S','H'],
            ['K','R','G','R','J','S','I','R','I','O'],
            ['M','G','Z','D','E','E','P','S','M','N'],
            ['D','I','N','T','E','R','N','E','T','E'] ]
            'IPHONE','SIRI','CELLPHONE',]#'MACHINES','SPEED'
words = WORDS.copy()               
WORDS = ['AI','FACIAL','SPEECH','CONNECTION','INTERNET',
visited = []

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
        self.CurrentMem = 0
        self.PeakMem = 0
        self.Timeconsumption = 0
    
    def nextRoot(self):
        if(self.rooty < 9):
            self.rooty += 1
        elif(self.rootx < 9):
            self.rooty = 0
            self.rootx += 1
        else:
            self.run = False
            
        #print('Root' + ':' + table[self.rootx][self.rooty])
        self.redraw()

    def search(self):
        #print('x =',self.x,'y = ',self.y,'dir = ',self.dir)
        if(self.x >= 0 and self.x <= 9):
            if (self.y >= 0 and self.y <= 9):
                #print(self.directory[self.dir] + ':' + table[self.x][self.y])
                self.string = self.string + table[self.x][self.y]
                #print(self.string)
                self.redraw()
                if self.string in words:
                    print("------------------------------------------------------")
                    self.path.append(self.string)
                    words.remove(self.string)
                    visited.append(self.string)
                    print(visited)
                    self.dir += 1 
                    if(self.dir > 3):
                        self.dir = 0
                        self.nextRoot()
                    self.x,self.y = self.rootx,self.rooty
                    self.string = ''
                    if(len(words) <= 0):
                        self.run = False
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
                if(self.dir > 3):
                    self.dir = 0
                    self.nextRoot()
                self.x,self.y = self.rootx,self.rooty
                self.string = ''
        else:
            self.dir += 1
            if(self.dir > 3):
                    self.dir = 0
                    self.nextRoot()
            self.x,self.y = self.rootx,self.rooty
            self.string = ''

    def circle(self):
        pygame.draw.circle(SCREEN, (0,0,255), (self.rooty*blockSize+blockSize//4+2,self.rootx*blockSize+blockSize//4+5), blockSize//4,2)
        pygame.draw.circle(SCREEN, (0,255,0), (self.y*blockSize+blockSize//4+2,self.x*blockSize+blockSize//4+5), blockSize//4,2)
  
    def redraw(self):
        SCREEN.fill(BLACK)
        drawGrid()
        start_button = pygame.Rect(800, 200, 200, 100)
        reset_button = pygame.Rect(800, 600, 200, 100)

        pygame.draw.rect(SCREEN, (255, 255, 0), start_button)
        pygame.draw.rect(SCREEN, (255,0,0), reset_button)
        self.circle()

        pygame.display.update()

def main():
    global start_status
    global reset_status
    global words
    global WORDS
    global myfont
    global InputBox_status

    FPS = 60
    CLOCK = pygame.time.Clock()
    timer = pygame.time.get_ticks()

    #define button
    start_button = pygame.Rect(800, 200, 200, 100)
    reset_button = pygame.Rect(800, 600, 200, 100)

    #define input box
    input_box = pygame.Rect(800, 400, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    #--------------

    dfs = DFS()
    GAME = True
    global globalCurrentMem, globalPeakMem,Timeconsumption
    globalPeakMem = 0
    avg = []

    starttime = pygame.time.get_ticks()
    tracemalloc.start()
    while GAME:
        CLOCK.tick(FPS)
        t = pygame.time.get_ticks() - timer
        #print(t)

        if(dfs.run):
            dfs.search()
            timer = pygame.time.get_ticks()
            CurrentMem, PeakMem = tracemalloc.get_traced_memory()
            if(len(avg) <= 80):
                avg.append(CurrentMem)
            else:
                avg.pop(0)
                avg.append(CurrentMem)
            if(PeakMem > dfs.PeakMem):
                dfs.PeakMem = PeakMem
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:          #button click
                if event.button == 1:                           #1 is the left mouse button, 2 is middle, 3 is right.
                    if start_button.collidepoint(event.pos):
                        print("-------------------------------------------------------------------")
                        start_status = 1
                        InputBox_status = 1
                    if reset_button.collidepoint(event.pos):
                        print("-------------------------------------------------------------------")
                        SCREEN.fill(BLACK)
                        start_status = 0
                        words = WORDS.copy()
                        visited.clear()
                        InputBox_status = 0
                        main()
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
            elif event.type == pygame.KEYDOWN:
                if InputBox_status == 0:
                    if event.key == pygame.K_RETURN:
                        #print(text)
                        text = ''
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                        #print(text)
                        InputBox_status = 0
                    else:
                        text += event.unicode
                        #print(text)
        SCREEN.fill(BLACK)
        drawGrid()
        if(start_status == 1):
            if(dfs.run):
                dfs.search()  
                timer = pygame.time.get_ticks()
        pygame.draw.rect(SCREEN, (255, 255, 0), start_button)
        pygame.draw.rect(SCREEN, (255,0,0), reset_button)
        # print(text)
        if InputBox_status == 0:
            txt_surface = myfont.render(text, True, color)
        # Resize the box if the text is too long.
            width = max(200, txt_surface.get_width()+10)
            input_box.w = width
        # Blit the text.
            SCREEN.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect.
            pygame.draw.rect(SCREEN, color, input_box, 2)
        
        
        pygame.display.update()
                #pygame.quit()
                GAME = False
                dfs.Timeconsumption = (pygame.time.get_ticks() - starttime)/1000
                dfs.CurrentMem = sum(avg)/len(avg)
                print(f'mem : {dfs.CurrentMem} bytes peak : {dfs.PeakMem} bytes Total Time :{dfs.Timeconsumption} s')
    tracemalloc.stop()
    

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
    
main()
