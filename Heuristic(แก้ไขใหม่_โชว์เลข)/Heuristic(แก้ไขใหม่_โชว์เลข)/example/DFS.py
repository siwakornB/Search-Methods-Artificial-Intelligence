import pygame as pg
from os import path
from collections import deque
vec = pg.math.Vector2

TILESIZE = 20
GRIDWIDTH = 20
GRIDHEIGHT = 20
WIDTH = TILESIZE * GRIDWIDTH
HEIGHT = TILESIZE * GRIDHEIGHT
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
DARKGRAY = (40, 40, 40)
LIGHTGRAY = (90, 90, 90)

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
        self.connections = [vec(1, 0), vec(-1, 0), vec(0, 1), vec(0, -1)]

    def in_bounds(self, node):
        return 0 <= node.x < self.width and 0 <= node.y < self.height

    def passable(self, node):
        return node not in self.walls

    def find_neighbors(self, node):
        neighbors = [node + connection for connection in self.connections]
        if (node.x + node.y) % 2:
            neighbors.reverse()
        neighbors = filter(self.in_bounds, neighbors)
        neighbors = filter(self.passable, neighbors)
        return neighbors

    def draw(self):
        for wall in self.walls:
            print(wall)
            rect = pg.Rect(wall * TILESIZE, (TILESIZE, TILESIZE))
            pg.draw.rect(screen, LIGHTGRAY, rect)

def vec2int(v):
    return (int(v.x), int(v.y))

def draw_icons():
    start_center = (start.x * TILESIZE + TILESIZE / 2, start.y * TILESIZE + TILESIZE / 2)
    screen.blit(fireman_img, fireman_img.get_rect(center=start_center))
    goal_center = (goal.x * TILESIZE + TILESIZE / 2, goal.y * TILESIZE + TILESIZE / 2)
    screen.blit(fire_img, fire_img.get_rect(center=goal_center))

def draw_grid():
    for x in range(0, WIDTH, TILESIZE):
        pg.draw.line(screen, LIGHTGRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILESIZE):
        pg.draw.line(screen, LIGHTGRAY, (0, y), (WIDTH, y))

def timer():
    ticks=pg.time.get_ticks()
    millis=ticks%1000
    seconds=int(ticks/1000 % 60)
    minutes=int(ticks/60000 % 24)
    clock.tick(FPS)
    out='{minutes:02d}:{seconds:02d}:{millis}'.format(minutes=minutes, millis=millis, seconds=seconds)
    return out

'''
fireman_img = pg.image.load('fireman.png').convert_alpha()
fireman_img = pg.transform.scale(fireman_img, (20, 20))
fireman_img.fill((255, 255, 255, 255), special_flags=pg.BLEND_RGBA_MULT) 
fire_img = pg.image.load('fire.png').convert_alpha()
fire_img = pg.transform.scale(fire_img, (20, 20))
fire_img.fill((255, 0, 0, 255), special_flags=pg.BLEND_RGBA_MULT)
'''
g = Grid(GRIDWIDTH, GRIDHEIGHT)
walls = [(10, 7), (11, 7), (12, 7), (13, 7), (14, 7), (15, 7), (16, 7), (7, 7), (6, 7), (5, 7), (5, 5), (5, 6), (1, 6), (2, 6), (3, 6), (5, 10), (5, 11), (5, 12), (5, 9), (5, 8), (12, 8), (12, 9), (12, 10), (12, 11), (15, 14), (15, 13), (15, 12), (15, 11), (15, 10), (17, 7), (18, 7), (21, 7), (21, 6), (21, 5), (21, 4), (21, 3), (22, 5), (23, 5), (24, 5), (25, 5), (18, 10), (20, 10), (19, 10), (21, 10), (22, 10), (23, 10), (14, 4), (14, 5), (14, 6), (14, 0), (14, 1), (9, 2), (9, 1), (7, 3), (8, 3), (10, 3), (9, 3), (11, 3), (2, 5), (2, 4), (2, 3), (2, 2), (2, 0), (2, 1), (0, 11), (1, 11), (2, 11), (21, 2), (20, 11), (20, 12), (23, 13), (23, 14), (24, 10), (25, 10), (6, 12), (7, 12), (10, 12), (11, 12), (12, 12), (5, 3), (6, 3), (5, 4), (5, 16), (4, 16), (8, 16), (6, 16), (8, 18), (10, 17), (9, 17), (8, 17), (11, 17), (15, 18), (14, 17), (13, 17), (12, 17), (3, 16), (2, 16), (1, 16), (7, 14), (7, 15), (7, 16), (12, 15), (13, 15), (14, 15), (15, 15), (17, 2), (19, 2), (18, 2), (19, 15), (18, 14), (18, 15), (17, 15), (9, 10), (8, 10), (7, 10), (9, 5), (8, 5), (7, 5), (11, 1), (11, 0), (4, 0), (4, 1), (17, 4), (19, 5), (19, 4), (18, 4), (11, 5), (12, 5), (2, 7), (0, 14), (1, 14), (2, 14), (0, 12), (0, 13), (0, 18), (0, 19), (15, 17), (4, 17), (4, 18), (16, 8), (11, 9), (18, 16)]
for wall in walls:
    g.walls.append(vec(wall))

start = vec(0, 0)
G = [(19,19),(1,10)]
goal = G[0]
frontier = []
frontier.append(start)
visited = []
visited.append(start)
path = {}
path[vec2int(start)] = None
max = len(frontier)
paused = True
running = True
done = False


pg.display.set_caption("FireMan DFS") 
while running:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            if event.key == pg.K_SPACE:
                paused = not paused
            if event.key == pg.K_m:
                print([(int(loc.x), int(loc.y)) for loc in g.walls])
        if event.type == pg.MOUSEBUTTONDOWN:
            mpos = vec(pg.mouse.get_pos()) // TILESIZE
            if event.button == 1:
                if mpos in g.walls:
                    g.walls.remove(mpos)
                else:
                    g.walls.append(mpos)
    #for algoirithms
    if len(frontier) > 0 and not done :#and not paused and not done:
        pg.display.set_caption("Space = "+str(max)+"    "+timer()) 
        current = frontier.pop()
        if current == goal:
            print("Space = ",max)
            goal = G[1]
            #done = True
        for next in g.find_neighbors(current):
            if next not in visited:
                frontier.append(next)
                visited.append(next)
                path[vec2int(next)] = current - next
                if max < len(frontier):
                    max = len(frontier)
                      
    if len(frontier) == 0:
        done = True
    #for drawing
    screen.fill(DARKGRAY)
    draw_grid()
    g.draw()
    for loc in visited:
        x, y = loc
        r = pg.Rect(x * TILESIZE + 3, y * TILESIZE + 3, TILESIZE - 3, TILESIZE - 3)
        pg.draw.rect(screen, (71, 130, 109), r)
    if len(frontier) > 0:
        for n in frontier:
            r = pg.Rect(n.x * TILESIZE + 3, n.y * TILESIZE + 3, TILESIZE - 3, TILESIZE - 3)
            pg.draw.rect(screen, RED, r)
    if done:
        current = goal
        while current != start:
            r = pg.Rect(current.x * TILESIZE + 9, current.y * TILESIZE + 9, TILESIZE - 14, TILESIZE - 14)
            pg.draw.rect(screen, YELLOW, r)
            current = current + path[vec2int(current)]
    #draw_icons()
    pg.display.flip()
  
    
