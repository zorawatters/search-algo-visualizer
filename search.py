#import numpy as np
from collections import deque
from queue import PriorityQueue
import heapq
import unittest
import math
import abc
import pygame
import numpy as np
from pygame.locals import *

# using constants for colors 
SAND = (217, 168, 143) #for nodes searched
CREAM = (249, 227, 203) #for grid
GRAY = (117, 112, 112) #for terminal nodes
BRICK = (176, 102, 96) #for obstacles
BLACK = (0, 0, 0) #for final path
BLUE = (174, 187, 199) #for options screen?
SKY = (160, 187, 199)  
PINK = (234, 195, 184) #for endpoints
WHITE = (255, 255, 255)

pygame.init()


SCREEN_WIDTH = 800 #making square so no need for height; it will be the same
MARGIN = 2
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH))
window.fill(SAND)

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
        self.x = row * (MARGIN + width)
        self.y = col * (MARGIN + width)
        self.color = CREAM
        #these booleans are so that we can color code and so that we can use them in the search functions
        self.visited = False
        self.obstacle = False
        self.goal = False
        self.origin = False
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
        self.origin = False
        self.adjacent = []

    def change_color(self, chosen_color):
        self.color = chosen_color
        pygame.display.update()
        
    def draw(self):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))
        pygame.display.update()

    def fill_adjacent(self, grid):
        #for all of these if statements, we will check if the move is on the board and if it is blocked. if legal (on board and not blocked) then we will add it to the list of adjacent nodes
        #downward node
        max_row = grid.n_rows - 1
        grid = grid.grid
        if ((self.row - 1) > 0) and (grid[self.row - 1][self.col].is_obstacle() != True):
            self.adjacent.append(grid[self.row - 1][self.col])
        #upward node
        if ((self.row + 1) < max_row) and not grid[self.row + 1][self.col].is_obstacle(): 
            self.adjacent.append(grid[self.row + 1][self.col])
        #westward node
        if ((self.col - 1) > 0) and not grid[self.row][self.col - 1].is_obstacle():
            self.adjacent.append(grid[self.row][self.col - 1])
        #eastward node
        if ((self.col + 1) < max_row) and not grid[self.row][self.col + 1].is_obstacle():
            self.adjacent.append(grid[self.row][self.col + 1])
        #diagonal not possible for now



# making class for entire grid
class Grid:
    """This class creates the grid"""
    def __init__(self, n_rows, grid_width):
        self.n_rows = n_rows
        self.grid_width = grid_width
        self.grid = []
        self.grid_coordinates = []

    #if user changes grid size
    def update_grid(self, nr):
        self.n_rows = nr
        self.grid = []

    def reset_grid(self):
        for row in self.grid:
            for node in row:
                node.reset_node()
        pygame.display.update()


    def make_grid(self):
        node_width = (self.grid_width - (self.n_rows * MARGIN)) // self.n_rows # this tells us how wide each square will need to be in the grid
        for row in range(self.n_rows):
            self.grid.append([]) #creating a new row
            self.grid_coordinates.append([])
            for col in range(self.n_rows):
                node = Node(row, col, node_width, self.n_rows)
                self.grid[row].append(node) #add new node to grid
                self.grid_coordinates[row].append((row, col))

    def draw_grid(self):
        #margin = self.width // self.n_rows
        for row in self.grid:
            for node in row:
                node.draw()
        pygame.display.update()

    def get_clicked_node(self, postion):
        node_width = (self.grid_width - (self.n_rows * MARGIN)) // self.n_rows
        row = postion[0] // (node_width + MARGIN)
        col = postion[1] // (node_width + MARGIN)
        print(row, col)
        return self.grid[row][col]
    
    def start_search(self, strategy, origin, goal): #this is the context
        #print(grid.grid_coordinates)
        print("in grid")
        A_Star(self.grid, origin, goal)
        
#using strategy pattern to determine algorithm actions

# class searchAlgorithm(object): #this is the abstract class for a search algorithm
#     def __init__(self, name):
#         self.alg = name


#     def run_search(self, grid, origin, goal):
#         pass


#this is my code from a previous implementation of a* and ucs. 
class PQ:
    def __init__(self, start, cost):
        self.states = {} #keeps track of lowest cost to each state
        self.q = [] #this is the heap queue. is a set of (cost, state) tuples to represent elements on the frontier
        self.index = 0 #using to get through object comparison barrier
        self.add(start, cost, self.index) #initialize that baby

    def add(self, state, cost, index):
        self.index = index
        heapq.heappush(self.q, (cost, self.index, state)) #heapq is the priority queue algorithm so using it will maintain the heap invariant (each node smaller than children)
        self.states[state] = cost #add and set cost for new state


    def pop(self):
       # print("in pop: ", self.q)
        (cost, self.index, state) = heapq.heappop(self.q)  # get cost of getting to explored state (heappop returns the smallest item from heap, ie the lowest cost)
        self.states.pop(state) #not the same pop function. removing state from frontier
        return(cost, state)

    def replace(self, state, cost): #replace the lowest cost to the next state if we find one
        self.states[state] = cost #replace cost
        for i, (oldcost, index, oldstate) in enumerate(self.q): #look through the frontier
            if oldstate == state and oldcost > cost: #replace there too
                old_i = index
                self.q[i] = (cost, old_i, state)
                heapq._siftdown(self.q, 0, i) # now i is posisbly out of order; restore
        return

