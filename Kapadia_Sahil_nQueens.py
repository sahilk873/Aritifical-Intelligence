import random

def random_chromosome(nq): #making random chromosomes 
    chromosome = []
    for i in range(nq):
        chromosome.append(random.randint(1, nq))
    return chromosome

def collisions(chromosome):
    horizontal_collisions = horizontal_collision(chromosome)
    diagonal_collisions = diagonal_collision(chromosome)
    return diagonal_collisions, horizontal_collisions

def diagonal_collision(chromosome):
    n = len(chromosome)
    ld, rd = [0] * (2*n), [0] * (2*n)
    for i in range(n):
        ld[i + chromosome[i] - 1] += 1
        rd[len(chromosome) - i + chromosome[i] - 2] += 1
    sumlist = 0
    for i in range(2*n-1):
        if ld[i]+rd[i]>2:
            sumlist.append((ld[i]-1 + rd[i]-1) / (n-abs(i-n+1)))
    return sum(sumlist)
    
def horizontal_collision(chromosome):
    hc = []
    for queen in chromosome:
        hc.append(chromosome.count(queen)-1)
    horizontal_collisions = sum(hc)
    return horizontal_collisions/2


def fitness(chromosome, maxFitness):    
    d, h = collisions(chromosome)
    return int(maxFitness - (d + h))

def probability(chromosome, fitness, maxFitness):
    return fitness(chromosome, maxFitness) / maxFitness

def pick(population, probabilities, i):
    storelist = []
    for c, p in zip(population, probabilities):
        storelist.append((c, p))
    storelist.sort(key=lambda x: x[1], reverse=True)
    return storelist[i][0], storelist[i+1][0]

    
def reproduce(board1, board2): #doing cross_over between two chromosomes
    l = len(board1)
    splice = random.randint(0, l - 1)
    x, y = board1[0:splice] + board2[splice:l], board2[0:splice] + board1[splice:l]
    return x, y

def mutate(chromosome):  #randomly changing the value of a random index of a chromosome
    change, mutation = random.randint(0, len(chromosome) - 1), random.randint(1, len(chromosome))
    chromosome[change] = mutation
    return chromosome

def genetic_algorithm(population, fitness, maxFitness, nq):
    mutation_probability = 0.6
    new_population = []
    probabilities = []
    for n in population:
        probabilities.append(probability(n, fitness, maxFitness))
    count = 0
    for i in range(len(population) - 80):
        x, y = pick(population, probabilities, i) #best chromosome 1
        child1, child2 = reproduce(x, y) #creating two new chromosomes from the best 2 chromosomes
        if count == 0:
            print_chromosome(child1, maxFitness)
            count+=1
        if random.random() < mutation_probability:
            child1 = mutate(child1)
        if random.random() < mutation_probability:
            child2 = mutate(child2)
        new_population.append(child1)
        new_population.append(child2)
    population = []
    for _ in range(100 - len(new_population)):
        population.append(random_chromosome(nq))
    new_population = new_population + population
    return new_population

def print_chromosome(chrom, maxFitness):
    print("Chromosome = {},  MaxFitness = {}".format(str(chrom), fitness(chrom, maxFitness)))

def generate():
    numberofqueens = int(input("Number of Queens: "))
    maxFitness = numberofqueens*(numberofqueens-1)/2
    population = []
    for i in range(100):
        population.append(random_chromosome(numberofqueens))
    
    generation = 0
    while not maxFitness in [fitness(chromosomes, maxFitness) for chromosomes in population]:
        population = genetic_algorithm(population, fitness, maxFitness, numberofqueens)
        generation += 1
    out = []
    for c in population:
        if fitness(c, maxFitness) == maxFitness:
            print("Solution is: " + str(c) + " in " + str(generation) + " generations with fitness of " + str(maxFitness) + "")
            out = c
            break
    board = [["x"] * numberofqueens for _ in range(numberofqueens)]
    for i, j in enumerate(out):
        board[numberofqueens - j][i] = "Q"
    print("\n".join(" ".join(row) for row in board))
            
generate()
            
           
            
    