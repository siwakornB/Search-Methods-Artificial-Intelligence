import pygame as pg

class Grid:
    walls = []
    def __init__(self, width, height,blockSize):
        self.width = width
        self.height = height
        self.blockSize = blockSize

    def in_bounds(self, node):
        return 0 <= node[0] < self.width and 0 <= node[1] < self.height

    def passable(self, node):
        return tuple(node) not in self.walls

    def find_neighbors(self, node):
        #up,right,left,down
        neighbors = [[node[0],node[1]-1],
        [node[0]+1,node[1]],
        [node[0]-1,node[1]],
        [node[0],node[1]+1]]
        #print(neighbors)
        neighbors = filter(self.in_bounds, neighbors)
        neighbors = filter(self.passable, neighbors)
        #print(neighbors,node)
        return neighbors 

    def draw(self,SCREEN):
        for wall in self.walls:
            rect = pg.Rect((wall[0]*self.blockSize+self.blockSize,wall[1]*self.blockSize+self.blockSize),
             (self.blockSize, self.blockSize))
            pg.draw.rect(SCREEN, (200,200,200), rect)

            rect = pg.Rect((wall[0]*self.blockSize+self.blockSize+900,wall[1]*self.blockSize+self.blockSize),
             (self.blockSize, self.blockSize))
            pg.draw.rect(SCREEN, (200,200,200), rect)

class Node:
    def __init__(self,position,parent = None):
        self.position = position
        self.parent = parent
        self.g = 0 # Distance to start node
        self.h = 0 # Distance to goal node
        self.f = 0 # Total cost

    # Compare nodes
    def __eq__(self, other):
        return self.position == other.position
    # Sort nodes
    def __lt__(self, other):
         return self.f < other.f
    # Print node
    def __repr__(self):
        return ('({0},{1})'.format(self.position, self.f))