import pygame as pg

class Grid:
    def __init__(self, width, height,blockSize):
        self.width = width
        self.height = height
        self.walls = []
        self.blockSize = blockSize
        self.connections = [(1, 0), (-1, 0), (0, 1), (0, -1)]

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

    def draw(self,SCREEN):
        for wall in self.walls:
            rect = pg.Rect((wall[0]*self.blockSize+self.blockSize,wall[1]*self.blockSize+self.blockSize),
             (self.blockSize, self.blockSize))
            pg.draw.rect(SCREEN, (200,200,200), rect)

            rect = pg.Rect((wall[0]*self.blockSize+self.blockSize+900,wall[1]*self.blockSize+self.blockSize),
             (self.blockSize, self.blockSize))
            pg.draw.rect(SCREEN, (200,200,200), rect)