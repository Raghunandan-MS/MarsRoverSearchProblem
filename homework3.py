import numpy as np
import math
from collections import deque
from heapq import heappush, heappop

def startUpFunction():
	# Creating a dict of all input parameters, for cleaner parameter and better function.
	inputParams = {};
	# Read the input.txt file in the current directory.
	input_file = open('input.txt', 'r')
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
	inputParams['target_sites'] = np.array(target_sites)
	inputParams['array'] = np.array(mesh_grid).transpose()
	algoType = inputParams['algo_name']
	# Call the init function to start search based on Algo type!
	# Returns a list of all possible outputs
	output = startGoalSearch(inputParams, algoType)
	output_file = open('output.txt', 'w')
	for i in output:
		output_file.write(i + '\n')
	input_file.close()
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

# Lambda function having cartesian co-ordinates to get all the neighbors indices.

getNeighborsIndex = lambda x, y, w, h : [(x2,y2) for x2 in range(x-1,x+2) for y2 in range(y-1,y+2) if ((x2 >= 0 and  y2 >= 0) and (x!=x2 or y!=y2) and (0 <= x2 < w and 0 <= y2 < h))]

# Common template for all functions to execute
def startGoalSearch(problemDict, algoType):
	outputList = [];
	target_site_count = problemDict['target_site_count']
	goalSearchFunction, queuingFunction = mappingDict[algoType]; # Use the function as specified in the mapping dict!
	for i in range(target_site_count):
		target = (problemDict['target_sites'][i][0],problemDict['target_sites'][i][1])
		goalPath = goalSearchFunction(problemDict, target, queuingFunction)
		'''
		The goal path here is a list of tuples.
		We use a for loop here to process this and print it in the desired co-ordinate format!
		'''
		if goalPath == 'FAIL':
			outputList.append(goalPath)
		else:
			outputString = ''
			for nodes in range(len(goalPath)):
				outputString = outputString + str(goalPath[nodes][0]) + ',' + str(goalPath[nodes][1]) + ' ';
			outputList.append(outputString)
	return outputList
'''
Breadth First Search Implementation of Mars Rover!

'''

def bfsGoalSearching(problem , target , queuingFunction):
	initialState = (problem['x'] , problem['y'])
	# Adding the initial state to the queue
	queue = deque([[(initialState), []]]) # Add the start state and an empty list that will have all the tuples!
	# Creating a set of visited elements to keep track of all the elements that have been seen!
	visited = set();
	if initialState == target:
		# Rover has landed on the goal state!
		return initialState
	while queue:
		# Pop the first element in the Q and process it.
		currNode, path = queue.popleft()
		if currNode == target:
		# Goal state has been reached by BFS
			visited.add(currNode)
			return path + [target];	
		if currNode not in visited:
			queue = queuingFunction(queue, problem, currNode, path, target, visited)
			visited.add(currNode)
	return "FAIL" # Because there is no path available to the target node for the Rover!

def bfsQueuingFunction(Q, problem, currNode, path, target, visited):
	# Find all neighboring nodes to the given current node.
	neighboringIndices = getNeighborsIndex(currNode[0], currNode[1], problem['width'], problem['height'])
	maxElevation = problem['max_elevation']
	for index in range(len(neighboringIndices)):
		neighbor = (neighboringIndices[index][0] , neighboringIndices[index][1])
		if abs(problem['array'][currNode[0]][currNode[1]] - problem['array'][neighbor[0]][neighbor[1]]) <= maxElevation and (neighbor not in visited):
			newPath = path + [currNode]
			Q.append([neighbor, newPath])
	return Q

'''
Uniform Cost Search Algorithm for Mars Rover!

'''

def ucsGoalSearching(problem, target, queuingFunction):
	initialState = (problem['x'], problem['y'])
	if initialState == target:
		# Start state was the goal state.
		return initialState;
	heap = []; # A heap data strcuture that heapq uses to sort the lowest element! Consider this sort of as a frontier / priority q.
	exploredList = set() # SOmewhat on similar lines of a visited set in BFS!
	heappush(heap, [0, initialState, []]) # Push to the heap the initialState with cost 0 and an empty neighbors path!
	while heap:
		cost , currNode , path = heappop(heap) # Pop's always the smallest element. Here based on the cost size.
		if currNode == target:
			# Goal State has been found!
			exploredList.add(currNode)
			return path + [currNode];
		if currNode not in exploredList:
			heap = queuingFunction(heap, problem, cost, currNode, path, target, exploredList)
			exploredList.add(currNode)
	# Return Fail as there is no path to the target node!
	return "FAIL"

