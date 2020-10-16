import pygame as pg
class DFS():        #depth first search
    def __init__(self,start = [0,0],goal):
        self.run = False  # initial with running state
        self.current = null
        self.goal_list = goal
        self.goal = goal_list.pop(0)
        self.stack = [] #!!!so fucking necessary
        self.stack.append(start)
        self.max_stack = 0
        self.directory = ['N','E','W','S']
        self.path = []  #in case of highlighting word
        self.visited = []

    def search(self,g):#not fin
        if len(self.stack) > 0:
            self.current = self.stack.pop()
        else:
            self.run = False
        if current == goal:
            self.goal = self.goal_list.pop(0)
            # not finish
        for next in g.find_neighbors(current):
            if next not in visited:
                self.stack.append(next)
                self.visited.append(next)
                self.path.append() #not fin
                if max < len(self.stack):
                    max = len(self.stack)