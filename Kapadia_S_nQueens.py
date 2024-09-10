import random
def adjacencies(chromosome): 
    for i in range(4, len(chromosome)-3):
        if chromosome[i+1] - chromosome[i] == 1:
            return False
        if chromosome[i-1] - chromosome[i] == 1:
            return False
        if chromosome[i] - chromosome[i+2] == 2:
            return False
        if chromosome[i-2] - chromosome[i] == 2:
            return False
        if chromosome[i] - chromosome[i+3] == 3:
            return False
        if chromosome[i-3] - chromosome[i] == 3:
            return False
        
    return True
        
def collisions(chromosome):
    horizontal_collisions = horizontal_collision(chromosome)
    diagonal_collisions = diagonal_collision(chromosome)
    return diagonal_collisions, horizontal_collisions

def diagonal_collision(chromosome):
    n = len(chromosome)
    left_diagonal = [0] * 2 * n
    right_diagonal = left_diagonal[:]
    for i in range(n):
        store = chromosome[i]
        n = len(chromosome)
        left_diagonal[i+store-1] += 1
        right_diagonal[n-i+store-2] += 1
    diagonal_collisions = 0
    for i in range(len(left_diagonal)-1):
        counter = 0
        fitval = abs(i-n+1)
        fitval1 = n-fitval
        if left_diagonal[i] > 1:
            counter += left_diagonal[i]-1
        if right_diagonal[i] > 1:
            counter += right_diagonal[i]-1
        diagonal_collisions += counter / fitval1
    return diagonal_collisions
    
def horizontal_collision(chromosome):
    hc = []
    for queen in chromosome:
        hc.append(chromosome.count(queen)-1)
    horizontal_collisions = sum(hc)
    return horizontal_collisions/2

def random_chromosome(nq): 
    c = []
    for i in range(1, nq+1):
        c.append(i)
    while not adjacencies(c):
        random.shuffle(c)
    return c


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

    
def reproduce(board1, board2): 
    l = len(board1)
    splice = random.randint(0, l - 1)
    x, y = board1[0:splice] + board2[splice:l], board2[0:splice] + board1[splice:l]
    if not adjacencies(x):
        x = board1
    if not adjacencies(y):
        y = board2
    return x, y

def mutate(chromosome):  
    change, mutation = random.randint(0, len(chromosome) - 1), random.randint(1, len(chromosome))
    chromosome[change] = mutation
    return chromosome

def genetic_algorithm(population, fitness, maxFitness, nq):
    mutation_probability = (nq*nq)/100
    new_population = []
    probabilities = []
    for n in population:
        probabilities.append(probability(n, fitness, maxFitness))
    count = 0
    x, y = pick(population, probabilities, 0)
    store = x
    for i in range(len(population) - int(len(population)*0.9)):
        x, y = pick(population, probabilities, i) 
        child1, child2 = reproduce(x, store) 
        if count == 0:
            print_chromosome(child1, maxFitness)
            count+=1
        if random.random() < mutation_probability:
            store = mutate(child1)
            if adjacencies(store):
                child1 = store
        if random.random() < mutation_probability:
            store = mutate(child2)
            if adjacencies(store):
                child2 = store
        new_population.append(child1)
        new_population.append(child2)
        store = y
    population = []
    for i in range((nq//3)*2 - len(new_population)):
        population.append(random_chromosome(nq))
    new_population = new_population + population
    return new_population

def print_chromosome(chromosome, maxFitness):
    print("Chromosome is  " + str(chromosome) + " with fitness: " + str(fitness(chromosome, maxFitness)))

def generate():
    numberofqueens = int(input("Number of Queens: "))
    maxFitness = numberofqueens*(numberofqueens-1)/2
    population = []
    for i in range((numberofqueens//8)*2):
        population.append(random_chromosome(numberofqueens))
    
    generation = 0
    while not maxFitness in [fitness(chromosomes, maxFitness) for chromosomes in population]:
        population = genetic_algorithm(population, fitness, maxFitness, numberofqueens)
        generation += 1
    
    out = next((c for c in population if fitness(c, maxFitness) == maxFitness), None)

    if out is not None:
        print(f"Solution is: {out} in {generation} generations with fitness of {maxFitness}")
        board = [["x"] * numberofqueens for i in range(numberofqueens)]
    for i, j in enumerate(out):
        board[numberofqueens - j][i] = "Q"
    print("\n".join(" ".join(row) for row in board))
            
generate()
            
           
            
    