class A_Star():
    # minimizes f(n) where f(n) = h(n) + g(n) meaning heuristic + cheapest path from start to n
    def __init__(self, grid, origin, goal):
        self.grid = grid
        self.origin = origin
        self.goal = goal
        self.run_search(self.grid, self.origin, self.goal)

    def run_search(self, grid, origin, goal):
        frontier = PQ(origin, 0) #this will set our priority queue and add the origin to it (at a cost of 0)
        previous = {origin: None}
        explored = {} 
        g_scores = {node: float("inf") for row in self.grid for node in row} #setting high path costs to be overridden later
        g_scores[origin] = 0
        index = 1
        while frontier:
            for event in pygame.event.get():
                if event.type == QUIT: #if the user clicked the window close button
                    pygame.quit()
            current_node = frontier.pop()
            #print("node position: ", current_node[1].get_position())
            if current_node[1].is_goal():
                current_node[1].change_color(PINK)
                self.retrace_path(previous, current_node[1])
                return True
            for adj in current_node[1].adjacent:
                g_next = g_scores[current_node[1]] + 1 #since each move has a cost of 1
                if g_next < g_scores[adj]: #if the score to the adjacent node is less than previously recorded
                   # print("g score from current node to ", adj.get_position(), " : ", g_next)
                    g_scores[adj] = g_next
                    newcost = g_next + self.heuristic_max(adj.get_position(), goal.get_position())
                    if (adj not in explored) and (adj not in frontier.states):
                        index += 1
                        frontier.add(adj, newcost, index) #adding f score to priority queue
                        previous[adj] = current_node[1]
                        adj.change_color(SAND) #this will color all nodes added sand
                    elif (adj in frontier.states) and (frontier.states[adj] > newcost):
                        frontier.replace(adj, newcost) 
                        previous[adj] = current_node[1]
            
            if current_node[1] != self.origin: # colors nodes that we search and determine we are done searching from and will not go back into the frontier
                current_node[1].change_color(GRAY)
                current_node[1].visited = True
                
        return True

    def heuristic_max(self, state, goal):
        cols = abs(goal[0] - state[0])
        rows = abs(goal[1] - state[1])
        x1=np.array(state)
        x2=np.array(goal)
        euc = np.sqrt(np.sum((x1-x2)**2))
        return max(cols, rows, euc)

    def retrace_path(self, prev, state):
        if state is None:
            return []
        if state != self.origin and state != self.goal:
            state.change_color(BLACK)
        return self.retrace_path(prev, prev[state])+[state]



grid = Grid(20, SCREEN_WIDTH)
grid.make_grid()

running = True
origin = None
goal = None
started = False


while running:
    grid.draw_grid()
    for event in pygame.event.get():
        if event.type == KEYDOWN: #this is a keypress event
            if event.key == K_ESCAPE: #if the user presses the escape key
                running = False
        elif event.type == QUIT: #if the user clicked the window close button
            running = False

        if started:
            continue #doesnt allow user to press anything but quit and escape if the search algo is running

        if event.type == MOUSEBUTTONDOWN: #if left click
            position = pygame.mouse.get_pos()
            print(position)
           # row, col = grid.get_clicked_position(position)
           # curr_node = grid[row][col] #node pressed by user
            curr_node = grid.get_clicked_node(position)
            if origin is None and curr_node != goal:
                curr_node.origin = True
                curr_node.change_color(PINK)
                origin = curr_node
            elif goal is None and curr_node != origin:
                curr_node.goal = True
                curr_node.change_color(PINK)
                goal = curr_node
            elif curr_node not in (goal, origin):
                curr_node.obstacle = True
                curr_node.change_color(BRICK)

        if event.type == KEYDOWN:
            if event.key == K_r:
                grid.reset_grid()
                origin = None
                goal = None
            elif event.key == K_SPACE and not started:
                started = True
                for row in grid.grid: #setting the adjacent nodes in the grid
                    for node in row:
                        node.fill_adjacent(grid)
                print("starting search")
                grid.start_search('astar', origin, goal)


#THINGS TO DO: remove grid coordinates from functions, do path callback

pygame.quit()