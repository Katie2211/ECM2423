
import re ##The import so that we can use regular expressions
import random ##The import so that we can use randomness


def ReadFile(fileName): ## Basic reading of file, but also removes any character that isn't . or 0-9
    data = []
    f = open(fileName, "r")
    fileContents = f.read()
    temp = ""
    for i in fileContents:
        temp = re.sub(r'[^.0-9]', '', i)
        if temp != "":

            data.append(temp)
         ##hopefully this will remove all of the non numeric characters
    return data

def fitness(population):
    ##population is going to be the current State
    fitness = 0
    fitness_list = []
    temp = []
    for p in population: ##For each solution currently in population
        fitness = 0
        ##These now check the unique elements in the lines and boxes
        for i in range(9): ## check all the horizontal lines
            temp = [p[(i*9)],p[(i*9)+1],p[(i*9)+2],p[(i*9)+3],p[(i*9)+4],p[(i*9)+5],p[(i*9)+6],p[(i*9)+7],p[(i*9)+8]]
            fitness = fitness + UniqueInList(temp)
        for i in range(9): ## checks all the vertical lines
            temp = []
            for j in range(9):
                temp.append(p[i+(j*9)])
            fitness = fitness + UniqueInList(temp)


        for j in range(3): ##Checks all the boxes
            j*3
            temp1 = []
            temp2 = []
            temp3 = []
            for i in range(3):
                temp1.append(p[(j*27)+(i*9)])
                temp1.append(p[(j*27)+(i*9)+1])
                temp1.append(p[(j*27)+(i*9)+2])
                temp2.append(p[(j*27)+(i*9)+3])
                temp2.append(p[(j*27)+(i*9)+4])
                temp2.append(p[(j*27)+(i*9)+5])
                temp3.append(p[(j*27)+(i*9)+6])
                temp3.append(p[(j*27)+(i*9)+7])
                temp3.append(p[(j*27)+(i*9)+8])
            fitness = fitness + UniqueInList(temp1) + UniqueInList(temp2) + UniqueInList(temp3)
        fitness_list.append(fitness) ##Final score added to the list
        ##List of population and fitness have one-one mapping which will help later
    return fitness_list
def UniqueInList(temp): ##Checks how many unique elements are in the list

    unique = set(temp)
    return len(unique)
def populate(list, permanent, PopulationSize): ##this will populate a new suduko puzzle population
    population = []
    for i in range(PopulationSize):
        temp = list
        for i in range(len(list)):
            if i not in permanent:
                temp[i] = random.choice(NUMBERS) ##Picks a bunch of random numbers
        population.append(temp)
    return population

def newSolution(list, permanent): ##Same idea as populate but for one new solution not whole population
        temp = list
        for i in range(81):
            if i not in permanent:
                temp[i] = random.choice(NUMBERS)
        return temp

def mutate(offspring,permanent, PopulationSize, generation):
    for i in offspring:
        for j in range(25 - generation): ##Less mutate for each generation
            k = ""
            k = pickChangableValue(permanent)
            newNumber = random.choice(NUMBERS)  ##Mutates to random number
            i[k] = newNumber
    return offspring
def pickChangableValue(permanent): ## picks a number that is not one of the original numbers
    valid = False
    while not(valid):
        j = random.randint(0,80)
        if j in permanent: ##Permanant holds index of original numbers
            valid = False
        else:
            valid = True
    return j

def select_pop(population, fitness_population, PopulationSize, TruncationRate): ##list it takes in should already be sorted
    fitness_pop = zip(population,fitness_population) ##Zips up fitness to prevent loss of order in sorting
    sorted_population = sorted(fitness_pop, key=lambda tup: tup[1]) ## Sorts with relation to the 2nd tuple value(fitness)
    return [ individual for individual, fitness in sorted_population[:int(PopulationSize * TruncationRate)] ] ##cuts off the end 80% of the list

