# Search Algorithm Visualizer

## What is this?
This project is meant to show how different algorithms behave when trying to find a path from one point to another. As of right now, only A* is availale, and commands are done entirely through the keyboard, aside from picking start/endpoints and placing barriers. 
I used pygame to create the user interface and grid for searching. The only valid moves are Up, Down, Left, and Right, all with a step cost of 1.

## Structure
To create the grid, I created a Grid class that creates an N x N grid of Node objects, which can be interacted with before starting the search program. These nodes will change color based on their role in the current iteration of the program.
There is also a Priority Queue class, which is used in A* to maintain the heap invariant and make sure each pop from the queue is the lowest cost node.
As of right now, there is a singular A_Star class that runs the search and determines the lowest cost path. In the future, this will be updated to use a Strategy design pattern in order to switch algorithm behavior.

# How to Run

## Requirements
 * Python 3.x
 * PyGame
 * Collections and Heapq
 * NumPy (avoidable if hueristic function is altered)

## Controls
 * Mouse
    * **First Click:** Starting Node
    * **Second Click:** Goal Node
    * **Subsequent Clicks:** Obstacle Nodes
    
 * Keyboard
    * **Space:** Begin Search
    * **r:** Reset Grid (only can be done before or after search algorithm has started/finished)
    * **Esc:** Exit the Game
    
## Color Coding
 * **Pink:** Start/End Nodes
 * **Brick:** Obstacle Nodes
 * **Grey:** Searched Nodes
 * **Sand:** Terminal Nodes (i.e. the nodes the algorithm decided to remove from the open set/frontier)
 * **Black:** Final Path Found
 
