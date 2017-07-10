import random
from math import cos, exp, pi
import matplotlib.pyplot as plt
import numpy as np

#GENETIC ALGORITHM

population_size = 100
max_generations = 100
mutation_rate = 0.01
crossover_rate = 0.9
x_size = 11
y_size = 12
chromosome_size = x_size + y_size
population = []

# 1. INITIALIZATION
def intitialize(population):
    while len(population) < population_size:
        x_chromosome = ""
        y_chromosome = ""
        for bit in range(x_size):
            x_chromosome += str(random.randint(0,1))
        for bit in range(y_size):
            y_chromosome += str(random.randint(0,1))
        if(binary_to_real_x(x_chromosome) + binary_to_real_y(y_chromosome) < 2):
             population.append(x_chromosome + y_chromosome)

# 2. FITNESS EVALUATION
def evaluate(chromosome):
    x = binary_to_real_x(chromosome[:x_size])
    y = binary_to_real_y(chromosome[x_size:])
    fi = 20*exp(-0.2*(x**2+y**2))
    se = exp(cos(2*pi*x) + cos(2*pi*y))
    return fi + se

# 3. SELECTION
def roulette_selection():
    scores = total_evaluation()
    rand = random.random()
    cumulation = 0
    print(scores[3])
    for i in range(len(scores)):
        cumulation += scores[i]
        if(cumulation > rand):
            return population[i]

# 4, CROSSOVER
# uniform using random bit-mask
def crossover(chrom1, chrom2):
    cross1 = ""
    cross2 = ""
    bit_mask = np.random.randint(0,2,chromosome_size)
    for i in range(len(bit_mask)):
        if bit_mask[i] == 0:
            cross1 += chrom1[i]
            cross2 += chrom2[i]
        else:
            cross1 += chrom2[i]
            cross2 += chrom1[i]
    return cross1, cross2

# 5. MUTATION
# bit-by-bit
def mutate_chromosome(chromo):
    new_chromo = ""
    for i in chromo:
        if random.random() > mutation_rate:
            new_chromo += i
            continue
        if i == "0":
            new_chromo += "1"
        else:
            new_chromo += "0"
    return new_chromo

# 6. CONSTRAINT HANDLING
def valid_chromosome(chromosome):
    x = binary_to_real_x(chromosome[:x_size])
    y = binary_to_real_y(chromosome[x_size:])
    return x + y <= 2

def binary_to_real_x(num):
    x_mark = int(num,2)
    return float("{0:.3f}".format(-1 + x_mark*(2/((2**x_size)-1))))

def binary_to_real_y(num):
    y_mark = int(num,2)
    return float("{0:.3f}".format(-1 + y_mark*(3/((2**y_size)-1))))

#Returns a list of evaluation scores, normalized
#for roulette selection
def total_evaluation():
    sum = 0
    scores = []
    for chromosome in population:
        fitness = evaluate(chromosome)
        sum += fitness
        scores.append(fitness)
    scores = [x/sum for x in scores]
    return scores

#Creates new population
#Chooses two parents, creates offspring, mutates and repeats
def repopulate():
    global population
    newPopulation = []
    while len(newPopulation) < population_size:
        chrom1 = roulette_selection()
        chrom2 = roulette_selection()
        if chrom1 == chrom2:
            continue
        if random.random() < crossover_rate:
            chrom1, chrom2 = crossover(chrom1, chrom2)
        chrom1 = mutate_chromosome(chrom1)
        chrom2 = mutate_chromosome(chrom2)
        if valid_chromosome(chrom1):
            newPopulation.append(chrom1)
        if valid_chromosome(chrom2):
            newPopulation.append(chrom2)
    #Elitism, keep best chromosome
    newPopulation[0] = find_best_chromo()[0]
    population = newPopulation

#Finds chromosome with highest fitness, returns both chromosome and corresponding score
def find_best_chromo():
    best_chromo = 0;
    best_fitness = -float("inf")
    for i in population:
        fitness = evaluate(i)
        if fitness > best_fitness:
            best_fitness = fitness
            best_chromo = i
    return best_chromo, best_fitness

def main():
    print("Initializing population")
    intitialize(population)
    print("Beginning running")
    best_fitnesses = []
    for i in range(max_generations):
        repopulate()
        if (i + 1) % 20 == 0:
            print("Finished generation: " + str(i+1))
        best_fitnesses.append(find_best_chromo()[1])
        if(i) % 100 == 0:
            print("Current best fitness level: " + str(best_fitnesses[-1]))

    best_chromo, best_fitness = find_best_chromo()
    best_fitnesses.append(best_fitness)
    print("x: " + str(binary_to_real_x(best_chromo[:x_size])))
    print("y: " + str(binary_to_real_y(best_chromo[x_size:])))
    print("Objective function value: " + str(float("{0:.4f}".format(best_fitness))))
    plt.plot(range(len(best_fitnesses)), best_fitnesses)
    plt.xlabel("Generation")
    plt.ylabel("Objective function value")
    plt.show()

main()
