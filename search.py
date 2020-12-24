import numpy as np
from collections import deque
import heapq
import unittest
import math
import pygame


# using constants for colors 
SAND = (217, 168, 143) #for options background
CREAM = (249, 227, 203) #for grid
GRAY = (117, 112, 112)
BRICK = (176, 102, 96) #for obstacles
BLACK = (0, 0, 0) #for final path
BLUE = (174, 187, 199) #for searching path
PINK = (234, 195, 184) #for endpoints
WHITE = (255, 255, 255)

SCREEN_WIDTH = 800 #making square so no need for height; it will be the same

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH))

# the way this will be implememted is as follows:
# we will have each square in the grid act as its own entity, simiar to how i set up the grid in my basic search file
# COULD use a get_adjacent() function for each node and only note the blockers 
# wondering if i should make path sprites and blocker sprites, but it might be easier to use the color coding system tech w/ tim uses.
# also another way to do this would be making an array based grid with different numbers representing visited/not visited and listening for mouseclicks

class Node: #this is going to represent a square in the grid
    def __init__(self, row, col, width, n_rows): # will create a surface of size width at (row, col)
        self.row = row
        self.col = col
        self.width = width
        self.n_rows = n_rows
        #this will set the position to put the node on the surface since the grid is not actually a grid
        self.x = row * width
        self.y = col * width
        self.color = CREAM
        #these booleans are so that we can color code and so that we can use them in the search functions
        self.visited = False
        self.obstacle = False
        self.goal = False
        #this will be populated with the nodes around the current node that are able to be visited
        self.adjacent = []
    
    def get_position(self):
        return (self.row, self.col)

    #checkers to be used 
    def is_visited(self):
        return self.visited

    def is_obstacle(self):
        return self.obstacle

    def is_goal(self):
        return self.goal

    def reset_node(self):
        self.color = CREAM
        self.visited = False
        self.obstacle = False
        self.goal = False
        
    def draw(self):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    def get_adjacent(self):


# making class for entire grid
class Grid:
    def __init__(self, n_rows, width):
        self.n_rows = n_rows
        self.width = width

    #if user changes grid size
    def update_grid(self, nr, nc):
        self.n_rows = nr
        self.n_cols = nc
        self.make_grid()

    def make_grid(self):
        grid = []
        node_width = self.width // self.n_rows # this tells us how wide each square will need to be in the grid
        for row in range(self.n_rows):
            grid.append([]) #creating a new row
            for col in range(self.n_rows):
                node = Node(row, col, node_width, self.n_rows)
                grid[x].append(node) #add new node to grid

    def draw_grid(self, window):
        margin = self.width // self.n_rows
        for row in range(self.n_rows):






def heuristic_max(state, goal):
    cols = abs(goal[0] - state[0])
    rows = abs(goal[1] - state[1])
    x1=np.array(state)
    x2=np.array(goal)
    euc = np.sqrt(np.sum((x1-x2)**2))
    return max(cols, rows, euc)