def	ucsQueuingFunction(heap, problem, cost, currNode, path, target, exploredList):
	ADJ_PATH_COST = 10
	DIAG_PATH_COST = 14
	maxElevation = problem['max_elevation']
	# Now, find the list of all neighbors to the current node!
	neighboringNodes = getNeighborsIndex(currNode[0], currNode[1], problem['width'], problem['height'])
	for node in range(len(neighboringNodes)):
		neighbor = (neighboringNodes[node][0] , neighboringNodes[node][1])
		if (abs(problem['array'][currNode[0]][currNode[1]] - problem['array'][neighbor[0]][neighbor[1]]) <= maxElevation and neighbor not in exploredList):
			if ((neighbor[0] in currNode) or (neighbor[1] in currNode)):
				updatedPathCost = cost + ADJ_PATH_COST # Neighbor that is non-diagonally adjacent.
			else:
				updatedPathCost = cost + DIAG_PATH_COST # Neighbor that is diagonally adjacent.
			updatedPath = path + [currNode]
			heappush(heap, [updatedPathCost, neighbor, updatedPath])
	return heap;

'''
A* Implementation for the Mars Rover Problem

'''
def aStarGoalSearching(problem , target , queuingFunction):
	initialState = (problem['x'] , problem['y'])
	if initialState == target:
		# The Rover has landed on the target! Yay!
		exploredList.add(initialState)
		return initialState
	heap = [] # A binary min heap to always store the lowest cost path at the beginning!
	exploredList = set() # A list that will store all the visited lists!
	heappush(heap, [0, initialState, []]) # Assumption that the estimated cost at starting is 0 for the Rover's landing position.
	while heap:
		cost, currNode, path = heappop(heap)
		if currNode == target:
			# Rover has reached the goal state!
			exploredList.add(currNode)
			return path + [currNode]
		if currNode not in exploredList:
			heap = queuingFunction(heap, problem, cost, currNode, path, target, exploredList)
			exploredList.add(currNode)

def aStarQueuingFunction(heap, problem, cost, currNode, path, target, exploredList):
	ADJ_PATH_COST = 10 # Assumption that the cost to go to non diagonal neighbors for the Rover is 10.
	DIAG_PATH_COST = 14 # Diagonally moving the rover takes an approx cost of 14.
	array = problem['array'];
	maxElevation = problem['max_elevation']
	neighboringNodes = getNeighborsIndex(currNode[0], currNode[1], problem['width'], problem['height'])
	for node in range(len(neighboringNodes)):
		neighbor = (neighboringNodes[node][0] , neighboringNodes[node][1])
		elevationDifference = abs(array[currNode[0]][currNode[1]] - array[neighbor[0]][neighbor[1]])
		if ((elevationDifference <= maxElevation) and (neighbor not in exploredList)):
			heuristicCost = heuristicEvalFunction(neighbor, target)
			if ((neighbor[0] in currNode) or (neighbor[1] in currNode)):
				updatedPathCost = cost + ADJ_PATH_COST + elevationDifference + heuristicCost
			else:
				updatedPathCost = cost + DIAG_PATH_COST + elevationDifference + heuristicCost
			updatedPath = path + [currNode]
			heappush(heap, [updatedPathCost, neighbor, updatedPath])
	return heap

def heuristicEvalFunction(start, end):
	# Taking 2 tuples as the start and end point
	if start == end:
		# This is a special case for the goal state!
		return 0;
	else:
		xDiff = abs(end[0] - start[0])
		yDiff = abs(end[0] - start[0])
		cost = math.sqrt((math.pow(xDiff, 2) + math.pow(yDiff, 2))) # You might get a cost with float value!
		return cost

# Mapping of Queuing Function to Algo names!
mappingDict = {
	'BFS': [bfsGoalSearching, bfsQueuingFunction],
	'UCS': [ucsGoalSearching, ucsQueuingFunction],
	'A*': [aStarGoalSearching, aStarQueuingFunction]
}

if __name__ == "__main__":
	startUpFunction();
