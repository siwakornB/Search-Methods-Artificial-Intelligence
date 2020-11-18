import pygame as pg

class DFS:        #depth first search
    def __init__(self,start,goal):
        self.running = False  # initial with running state
        self.done = False #for tell whether search is done
        if start == None:
            self.start = [0,0]
        else:
            self.start = start
        self.goal_list = goal.copy()
        self.g_temp = goal
        self.goal = self.g_temp.pop(0)
        self.stack = [] #!!!so fucking necessary
        self.current = start
        self.path = [start]  #in case of trace a way
        self.visited = []

        self.time_consumption = 0
        self.max_mem = 0

    def se(self,g):    
        if self.current == self.goal:
            print('dfs done',self.goal)
            if len(self.g_temp) > 0:
                self.goal = self.g_temp.pop(0)
                self.visited = []
                self.path = []
            else:
                self.done = True
            # not finish
        if not self.done:
            for next in g.find_neighbors(self.current):
                if next not in self.visited:
                    self.stack.append(next)
                    self.visited.append(next)
        #next
        if len(self.stack) > 0:
            self.current = self.stack.pop()
            if not self.done:
                self.path.append(self.current)

    def search(self,g):    
        if self.current == self.goal:
            print('dfs done',self.goal)
            if len(self.g_temp) > 0:
                self.goal = self.g_temp.pop(0)
                self.visited = []
                self.path = []
            else:
                self.done = True
        if not self.done:
            for next in g.find_neighbors(self.current):
                if next not in self.visited:
                    self.stack.append(next)
                    self.visited.append(next)
        #next
        if len(self.stack) > 0:
            self.current = self.stack.pop()
            if not self.done:
                self.path.append(self.current)

    def pause(self):
        self.running = not self.running

    def get_pos(self):
        return {'walk':[self.current],'goal':[self.goal]}
    
    def get_visited(self):
        return self.visited

    def get_path(self):
        return self.path
    
    def is_done(self):
        return self.done

    def is_pause(self):
        return self.running

    def reset(self):
        self.running = False  # initial with running state
        self.done = False #for tell whether search is done
        self.g_temp = self.goal_list.copy()
        self.goal = self.g_temp.pop(0)
        self.stack = [] #!!!so fucking necessary
        self.current = self.start
        self.max_stack = 0
        self.path = [self.start]  #in case of highlighting word
        self.visited = []
        