def crossover_pop(population,permanent, PopulationSize): ##More explanation in written answers
    temp = population
    new_pop = []
    for i in range(PopulationSize):
        n = random.choice(population)
        m = random.choice(population)
        j = random.choice([0,0,1,1,2]) ##Controls chance
        ##Picks either of the parents to keep going with or creates a new solution all together
        if j == 0:
            new_pop.append(n)
        elif j == 1:
            new_pop.append(m)
        else:
            new_pop.append(newSolution(population[0], permanent))
        #new_pop.append(crossover_pair(n,m))

    return new_pop


def best_pop(population, fitness_population):
        return sorted(zip(population, fitness_population), key = lambda ind_fit: ind_fit[1])[0] ##Sorts by fitness and then gets the first item

def EA(startFile, PopulationSize): ## our evolutionary algorithm
    PopulationSize = PopulationSize
    TruncationRate = 0.8
    MutationRate = 1.0/81
    NumberGeneration = 24


    ##Now going to get the start and target
    start = ReadFile(startFile)
    permanent = []
    for i in range(len(start)): ##creates a list of index of values that cannot be changed(the ones you start with)
        if(start[i] != "."):
            permanent.append(i)
    performance = []
    population = populate(start, permanent, PopulationSize) ##Starting population
    fitness_population = fitness(population)
    best_ind, best_fit = best_pop(population, fitness_population) ##Shows you the current situation based on the first population
    print("#%3d" % -1, "fit:%3d" % best_fit, "".join(best_ind)) ##-1 is the population before mutation or reproduction
    for gen in range(NumberGeneration):
        ##Normal steps for EA
        mating_pool = select_pop(population, fitness_population, PopulationSize, TruncationRate)
        offspring_population = crossover_pop(mating_pool,permanent, PopulationSize)
        population = mutate(offspring_population, permanent, PopulationSize, gen)
        fitness_population = fitness(population)
        best_ind, best_fit = best_pop(population, fitness_population)
        ##Gets the best of the current population
        print("#%3d" % gen, "fit:%3d" % best_fit, "".join(best_ind))
        performance.append((gen,best_fit,best_ind)) ##adds the best for average later
    return performance

def analysePerformance(performance):##gets the average of all the best solutions in each generation

    totalFit = 0
    for i in performance:
        totalFit = totalFit + i[1]
    print("The average Fit was: ", totalFit/24)


##Our "Alphabet" is going to be 0-9
##We have a global variable here, overall I have tried to limit the amount of globals I have as it is bad practice
NUMBERS = ["1","2","3","4","5","6","7","8","9"]
##Runs all the tests and trys to handle the large amount of data by splitting it up as much as possible
print("Welcome to the EA for Sudoko")
print("The maximum fitnes is 243")
print("The first result we are going to be getting is for a pop of 10")
for i in range(5): ##This will run the tests 60 times
    print("This is run ", i)
    print("Grid1 : ")
    analysePerformance(EA("Grid1.ss", 10))
    print("Grid2 : ")
    analysePerformance(EA("Grid2.ss",10))
    print("Grid3 : ")
    analysePerformance(EA("Grid3.ss",10))
print("The second result we are going to be getting is for a pop of 100")
for i in range(5):
    print("This is run ", i)
    print("Grid1 : ")
    analysePerformance(EA("Grid1.ss",100))
    print("Grid2 : ")
    analysePerformance(EA("Grid2.ss", 100))
    print("Grid3 : ")
    analysePerformance(EA("Grid3.ss",100))
print("The third result we are going to be getting is for a pop of 1000")
for i in range(5):
    print("This is run ", i)
    print("Grid1 : ")
    analysePerformance(EA("Grid1.ss",1000))
    print("Grid2 : ")
    analysePerformance(EA("Grid2.ss",1000))
    print("Grid3 : ")
    analysePerformance(EA("Grid3.ss",1000))
print("The forth result we are going to be getting is for a pop of 10000")
for i in range(5):
    print("This is run ", i)
    print("Grid1 : ")
    analysePerformance(EA("Grid1.ss",10000))
    print("Grid2 : ")
    analysePerformance(EA("Grid2.ss", 10000))
    print("Grid3 : ")
    analysePerformance(EA("Grid3.ss", 10000))
