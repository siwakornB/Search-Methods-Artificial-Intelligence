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

    def search(self):
        # Loop until the open list is empty
        while len(open) > 0:
            # Sort the open list to get the node with the lowest cost first
            self.open.sort()
            # Get the node with the lowest cost
            self.current_node = self.open.pop(0)
            # Add the current node to the closed list
            self.closed.append(current_node)
            
            # Check if we have reached the goal, return the path
            if current_node == goal_node:
                path = []
                while current_node != start_node:
                    path.append(current_node.position)
                    current_node = current_node.parent
                #path.append(start) 
                # Return reversed path
                return path[::-1]
            # Unzip the current node position
            (x, y) = current_node.position
            # Get neighbors
            neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
            # Loop neighbors
            for next in neighbors:
                # Get value from map
                map_value = map.get(next)
                # Check if the node is a wall
                if(map_value == '#'):
                    continue
                # Create a neighbor node
                neighbor = Node(next, current_node)
                # Check if the neighbor is in the closed list
                if(neighbor in closed):
                    continue
                # Generate heuristics (Manhattan distance)
                neighbor.g = abs(neighbor.position[0] - start_node.position[0]) + abs(neighbor.position[1] - start_node.position[1])
                neighbor.h = abs(neighbor.position[0] - goal_node.position[0]) + abs(neighbor.position[1] - goal_node.position[1])
                neighbor.f = neighbor.g + neighbor.h
                # Check if neighbor is in open list and if it has a lower f value
                if(add_to_open(open, neighbor) == True):
                    # Everything is green, add neighbor to open list
                    open.append(neighbor)
        # Return None, no path is found
        return None