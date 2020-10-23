import pygame as pg

class DFS:        #depth first search
    def __init__(self,start,goal):
        self.running = False  # initial with running state
        self.done = False #for tell whether search is done
        if start == None:
            self.start = [0,0]
        else:
            self.start = start
        self.goal_list = goal
        self.goal = self.goal_list.pop(0)
        self.stack = [] #!!!so fucking necessary
        self.current = start
        self.max_stack = 0
        self.path = [start]  #in case of highlighting word
        self.visited = []

    def search(self,g):    
        if self.current == self.goal:
            print('done',self.goal)
            if len(self.goal_list) > 0:
                self.goal = self.goal_list.pop(0)
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
                    if self.max_stack < len(self.stack):
                        self.max_stack = len(self.stack)
        #next
        if len(self.stack) > 0:
            self.current = self.stack.pop()
            if not self.done:
                self.path.append(self.current)
    

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