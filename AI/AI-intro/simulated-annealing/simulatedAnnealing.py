from math import exp
from time import time
import numpy
import random
import copy
import sys

#CartonSolver is the specialization class. Objective function and neighbor generation is implemented here 
class CartonSolver():
	k = None
	horizontal_size = None
	vertical_size = None
	f_target = None

	def __init__(self, k, x, y):
		self.horizontal_size = x
		self.vertical_size = y
		self.k=k
		self.f_target = k*x+1 if x<y else k*y+1

	#Just returning the sum of eggs plus 1 actually makes a pretty good objective function
	#This is because we never make any illegal neighbors, and thusly don't need to consider any punishment.
	#The large commented block of code underneath is a previous OF, which considered where the eggs
	#were placed in relation to eachother. Unnecessarily complex
	def objective_function(self, state):
		return numpy.sum(state)+1 
		"""
		sum = 1
		for i in state:
			horizontal_eggs = numpy.sum(i)
			if horizontal_eggs > 1:
				sum += horizontal_eggs - 1
		for i in range(len(state)):
			vertical_eggs = numpy.sum(state[:,i])
			if vertical_eggs > 1:
				sum += vertical_eggs -1
		flipped = numpy.flipud(state)
		for i in range(-len(state[0])+1, len(state[0])):
			x = numpy.sum(numpy.diagonal(state, i))
			y = numpy.sum(numpy.diagonal(flipped, i))
			if x>1: sum+=x-1
			if y>1: sum+=y-1
			#if x==0 or y==0: sum+=0.9
		
		#return sum
		"""

	#Checks if the current board is legal
	#If number of eggs exceeds limit in any horizontal, vertical or diagonal line, return False	
	def viable_board(self,state):
		for i in state:
			horizontal_eggs = numpy.sum(i)
			if horizontal_eggs > self.k:
				return False
		for i in range(len(state)):
			vertical_eggs = numpy.sum(state[:,i])
			if vertical_eggs > self.k:
				return False
		flipped = numpy.flipud(state)
		for i in range(-len(state[0])+1, len(state[0])):
			x = numpy.sum(numpy.diagonal(state, i))
			y = numpy.sum(numpy.diagonal(flipped, i))
			if x>self.k or y>self.k:
				return False
		return True

	#First populates board
	#Once it can not be populated further, flip bits randomly
	def generate_neighbors(self, state):
		neighbors = []
		for i in range(len(state)):
			for j in range(len(state[0])):
				if state[i][j] == 0:
					neighbor = numpy.copy(state)
					neighbor[i][j] = 1
					if self.viable_board(neighbor): neighbors.append(neighbor)
		while len(neighbors) == 0:
			for i in range(6):
				neighbor = numpy.copy(state)
				y,x = random.randint(0,len(neighbor)-1), random.randint(0,len(neighbor[0])-1)
				neighbor[y][x] = int(not neighbor[y][x])
				if self.viable_board(neighbor): neighbors.append(neighbor)
		return neighbors


#The general SA-algorithm. Takes in beginning state, temperatures
#and a specialization-class which must include f_target, and functions
#for finding objective function score and neighbors
def simulated_annealing(P, dt, t_max, specialization):
	t=t_max
	best_state = None
	maximum = 0
	FP = specialization.objective_function(P)
	while FP<specialization.f_target:
		if t<0: break
		neighbors = specialization.generate_neighbors(P)
		if not neighbors: return P
		F_neighbors = []
		for neighbor in neighbors:
			F_neighbors.append(specialization.objective_function(neighbor))
		P_max_index = F_neighbors.index(max(F_neighbors))
		P_max = neighbors[P_max_index]
		if F_neighbors[P_max_index]>maximum:
			best_state = neighbors[P_max_index]
		q = (F_neighbors[P_max_index]-FP)/FP
		p = min(1, exp(-q/t))
		if random.random()>p:
			P=P_max
		else:
			P = random.choice(neighbors)
		t = t - dt
		FP = specialization.objective_function(P)
	print("Finished")
	return best_state

#List of problems we want to solve
carton_solvers = [CartonSolver(2,5,5), CartonSolver(2,6, 6), CartonSolver(1,8,8), CartonSolver(3,10,10)]
f = open("sasolutions.txt", 'w')

#Go through every problem, and print solution to file
for carton_solver in carton_solvers:
	p = numpy.zeros((carton_solver.vertical_size, carton_solver.horizontal_size))
	solution = simulated_annealing(p, 0.001, 1, carton_solver)
	for line in solution:
		for element in line:
			f.write(str(int(element)))
		f.write("\n")
	f.write("\n\n\n")
