# Intelligent-Systems
Solving simple and advanced problems and tasks using basic knowledge of research algorithms, machine learning algorithms etc.

This project is presenting basic knowledge of research algorithms with defined heuristics:
Algorithms:
1a) Depth first search
2a) Breadth first search
3a) Branch and Bound
4a) A*
Heuristics for algorithms(each algorithm has its own heuristic):
1b) Surrounding tile with least cost. If there are multiple tiles with same cost, then the next tile is chosen by their relative position of the current tile, in the following order: north, east, south, west.
2b) Tile with least average cost of surrounding tiles. Surrounding tiles are the ones on the north, south, east and west, excluding tiles which are out of the map, or the one
that player is currently on. 
3b) If there are multiple partial paths with same cost, the chosen path is the one with least number of nodes. If there are partial paths with same cost and node's count, 
following node is chosen randomly between those partial paths.
4b) For each tile on the map, heuristic is euclidean distance between selected tile and the destination tile.

Quick review of the program:

Problem is being represented in pygame, called pyTanja. In folder maps, there are some examples of game maps, written in a specific way in basic .txt file. First two rows in map txt file
represent start position of the selected agent(Each agent is using one of the algorithm defined above), and the second row is position of the finish tile. Following rows present 
the map that game will be played on. Each character defines one sort of a tile:
r: pathway, cost = 2;
t: grass, cost = 3;
m: mud, cost = 5;
d: sand, cost = 7;
w: water, cost = 500;
s: rock, cost = 1000;

Agent is being selected in the command line arguments, before the start of the program. After it is being selected, program can start. After starting the program, algorithm can be 
started by pressing one of the following two keys:
ENTER = It finishes the algorithm right away, only leaving tracemarks where agent has been going before getting to the finish tile;
SPACE = Algorithm is being represented step by step, until the agent arrives to the finish tile.
Anyways, the final result of the agent path is the same.
pyTanja can be closed by pressing ESC.
There are also some util folders, like image folders, for agent images and tile images, etc.
