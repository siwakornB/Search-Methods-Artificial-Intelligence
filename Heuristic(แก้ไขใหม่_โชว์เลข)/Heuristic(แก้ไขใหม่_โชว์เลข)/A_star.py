#import necessary lib
import pygame
from Grid import Node
from copy import deepcopy
import datetime
#for memory tracer
import tracemalloc
WIDTH,HEIGHT = 1350,500
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))


class A_Star:
    def __init__(self,start,goal,g):
        self.running = False  # initial with running state
        self.done = False #for tell whether search is done
        if start == None:
            self.start = Node([0,0])
        else:
            self.start = Node(start)
        self.goal_list = goal.copy()
        #print(self.goal_list)
        #self.g_temp = goal
        self.current_node = self.start
        # Create lists for open nodes and closed nodes
        self.open = []
        self.closed = []
        self.open.append(self.start)
        #for statistics

        stt = pygame.time.get_ticks()
        tracemalloc.start()
        self.astar_search(start,goal,g)
        CurrentMem, self.Peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        self.time_consumption = pygame.time.get_ticks() - stt
                
        self.g_temp = self.goal_list.copy()       
        self.goal = self.g_temp.pop(0)

    def search(self,g):
        # Loop until the open list is empty
        if len(self.open) > 0:
            # Sort the open list to get the node with the lowest cost first
            self.open.sort()
            # Get the node with the lowest cost
            self.current_node = self.open.pop(0)
            # Add the current node to the closed list
            self.closed.append(self.current_node)
            
            # Check if we have reached the goal, return the path
            #print(self.current_node.position,self.goal)
            if self.current_node.position == self.goal:
                #print('A_star done',self.goal)
                path = []
                backtraverse = deepcopy(self.current_node)
                while backtraverse.position != self.start.position:
                    path.append(backtraverse.position)
                    backtraverse = backtraverse.parent
                if len(self.g_temp) > 0:
                    self.goal = self.g_temp.pop(0)
                else:                                        
                    self.done = True
                    return 0
                self.open = []
                self.closed = []
                
            # Get neighbors
            neighbors = g.find_neighbors(self.current_node.position)
            # Loop neighbors
            for next in neighbors:
                # Create a neighbor node
                neighbor = Node(next, self.current_node)
                # Check if the neighbor is in the closed list
                if(neighbor in self.closed):
                    continue
                # Generate heuristics (Manhattan distance)
                neighbor.g = abs(neighbor.position[0] - self.start.position[0]) + abs(neighbor.position[1] - self.start.position[1])
                neighbor.h = abs(neighbor.position[0] - self.goal[0]) + abs(neighbor.position[1] - self.goal[1])
                neighbor.f = neighbor.g + neighbor.h
                # Check if neighbor is in open list and if it has a lower f value
                if self.check(neighbor):
                    # Everything is green, add neighbor to open list
                    self.open.append(neighbor)
        # Return None, no path is found
        #return None

    # A* search
    def astar_search(self,start, end,g):
        # Create lists for open nodes and closed nodes
        open = []
        closed = []
        # Create a start node and an goal node
        start_node = Node(start, None)
        goal_node = Node(end.pop(0), None)
        # Add the start node
        open.append(start_node)
        
        # Loop until the open list is empty
        while len(open) > 0:
            # Sort the open list to get the node with the lowest cost first
            open.sort()
            # Get the node with the lowest cost
            current_node = open.pop(0)
            # Add the current node to the closed list
            closed.append(current_node)
            
            # Check goal
            #print(closed)
            if current_node == goal_node:
                if len(end) > 0:
                    goal_node = Node(end.pop(0), None)
                else:
                    return 0                                        
                open = []
                closed = []
                            
            # Get neighbors
            neighbors = g.find_neighbors(current_node.position)
            # Loop neighbors
            for next in neighbors:
                neighbor = Node(next,current_node)
                # Check if the neighbor is in the closed list
                if(neighbor in closed):
                    continue
                # Generate heuristics (Manhattan distance)
                neighbor.g = abs(neighbor.position[0] - start_node.position[0]) + abs(neighbor.position[1] - start_node.position[1])
                neighbor.h = abs(neighbor.position[0] - goal_node.position[0]) + abs(neighbor.position[1] - goal_node.position[1])
                neighbor.f = neighbor.g + neighbor.h

                # Check if neighbor is in open list and if it has a lower f value
                if self.chc(neighbor,open):
                    open.append(neighbor)

    def chc(self, neighbor,open):
        for node in open:
            if (neighbor.position == node.position and neighbor.f >= node.f):
                return False
        return True
    def check(self, neighbor):
        for node in self.open:
            if (neighbor.position == node.position and neighbor.f >= node.f):
                return False
        return True

    def get_open(self):
        return [e.position for e in self.open]

    def get_closed(self):
        return [e.position for e in self.closed]

    def pause(self):
        self.running = not self.running

    def get_pos(self):
        return {'walk':[self.current_node.position],'goal':[self.goal]}

    def is_done(self):        
        return self.done

    def is_pause(self):
        return self.running

    def reset(self):
        self.running = False  # initial with running state
        self.done = False #for tell whether search is done
        self.g_temp = self.goal_list.copy()
        print(self.g_temp)
        self.goal = self.g_temp.pop(0)
        self.current_node = self.start
        # Create lists for open nodes and closed nodes
        self.open = []
        self.closed = []
        self.open.append(self.start)
        #for statistics
        self.time_consumption = 0
        self.max_mem = 0