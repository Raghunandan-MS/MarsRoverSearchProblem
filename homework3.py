import math
from collections import deque
from heapq import heappush, heappop

def startUpFunction():
<<<<<<< Updated upstream
	# Creating a dict of all input parameters, for cleaner parameter and better function.
=======
	global inputParams
>>>>>>> Stashed changes
	inputParams = {};
	# Read the input.txt file in the current directory.
	input_file = open('testcases/input4.txt', 'r')
	# Read the file line by line and strip the new line charecter!
	input_data = input_file.readlines()
	# Add all additional inputs to the file.
	inputParams['algo_name'] = input_data[0].rstrip('\n');
	inputParams['width'] = int(input_data[1].rstrip('\n').split(' ')[0])
	inputParams['height'] = int(input_data[1].rstrip('\n').split(' ')[1])
	inputParams['x'] = int(input_data[2].rstrip('\n').split(' ')[0])
	inputParams['y'] = int(input_data[2].rstrip('\n').split(' ')[1])
	inputParams['max_elevation'] = int(input_data[3].rstrip('\n'))
	inputParams['target_site_count'] = int(input_data[4].rstrip('\n'))
	target_sites, mesh_grid = inputListToArray(inputParams['target_site_count'], input_data[5:])
	inputParams['target_sites'] = target_sites
	inputParams['array'] = list(map(list, zip(*mesh_grid)))
	algoType = inputParams['algo_name']
	input_file.close()
	# Call the init function to start search based on Algo type!
	# Returns a list of all possible outputs
	output = startGoalSearch(algoType)
	output_file = open('output.txt', 'w')
	for i in output:
		output_file.write(i)
	output_file.close()

def inputListToArray(cnt,data):
	target_sites = []
	mesh_grid = []
	for i in range(len(data)):
		if i<=cnt-1:
			target_sites.append(list(map(int, data[i].rstrip('\n').split(' '))))
		else:
			mesh_grid.append(list(map(int, data[i].rstrip('\n').split())))
	return target_sites, mesh_grid

# Common template for all functions to execute
def startGoalSearch(algoType):
	outputList = [];
	target_site_count = inputParams['target_site_count']
	goalSearchFunction, queuingFunction = mappingDict[algoType]; # Use the function as specified in the mapping dict!
	for i in range(target_site_count):
		target = (inputParams['target_sites'][i][0],inputParams['target_sites'][i][1])
		goalPath = goalSearchFunction(target, queuingFunction)
		'''
		The goal path here is a list of tuples.
		We use a for loop here to process this and print it in the desired co-ordinate format!
		'''
		if goalPath == 'FAIL':
			outputList.append(goalPath + '\n')
		else:
			outputString = ''
			for nodes in range(len(goalPath)):
				outputString = outputString + str(goalPath[nodes][0]) + ',' + str(goalPath[nodes][1]) + ' ';
			outputList.append(outputString.rstrip() + '\n')
	outputList[-1] = outputList[-1].strip()
	return outputList

def getNeighboringIndices(currNode, exploredList):
	neighborsList = []
	maxElevation = inputParams['max_elevation']
	w = inputParams['width']
	h = inputParams['height']
	array = inputParams['array']
	x, y = currNode
	for x1 in range(x-1,x+2):
		for y1 in range(y-1, y+2):
			if ((x1 >= 0 and  y1 >= 0) and (x!=x1 or y!=y1) and (0 <= x1 < w and 0 <= y1 < h) and (abs(array[x][y] - array[x1][y1]) <= maxElevation)) and ((x1,y1 not in exploredList)):
				neighborsList.append((x1,y1))
	return neighborsList # List that would contain all the permissible neighbors based on max elevation difference!
'''
Breadth First Search Implementation of Mars Rover!
'''
def bfsGoalSearching(target , queuingFunction):
	initialState = (inputParams['x'] , inputParams['y'])
	# Adding the initial state to the queue
	#queue = deque([[(initialState), []]]) # Add the start state and an empty list that will have all the tuples!
	queue = deque([[initialState, []]])
	# Creating a set of visited elements to keep track of all the elements that have been seen!
	visited = set();
	if initialState == target:
		# Rover has landed on the goal state!
		return [initialState]
	while queue:
		# Pop the first element in the Q and process it.
		currNode, path = queue.popleft()
		if currNode == target:
		# Goal state has been reached by BFS
			visited.add(currNode)
			return path + [target];	
		if currNode not in visited:
			queue = queuingFunction(queue, currNode, path, target, visited)
			visited.add(currNode)
	return "FAIL" # Because there is no path available to the target node for the Rover!

def bfsQueuingFunction(Q, currNode, path, target, visited):
	# Find all neighboring nodes to the given current node.
	maxElevation = inputParams['max_elevation']
	neighboringIndices = getNeighboringIndices(currNode, visited)
	for node in neighboringIndices:
		newPath = path + [currNode]
		Q.append([node, newPath])
	return Q

'''
Uniform Cost Search Algorithm for Mars Rover!
'''

