#import necessary lib
import pygame
import os 
import random
import time
import datetime
#import puzzel generetor
from word_search_puzzle.utils import display_panel
from word_search_puzzle.algorithms import create_panel
#for memory tracer
import tracemalloc

pygame.font.init()
myfont = pygame.font.SysFont("comicsans",40)
litfont = pygame.font.SysFont("comicsans",30)


BLACK = (0, 0, 0)
WHITE = (200, 200, 200)

WIDTH,HEIGHT = 1366,768
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Words Search")

blockSize = 40  # Set the size of the grid block
table = [['C', 'O', 'N', 'N', 'E', 'C', 'T', 'I', 'O', 'N'],
         ['F', 'C', 'E', 'L', 'L', 'P', 'H', 'O', 'N', 'E'],
         ['A', 'R', 'Z', 'T', 'S', 'P', 'E', 'E', 'C', 'H'],
         ['C', 'B', 'T', 'M', 'A', 'L', 'U', 'J', 'G', 'G'],
         ['I', 'A', 'L', 'X', 'F', 'I', 'U', 'G', 'B', 'I'],
         ['A', 'S', 'E', 'N', 'I', 'H', 'C', 'A', 'M', 'P'],
         ['L', 'L', 'H', 'P', 'B', 'E', 'M', 'O', 'S', 'H'],
         ['K', 'L', 'G', 'R', 'J', 'S', 'I', 'R', 'I', 'O'],
         ['M', 'R', 'Z', 'D', 'E', 'E', 'P', 'S', 'M', 'N'],
         ['D', 'I', 'N', 'T', 'E', 'R', 'N', 'E', 'T', 'E']]

WORDS = ['AI', 'FACIAL', 'SPEECH', 'CONNECTION', 'INTERNET',
         'IPHONE', 'SIRI', 'CELLPHONE','ML' ]  # 'MACHINES','SPEED'
WORDSs = ['AI','ML']
words = WORDS.copy()
visited = []
class Timer:
    def __init__(self):
        self.accumulated_time = 0
        self.start_time = pygame.time.get_ticks()
        self.running = False

    def pause(self):
        self.running = False
        self.accumulated_time += pygame.time.get_ticks() - self.start_time

    def start(self):
        self.running = True
        self.start_time = pygame.time.get_ticks()

    def get(self):
        if self.running:
            return (self.accumulated_time +
                    (pygame.time.get_ticks() - self.start_time))
        else:
            return self.accumulated_time


