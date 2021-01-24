from collections import deque
from queue import PriorityQueue
import heapq
import unittest
import math
import abc
import pygame
import numpy as np
from pygame.locals import *

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
        self.add(start, cost) #initialize that baby

    def add(self, state, cost):
        heapq.heappush(self.q, (cost,state)) #heapq is the priority queue algorithm so using it will maintain the heap invariant (each node smaller than children)
        self.states[state] = cost #add and set cost for new state

    def pop(self):
        (cost, state) =  heapq.heappop(self.q)  # get cost of getting to explored state (heappop returns the smallest item from heap, ie the lowest cost)
        self.states.pop(state) #not the same pop function. removing state from frontier
        return(cost, state)

    def replace(self, state, cost): #replace the lowest cost to the next state if we find one
        self.states[state] = cost #replace cost
        for i, (oldcost, oldstate) in enumerate(self.q): #look through the frontier
            if oldstate == state and oldcost > cost: #replace there too
                self.q[i] = (cost, state)
                heapq._siftdown(self.q, 0, i) # now i is posisbly out of order; restore
        return

class A_Star():
    # minimizes f(n) where f(n) = h(n) + g(n) meaning heuristic + cheapest path from start to n
    def __init__(self, grid, origin, goal):
        self.curr_grid = grid
        self.origin = origin
        self.goal = goal

    def run_search(self, grid, origin, goal):
        frontier = PQ(self.origin, 0) #this will set our priority queue and add the origin to it (at a cost of 0)
        previous = {start: None}
        explored = {} 
        g_scores = {node: float("inf") for row in self.curr_grid.grid for node in row} #setting high path costs to be overridden later
        g_scores[origin] = 0
        while frontier:
            for event in pygame.event.get():
                if event.type == QUIT: #if the user clicked the window close button
                    pygame.quit()
            
            current_node = frontier.pop()
            if current_node.is_goal():
                return True

            for adj in current_node.adjacent:
                g_next = g_scores[current_node] + 1 #since each move has a cost of 1
                if g_next < g_scores[adj]:
                    g_scores[adj] = g_next
                    newcost = g_next + heuristic_max(adj.get_position(), goal.get_position())
                    if (adj not in explored) and (adj not in frontier.states):
                        frontier.add(adj, newcost) #adding f score to priority queue
                        previous[adj] = current_node
                        adj.change_color(BLUE)
                    elif (adj in frontier.states) and (frontier.states[adj] > newcost):
                        frontier.replace(adj, newcost) 
                        previous[adj] = current_node
                        adj.change_color(SKY)
            if current_node != self.origin:
                current_node.change_color(GRAY)
                current_node.visited = True

    def heuristic_max(self, state, goal):
        cols = abs(goal[0] - state[0])
        rows = abs(goal[1] - state[1])
        x1=np.array(state)
        x2=np.array(goal)
        euc = np.sqrt(np.sum((x1-x2)**2))
        return max(cols, rows, euc)