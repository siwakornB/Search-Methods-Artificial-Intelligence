#import necessary lib
import pygame
from Grid import Node

class A_Star:
    def __init__(self,start,goal):
        self.running = False  # initial with running state
        self.done = False #for tell whether search is done
        if start == None:
            self.start = Node([0,0])
        else:
            self.start = Node(start)
        self.goal_list = goal
        self.g_temp = goal
        self.goal = self.g_temp.pop(0)
        self.current_node = self.start
        #array
        
        # Create lists for open nodes and closed nodes
        self.open = []
        self.closed = []
        self.open.append(self.start)
        #for statistics
        self.time_consumption = 0
        self.max_mem = 0

    def search(self,g):
        # Loop until the open list is empty
        while len(open) > 0:
            # Sort the open list to get the node with the lowest cost first
            self.open.sort()
            # Get the node with the lowest cost
            self.current_node = self.open.pop(0)
            # Add the current node to the closed list
            self.closed.append(self.current_node)
            
            # Check if we have reached the goal, return the path
            if self.current_node.position == self.goal.position:
                path = []
                while self.current_node != self.start:
                    path.append(self.current_node.position)
                    self.current_node = self.current_node.parent
                # Return reversed path
                return path[::-1]
            # Get neighbors
            neighbors = g.find_neighbors(self.current_node)
            # Loop neighbors
            for next in neighbors:
                # Create a neighbor node
                neighbor = Node(next, self.current_node)
                # Check if the neighbor is in the closed list
                if(neighbor in self.closed):
                    continue
                # Generate heuristics (Manhattan distance)
                neighbor.g = abs(neighbor.position[0] - self.start.position[0]) + abs(neighbor.position[1] - self.start.position[1])
                neighbor.h = abs(neighbor.position[0] - self.goal.position[0]) + abs(neighbor.position[1] - self.goal.position[1])
                neighbor.f = neighbor.g + neighbor.h
                # Check if neighbor is in open list and if it has a lower f value
                if self.check(neighbor):
                    # Everything is green, add neighbor to open list
                    self.open.append(neighbor)
        # Return None, no path is found
        return None

    def check(self, neighbor):
        for node in self.open:
            if (neighbor.position == node.position and neighbor.f >= node.f):
                return False
        return True