class DFS():        #depth first search
    def __init__(self):
        self.run = False  # initial with running state
        self.rootrow = 0  # just for keeping root
        self.rootcol = 0
        self.row = 0  # for keeping recent search
        self.column = 0
        self.string = ''
        self.dir = 0 #0-3 for directory
        self.directory = ['NorthEast','East','SouthEast','South']
        self.path = []  #in case of highlighting word
        self.CurrentMem = 0
        self.PeakMem = 0
        self.Timeconsumption = 0
        self.avg = []
        self.words = WORDS.copy()
        self.visited = []

    def nextRoot(self):
        if (self.rootcol < 9):
            self.rootcol += 1
        elif (self.rootrow < 9):
            self.rootcol = 0
            self.rootrow += 1

        # print('Root' + ':' + table[self.rootrow][self.rootcol])

    def search(self):
        #print('x =',self.x,'y = ',self.y,'dir = ',self.dir)
        
        #print(self.directory[self.dir] + ':' + table[self.x][self.y])
        self.string = self.string + table[self.x][self.y]
        #print(self.string)
        if self.string in self.words:
            print("------------------------------------------------------")
            self.path.append(self.string)
            self.words.remove(self.string)
            #-------------------------
            visit_each = []
            visit_each.append(self.string)
            if (self.dir == 0):
                visit_each.append(str(self.column - len(self.string)+1) + ',' + str(self.row + len(self.string)-1))
            elif (self.dir == 1):
                visit_each.append(str(self.column - len(self.string) + 1) + ',' + str(self.row))
            elif (self.dir == 2):
                visit_each.append(str(self.column - 1) + ',' + str(self.row - len(self.string) + 1))
            elif (self.dir == 3):
                visit_each.append(str(self.column) + ',' + str(self.row - len(self.string) + 1))
            visit_each.append(str(self.column)+ ',' + str(self.row))
            visit_each.append(self.dir)
            self.visited.append(visit_each)
            #-------------------------
            print(self.visited)
            self.visit_each = ['' for i in range(4)]
            self.dir += 1
            if (self.dir > 3):
                self.dir = 0
                self.nextRoot()
            self.row, self.column = self.rootrow, self.rootcol
            self.string = ''
            if(len(self.words) <= 0):
                self.run = False
                print(f'mem : {self.CurrentMem} bytes peak : {self.PeakMem} bytes Total Time :{self.Timeconsumption} ms')
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
        if(self.x < 0 or self.x > 9) or (self.y < 0 or self.y > 9):
            self.dir += 1
            if(self.dir > 3):
                self.dir = 0
                self.nextRoot()
            self.row, self.column = self.rootrow, self.rootcol
            self.string = ''

    def draw(self):
        #draw search circle
        pygame.draw.circle(SCREEN, (0, 0, 255),
                           (self.rootcol * blockSize + blockSize // 2 + 2, self.rootrow * blockSize + blockSize // 2 + 5),
                           blockSize // 2, 2)
        pygame.draw.circle(SCREEN, (0, 255, 0),
                           (self.column * blockSize + blockSize // 2 + 2, self.row * blockSize + blockSize // 2 + 5),
                           blockSize // 2, 2)
        for index,vis in enumerate(self.visited):
            #print(index,vis)
            start_x,start_y = vis[1].split(',')
            end_x,end_y = vis[2].split(',')
            start_x = int(start_x)
            start_y = int(start_y)
            end_x = int(end_x)
            end_y = int(end_y)
            if (vis[3] == 0):
                
                while start_x <= end_x and start_y >= end_y :
                    #print(start_x, start_y)
                    pygame.draw.circle(SCREEN, (0, 255, 0),
                                       (start_x * blockSize + blockSize // 2 + 2,
                                        start_y * blockSize + blockSize // 2 + 5),
                                       blockSize // 2, 0)
                    start_x += 1
                    start_y -= 1
            if(vis[3] == 1):
                while start_x <= end_x :
                    #print(start_x, start_y)
                    pygame.draw.circle(SCREEN, (255, 255, 255),
                                   (start_x * blockSize + blockSize // 2 + 2,
                                    start_y * blockSize + blockSize // 2 + 5),
                                   blockSize // 2, 0)
                    start_x+=1
            if (vis[3] == 2):
                while start_x <= end_x and start_y <= end_y :
                    #print(start_x, start_y)
                    pygame.draw.circle(SCREEN, (0, 255, 0),
                                       (start_x * blockSize + blockSize // 2 + 2,
                                        start_y * blockSize + blockSize // 2 + 5),
                                       blockSize // 2, 0)
                    start_x += 1
                    start_y += 1
            if(vis[3] == 3):
                while start_y <= end_y :
                    #print(start_x, start_y)
                    pygame.draw.circle(SCREEN, (0, 255, 0),
                                   (start_x * blockSize + blockSize // 2 + 2,
                                    start_y * blockSize + blockSize // 2 + 5),
                                   blockSize // 2, 0)
                    start_y+=1

        txt = [f'mem : {self.CurrentMem} bytes',f'peak : {self.PeakMem} bytes',f'Total Time :{self.Timeconsumption} ms']
        stat1 = litfont.render(txt[0], True, WHITE)
        stat2 = litfont.render(txt[1], True, WHITE)
        stat3 = litfont.render(txt[2], True, WHITE)
        # Blit the text.
        SCREEN.blit(stat1, (50,500))
        SCREEN.blit(stat2, (50,530))
        SCREEN.blit(stat3, (50,560))
  
    def reset(self):
        self.run = False
        self.rootrow = 0
        self.rootcol = 0
        self.row = 0
        self.column = 0
        self.string = ''
        self.dir = 0
        self.path = []
        print(f'mem : {self.CurrentMem} bytes peak : {self.PeakMem} bytes Total Time :{self.Timeconsumption} ms')
        self.CurrentMem = 0
        self.PeakMem = 0
        self.Timeconsumption = 0
        self.avg.clear()
        
        self.words = WORDS.copy()
        self.visited.clear()
        global StartResetButton_status
        StartResetButton_status = False
        

class IDDFS():       #iterative deepening depth first search
    def __init__(self):
        self.run = False  # initial with running state
        self.rootrow = 0  # just for keeping root
        self.rootcol = 0
        self.row = 0  # column # for keeping recent search
        self.column = 0  # row
        self.string = ''
        self.dir = 0 #0-3 for directory
        self.directory = ['NorthEast','East','SouthEast','South']
        self.path = []  #in case of highlighting word
        self.CurrentMem = 0
        self.PeakMem = 0
        self.Timeconsumption = 0
        self.avg = []
        self.words = WORDS.copy()
        self.visited = []
        self.temp_level = 0
        self.max_level = 1
        
    def nextRoot(self):
        if (self.rootcol < 9):
            self.rootcol += 1
        elif (self.rootrow < 9):
            self.rootcol = 0
            self.rootrow += 1
        elif self.rootcol == 9 and self.rootrow == 9:
            self.max_level += 1
            self.temp_level = 0
            self.rootrow = 0  # just for keeping root
            self.rootcol = 0
            self.dir = 0  # 0-3 for directory
        else:
            self.run = False

        # print('Root' + ':' + table[self.rootrow][self.rootcol])

    def search(self):
        #print('temp',self.temp_level,'max',self.max_level)
        
        #print(self.directory[self.dir])
        self.string = self.string + table[self.x][self.y]
        #print(self.string)
        if self.string in self.words:
            print("------------------------------------------------------")
            self.path.append(self.string)
            self.words.remove(self.string)
            #-------------------------
            visit_each = []
            visit_each.append(self.string)
            if (self.dir == 0):
                visit_each.append(str(self.column - len(self.string)+1) + ',' + str(self.row + len(self.string)-1))
            elif (self.dir == 1):
                visit_each.append(str(self.column - len(self.string) + 1) + ',' + str(self.row))
            elif (self.dir == 2):
                visit_each.append(str(self.column - 1) + ',' + str(self.row - len(self.string) + 1))
            elif (self.dir == 3):
                visit_each.append(str(self.column) + ',' + str(self.row - len(self.string) + 1))
            visit_each.append(str(self.column)+ ',' + str(self.row))
            visit_each.append(self.dir)
            self.visited.append(visit_each)
            #-------------------------
            print(self.visited)
            self.dir += 1 
            if(self.dir > 3):
                self.dir = 0
                self.nextRoot()
            self.row, self.column = self.rootrow, self.rootcol
            self.string = ''
        if(len(self.words) <= 0):
            self.run = False
            print(f'mem : {self.CurrentMem} bytes peak : {self.PeakMem} bytes Total Time :{self.Timeconsumption} ms')
        if (self.dir == 0 ):
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
        self.temp_level += 1
        if(self.x < 0 or self.x > 9) or (self.y < 0 or self.y > 9) or (self.temp_level > self.max_level):
            self.temp_level = 0
            self.dir += 1
            if(self.dir > 3):
                self.dir = 0
                self.nextRoot()
            self.row, self.column = self.rootrow, self.rootcol
            self.string = ''

    def draw(self):
        pygame.draw.circle(SCREEN, (0, 0, 255),
                           (self.rootcol * blockSize + blockSize // 2 + 902, self.rootrow * blockSize + blockSize // 2 + 5),
                           blockSize // 2, 2)
        pygame.draw.circle(SCREEN, (0, 255, 0),
                           (self.column * blockSize + blockSize // 2 + 902, self.row * blockSize + blockSize // 2 + 5),
                           blockSize // 2, 2)

        for index,vis in enumerate(self.visited):
            #print(index,vis)
            start_x,start_y = vis[1].split(',')
            end_x,end_y = vis[2].split(',')
            start_x = int(start_x)
            start_y = int(start_y)
            end_x = int(end_x)
            end_y = int(end_y)
            if (vis[3] == 0):
                
                while start_x <= end_x and start_y >= end_y :
                    #print(start_x, start_y)
                    pygame.draw.circle(SCREEN, (0, 255, 0),
                                       (start_x * blockSize + blockSize // 2 + 902,
                                        start_y * blockSize + blockSize // 2 + 5),
                                       blockSize // 2, 0)
                    start_x += 1
                    start_y -= 1
            if(vis[3] == 1):
                while start_x <= end_x :
                    #print(start_x, start_y)
                    pygame.draw.circle(SCREEN, (255, 255, 255),
                                   (start_x * blockSize + blockSize // 2 + 902,
                                    start_y * blockSize + blockSize // 2 + 5),
                                   blockSize // 2, 0)
                    start_x+=1
            if (vis[3] == 2):
                while start_x <= end_x and start_y <= end_y :
                    #print(start_x, start_y)
                    pygame.draw.circle(SCREEN, (0, 255, 0),
                                       (start_x * blockSize + blockSize // 2 + 902,
                                        start_y * blockSize + blockSize // 2 + 5),
                                       blockSize // 2, 0)
                    start_x += 1
                    start_y += 1
            if(vis[3] == 3):
                while start_y <= end_y :
                    #print(start_x, start_y)
                    pygame.draw.circle(SCREEN, (0, 255, 0),
                                   (start_x * blockSize + blockSize // 2 + 902,
                                    start_y * blockSize + blockSize // 2 + 5),
                                   blockSize // 2, 0)
                    start_y+=1

        txt = [f'mem : {self.CurrentMem} bytes', f'peak : {self.PeakMem} bytes',
               f'Total Time :{self.Timeconsumption} ms']
        stat1 = litfont.render(txt[0], True, WHITE)
        stat2 = litfont.render(txt[1], True, WHITE)
        stat3 = litfont.render(txt[2], True, WHITE)
        # Blit the text.
        SCREEN.blit(stat1, (950,500))
        SCREEN.blit(stat2, (950,530))
        SCREEN.blit(stat3, (950,560))
  
    def reset(self):
        self.run = False
        self.rootrow = 0
        self.rootcol = 0
        self.row = 0
        self.column = 0
        self.string = ''
        self.dir = 0
        self.path = []
        print(f'mem : {self.CurrentMem} bytes peak : {self.PeakMem} bytes Total Time :{self.Timeconsumption} ms')
        self.CurrentMem = 0
        self.PeakMem = 0
        self.Timeconsumption = 0
        self.avg.clear()
        self.max_level = 1
        self.temp_level = 0
        
        self.words = WORDS.copy()
        self.visited.clear()
        global StartResetButton_status
        StartResetButton_status = False
        

def main():
    global StartResetButton_status,InputBox_status
    
    StartResetButton_status = True
    InputBox_status = True

    FPS = 60
    CLOCK = pygame.time.Clock()
    timer = pygame.time.get_ticks()
    timer2 = pygame.time.get_ticks()

    #define button
    StartResetButton = pygame.Rect((WIDTH*2/7)+200, HEIGHT*4/5, 100, 50)

    #define input box
    input_box = pygame.Rect((WIDTH*2/7)+400, (HEIGHT*4/5), 100, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    #--------------

    #define text 'Delay: '
    text_delay = myfont.render('Delay:', True, (255,255,0)) 
    textRect = text_delay.get_rect()  
    textRect.center = ((WIDTH*2/7)+350,HEIGHT*4/5+25) 

    dfs = DFS()
    iddfs = IDDFS()
    GAME = True
    
    def redraw():
        SCREEN.fill(BLACK)
        

        pygame.draw.rect(SCREEN, (255, 255, 0), StartResetButton)
        dfs.draw()
        iddfs.draw()

        if InputBox_status:
                txt_surface = myfont.render(text, True, color)
            # Resize the box if the text is too long.
                width = max(200, txt_surface.get_width()+10)
                input_box.w = width
            # Blit the text.
                SCREEN.blit(txt_surface, (input_box.x+5, input_box.y+5))
            # Blit the input_box rect.
            pygame.draw.rect(SCREEN, color, input_box, 2)
        drawGrid()
        pygame.display.update()
    
    
    while GAME:
        CLOCK.tick(FPS)
        t1 = pygame.time.get_ticks() - timer
        t2 = pygame.time.get_ticks() - timer2
        #DFS
        delay = 0
        if(t1 > delay and dfs.run):
            timer = pygame.time.get_ticks()
            
            tracemalloc.start()
            starttime1 = datetime.datetime.now()
            dfs.search()
            CurrentMem, PeakMem = tracemalloc.get_traced_memory()
            if(len(dfs.avg) <= 100):
                dfs.avg.append(CurrentMem)
            else:
                dfs.avg.pop(0)
                dfs.avg.append(CurrentMem)
            if(PeakMem > dfs.PeakMem):
                dfs.PeakMem = PeakMem
            dfs.CurrentMem = sum(dfs.avg)/len(dfs.avg)
            tim = (datetime.datetime.now() - starttime1)
            dfs.Timeconsumption += tim.microseconds/1000
            tracemalloc.stop()
            #------ IDDFS -----------
        if(t2 > delay and iddfs.run):
            timer2 = pygame.time.get_ticks()

            tracemalloc.start()
            starttime2 = datetime.datetime.now()
            iddfs.search()
            CurrentMem, PeakMem = tracemalloc.get_traced_memory()
            if(len(iddfs.avg) <= 100):
                iddfs.avg.append(CurrentMem)
            else:
                iddfs.avg.pop(0)
                iddfs.avg.append(CurrentMem)
            if(PeakMem > iddfs.PeakMem):
                iddfs.PeakMem = PeakMem
            iddfs.CurrentMem = sum(iddfs.avg)/len(iddfs.avg)
            tim2 = (datetime.datetime.now() - starttime2)
            iddfs.Timeconsumption += tim2.microseconds/1000
            tracemalloc.stop()
        redraw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #pygame.quit()
                GAME = False
            elif event.type == pygame.MOUSEBUTTONDOWN:          #button click
                if event.button == 1:                           #1 is the left mouse button, 2 is middle, 3 is right
                    if StartResetButton.collidepoint(event.pos):
                        if StartResetButton_status:
                            print("------------------------START----------------------------")
                            dfs.run = True
                            iddfs.run = True
                            InputBox_status = False
                            StartResetButton_status = not StartResetButton_status
                        else:
                            print("------------------------RESET----------------------------")
                            dfs.reset()
                            iddfs.reset()
                            InputBox_status = True
                            StartResetButton_status = not StartResetButton_status
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
            elif event.type == pygame.KEYDOWN:
                if InputBox_status:
                    if event.key == pygame.K_RETURN:
                        #print(text)
                        text = ''
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                        #print(text)
                    elif ord(event.unicode) > 0 and ord(event.unicode) <= 1000:
                        text += event.unicode

                        #print(text)
        


def drawGrid():
    for x in range(10):
        for y in range(10):
            textsurface = myfont.render(table[x][y], True, (255, 255, 255)) #text / Anti aliasing / color (in this case it's white)
            SCREEN.blit(textsurface,(y*blockSize+15,x*blockSize+15))

            SCREEN.blit(textsurface,(y*blockSize+15+900,x*blockSize+15))

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
