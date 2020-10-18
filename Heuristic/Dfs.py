import pygame as pg
class DFS:        #depth first search
    def __init__(self,start,goal):
        self.running = False  # initial with running state
        self.done = False #for tell whether search is done
        self.current = None
        if start == None:
            self.start = [0,0]
        else:
            self.start = start
        self.goal_list = goal
        self.goal = self.goal_list.pop(0)
        self.stack = [] #!!!so fucking necessary
        self.stack.append(start)
        self.max_stack = 0
        self.directory = ['N','E','W','S']
        self.path = []  #in case of highlighting word
        self.visited = []

    def search(self,g):
        if len(self.stack) > 0:
            self.current = self.stack.pop()
        else:
            self.done = True
        if self.current == self.goal:
            if len(self.goal_list) > 0:
                self.goal = self.goal_list.pop(0)
            else:
                self.done = True
            # not finish
        for next in g.find_neighbors(self.current):
            if next not in self.visited:
                self.stack.append(next)
                self.visited.append(next)
                self.path.append(next) #not fin
                if self.max_stack < len(self.stack):
                    self.max_stack = len(self.stack)