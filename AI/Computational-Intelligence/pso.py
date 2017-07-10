from random import random, uniform
from math import cos, exp, pi, sqrt
import matplotlib.pyplot as plt
import sys
from copy import deepcopy
from numpy import arange

#PARTICLE SWARM OPTIMIZATION

#Parameters if finetuning is selected
parameters = {'c1':arange(0,4.5,0.5),
            'c2': arange(0,4.5,0.5),
            'inertia_weight': arange(1, 2, 0.1)}
#Standard parameters if running without finetuning
c = 2.05
phi = 4.1
k = 2 / abs(2 - phi - sqrt(phi**2 - 4*phi))
inertia_weight = 1


max_iterations = 50
population_size = 30

class Particle:
    x = None
    y = None
    x_velocity = None
    y_velocity = None
    best_x = None
    best_y = None
    fitness = None

    def __init__(self, x, y, x_velocity, y_velocity):
        self.x = x
        self.y = y
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.best_y = y
        self.best_x = x
        self.fitness = self.fitness_value(self.x, self.y)

    def update_velocity(self, g_best, k, c1, c2):
        self.x_velocity = k*(inertia_weight*self.x_velocity + random()*c1*(self.best_x - self.x) + random() * c2 * (g_best.best_x - self.x))
        self.y_velocity = k*(inertia_weight*self.y_velocity + random()*c1*(self.best_y - self.y) + random() * c2 * (g_best.best_y - self.y))


    def update_location(self):
        old_x = self.x
        old_y = self.y
        self.x += self.x_velocity
        #If particle is outside boundary, bounce
        if self.x > 1 or self.x < -1:
            self.x = self.x/abs(self.x)
            self.x_velocity = - self.x_velocity
        self.y += self.y_velocity
        if self.y > 2 or self.y < -1:
            self.y = 2 if self.y>2 else -1
            self.y_velocity = - self.y_velocity
        self.fitness = self.fitness_value(self.x, self.y)
        #Punish if x+y > 2
        if self.x + self.y > 2:
            self.fitness = - float('inf')
        #Check if local best
        if  self.fitness > self.fitness_value(self.best_x, self.best_y):
            self.best_x = self.x
            self.best_y = self.y

    def fitness_value(self, x, y):
        if self.x is None or self.y is None:
            return -float('Inf')
        first = 20*exp(-0.2*(x**2+y**2))
        second = exp(cos(2*pi*x) + cos(2*pi*y))
        return first + second

#The inertia changes during run
def update_inertia(iteration, initial_inertia_weight=1):
    return initial_inertia_weight - (initial_inertia_weight-(initial_inertia_weight-1))*iteration/max_iterations

def pso(c1, c2, k, initial_inertia_weight):
    weight = initial_inertia_weight
    population = []
    best_fitnesses = []
    iteration = -1
    global_best = Particle(None, None, None, None)
    #Initialize population, random velocity and location
    for i in range(population_size):
        x_velocity = uniform(-1,1)
        y_velocity = uniform(-1,1)
        x = uniform(-1,1)
        y = uniform(-1, 2)
        particle = Particle(x,y,x_velocity, y_velocity)
        population.append(particle)
        #Check if global best
        if particle.fitness >= global_best.fitness:
            global_best = particle

    while iteration < max_iterations:
        iteration +=1
        for particle in population:
            # Don't update if particle is global best
            if particle.fitness == global_best.fitness:
                continue
            particle.update_velocity(global_best, k, c1, c2)
            particle.update_location()
            #Check if current particle is now global best
            if particle.fitness > global_best.fitness:
                global_best = particle
        #Update inertia weight
        weight = update_inertia(iteration, initial_inertia_weight)
        #Add current best result for later plot
        best_fitnesses.append(global_best.fitness)
        #Stop running if converged
        if iteration > 10 and  best_fitnesses[iteration] <= best_fitnesses[iteration - 10] + 0.00001:
            break
    return deepcopy(best_fitnesses), global_best

#Check if finetuning is wanted
if len(sys.argv) > 1 and sys.argv[1] == "-finetune":
    best_result_set = None
    best_fitness = -float('inf')
    best_c1= best_c2 = best_inertia_weight = best_phi = best_x = best_y = -1
    for c1 in  parameters["c1"]:
        for c2 in parameters["c2"]:
            for inertia_weight in parameters["inertia_weight"]:
                if c1 + c2 < 4:
                    continue
                phi = c1 + c2
                new_k = 2 / abs(2 - phi - sqrt(phi**2 - 4*phi))
                result, best_particle = pso(c1, c2, new_k, inertia_weight)
                #If result is better, save parameters
                if result[-1] > best_fitness:
                    best_fitness = result[-1]
                    best_c1 = c1
                    best_c2 = c2
                    best_phi = phi
                    best_inertia_weight = inertia_weight
                    best_result_set = deepcopy(result)
                    best_x = best_particle.x
                    best_y = best_particle.y
    plt.plot(range(len(best_result_set)), best_result_set)
    plt.xlabel("Generation")
    plt.ylabel("Objective function value")
    plt.title("c1: " + str(best_c1) + ", c2: " + str(best_c2) + ", initial_inertia_weight:" + str(best_inertia_weight))
    print(best_x, best_y, best_fitness)
    plt.show()
else:
    result, best_particle = pso(c,c,k, inertia_weight)
    plt.plot(range(len(result)), result)
    plt.xlabel("Generation")
    plt.ylabel("Objective function value")
    print(best_particle.x, best_particle.y, best_particle.fitness)
    plt.show()