def ucsGoalSearching(target, queuingFunction):
	initialState = (inputParams['x'], inputParams['y'])
	if initialState == target:
		# Start state was the goal state.
		return [initialState]
	heap = []; # A heap data strcuture that heapq uses to sort the lowest element! Consider this sort of as a frontier / priority q.
	#priorityQueue = []; # Using a list to sort the values to maintain a priority queue.
	exploredList = set() # SOmewhat on similar lines of a visited set in BFS!
	heappush(heap, [0, initialState, []]) # Push to the heap the initialState with cost 0 and an empty neighbors path!
	#priorityQueue.append([0, initialState, []]) # Considering the initial state to have 0 path cost and no parents!
	while heap:
		cost , currNode , path = heappop(heap) # Pop's always the smallest element. Here based on the cost size.
		if currNode == target:
			# Goal State has been found!
			exploredList.add(currNode)
			return path + [currNode];
		if currNode not in exploredList:
			heap = queuingFunction(heap, cost, currNode, path, target, exploredList)
			exploredList.add(currNode)
			#if currNode == (68, 28):
			#	print (heap)
	# Return Fail as there is no path to the target node!
	return "FAIL"

def	ucsQueuingFunction(heap, cost, currNode, path, target, exploredList):
	ADJ_PATH_COST = 10
	DIAG_PATH_COST = 14
	maxElevation = inputParams['max_elevation']
	# Now, find the list of all neighbors to the current node!
	neighboringNodes = getNeighboringIndices(currNode, exploredList)
	for node in neighboringNodes:
		totalCost = 0
		if ((node[0] in currNode) or (node[1] in currNode)):
			totalCost = cost + ADJ_PATH_COST # Neighbor that is non-diagonally adjacent.
		else:
			totalCost = cost + DIAG_PATH_COST # Neighbor that is diagonally adjacent.
		updatedPath = path + [currNode]
		heappush(heap, [totalCost, node, updatedPath])
	return heap;

'''
A* Implementation for the Mars Rover Problem
'''
def aStarGoalSearching(target , queuingFunction):
	initialState = (inputParams['x'] , inputParams['y'])
	if initialState == target:
		# The Rover has landed on the target! Yay!
		return [initialState]
	heap = []
	exploredList = set() # A list that will store all the visited lists!
	xDiff = abs(initialState[0] - target[0])
	yDiff = abs(initialState[1] - target[1])
	initDistance = math.ceil(math.sqrt(math.pow(xDiff , 2) + math.pow(yDiff , 2)))
	heappush(heap, [initDistance, 0, initialState, []]) # Assumption that the estimated cost at starting is 0 for the Rover's landing position.
	while heap:
		heuristicCost, cost, currNode, path = heappop(heap)
		if currNode == target:
			# Rover has reached the goal state!
			exploredList.add(currNode)
			return path + [currNode]
		if currNode not in exploredList:
			heap = queuingFunction(heap, cost, currNode, path, target, exploredList)
			exploredList.add(currNode)
	return "FAIL"

def aStarQueuingFunction(heap, cost, currNode, path, target, exploredList):
	ADJ_PATH_COST = 10 # Assumption that the cost to go to non diagonal neighbors for the Rover is 10.
	DIAG_PATH_COST = 14 # Diagonally moving the rover takes an approx cost of 14.
	neighbors = getNeighboringIndices(currNode, exploredList)
	# Better to compute the heuristic cost for each node as compared to making multiple calls in a for loop. (neighbor_x,neighbor_y,heuristicCost,elevDiff)
	neighborsHeuristicCost = heuristicEvalFunction(neighbors, currNode, target)
	for nodes in neighborsHeuristicCost:
		totalCost = 0
		totalHeuristicCost = 0
		neighbor, heuristicValue, elevDiff = nodes
		#totalHeuristicCost = cost + heuristicValue # Add the cost to reach the neighbor + the heuristic
		if ((nodes[0] in currNode) or (nodes[1] in currNode)):
			totalCost = cost + elevDiff + ADJ_PATH_COST + heuristicValue
		else:
			totalCost = cost + elevDiff + DIAG_PATH_COST + heuristicValue
		updatedPath = path + [currNode]
		heappush(heap, [totalCost, totalCost - heuristicValue, neighbor, updatedPath])
	return heap

def heuristicEvalFunction(neighborsList, currNode, target):
	array = inputParams['array']
	neighborsHeuristicCost = [] # Appending a tuple of 3 elements (neighbors_x, neighbors_y, heuristicCost, maxElevation)
	for neighbors in neighborsList:
		elevDiff = abs(array[currNode[0]][currNode[1]] - array[neighbors[0]][neighbors[1]])
		if neighbors == target:
			neighborsHeuristicCost.append([neighbors, 0, elevDiff]) # If it is the goal state, we set the heuristic cost to 0!
		else:
			xDiff, yDiff = abs(neighbors[0] - target[0]), abs(neighbors[1] - target[1])
			totalEuclideanCost = math.ceil(math.sqrt((math.pow(xDiff, 2) + math.pow(yDiff, 2))))
			neighborsHeuristicCost.append([neighbors, totalEuclideanCost, elevDiff])
	return neighborsHeuristicCost

# Mapping of Queuing Function to Algo names!
mappingDict = {
	'BFS': [bfsGoalSearching, bfsQueuingFunction],
	'UCS': [ucsGoalSearching, ucsQueuingFunction],
	'A*': [aStarGoalSearching, aStarQueuingFunction]
}

if __name__ == "__main__":
	startUpFunction()