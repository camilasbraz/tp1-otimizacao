import numpy as np
import random as rd
from random import randint
import matplotlib.pyplot as plt

class Backpack:
    def __init__(self, item_number, weight, value, threshold):
        self.item_number = item_number
        self.weight = weight
        self.value = value
        self.threshold = threshold

    def display_items(self):
        print('Item No.   Weight   Value')
        for i in range(len(self.item_number)):
            print('{0}          {1}         {2}\n'.format(self.item_number[i], self.weight[i], self.value[i]))

class GeneticAlgorithm:
    def __init__(self, backpack, pop_size, num_generations):
        self.backpack = backpack
        self.pop_size = pop_size
        self.num_generations = num_generations
        self.initial_population = np.random.randint(2, size=pop_size)
        self.initial_population = self.initial_population.astype(int)
        self.fitness_history = []

    def cal_fitness(self, population):
        fitness = np.empty(population.shape[0])
        for i in range(population.shape[0]):
            S1 = np.sum(population[i] * self.backpack.value)
            S2 = np.sum(population[i] * self.backpack.weight)
            if S2 <= self.backpack.threshold:
                fitness[i] = S1
            else:
                fitness[i] = 0
        return fitness.astype(int)

    def selection(self, fitness, num_parents):
        fitness = list(fitness)
        parents = np.empty((num_parents, self.pop_size[1]))
        for i in range(num_parents):
            max_fitness_idx = np.where(fitness == np.max(fitness))
            parents[i, :] = self.initial_population[max_fitness_idx[0][0], :]
            fitness[max_fitness_idx[0][0]] = -999999
        return parents

    def crossover(self, parents, num_offsprings):
        # Same as your crossover method
        offsprings = np.empty((num_offsprings, parents.shape[1]))
        crossover_point = int(parents.shape[1]/2)
        crossover_rate = 0.8
        i=0
        while (parents.shape[0] < num_offsprings):
            parent1_index = i%parents.shape[0]
            parent2_index = (i+1)%parents.shape[0]
            x = rd.random()
            if x > crossover_rate:
                continue
            parent1_index = i%parents.shape[0]
            parent2_index = (i+1)%parents.shape[0]
            offsprings[i,0:crossover_point] = parents[parent1_index,0:crossover_point]
            offsprings[i,crossover_point:] = parents[parent2_index,crossover_point:]
            i=+1
        return offsprings

    def mutation(self, offsprings):
        mutants = np.empty((offsprings.shape))
        mutation_rate = 0.4
        for i in range(mutants.shape[0]):
            random_value = rd.random()
            mutants[i,:] = offsprings[i,:]
            if random_value > mutation_rate:
                continue
            int_random_value = randint(0,offsprings.shape[1]-1)    
            if mutants[i,int_random_value] == 0 :
                mutants[i,int_random_value] = 1
            else :
                mutants[i,int_random_value] = 0
        return mutants   

    def optimize(self):
        num_parents = int(self.pop_size[0] / 2)
        num_offsprings = self.pop_size[0] - num_parents
        for _ in range(self.num_generations):
            fitness = self.cal_fitness(self.initial_population)
            self.fitness_history.append(fitness)
            parents = self.selection(fitness, num_parents)
            offsprings = self.crossover(parents, num_offsprings)
            mutants = self.mutation(offsprings)
            self.initial_population[0:parents.shape[0], :] = parents
            self.initial_population[parents.shape[0]:, :] = mutants

    def run_experiment(self):
        self.optimize()
        fitness_last_gen = self.cal_fitness(self.initial_population)
        max_fitness = np.where(fitness_last_gen == np.max(fitness_last_gen))
        parameters = [self.initial_population[max_fitness[0][0], :]]
        selected_items = self.backpack.item_number * parameters
        print('The optimized parameters for the given inputs are: \n{}'.format(parameters))
        print('\nSelected items that will maximize the knapsack without breaking it:')
        for i in range(selected_items.shape[1]):
            if selected_items[0][i] != 0:
                print('{}\n'.format(selected_items[0][i]))

    def plot_fitness_history(self):
        fitness_history_mean = [np.mean(fitness) for fitness in self.fitness_history]
        fitness_history_max = [np.max(fitness) for fitness in self.fitness_history]
        plt.plot(list(range(self.num_generations)), fitness_history_mean, label='Mean Fitness')
        plt.plot(list(range(self.num_generations)), fitness_history_max, label='Max Fitness')
        plt.legend()
        plt.title('Fitness through the generations')
        plt.xlabel('Generations')
        plt.ylabel('Fitness')
        plt.savefig('./resultados/plot.png')

# Example usage
item_number = np.arange(1, 11)
weight = np.random.randint(1, 15, size=10)
value = np.random.randint(10, 750, size=10)
knapsack_threshold = 35

backpack = Backpack(item_number, weight, value, knapsack_threshold)
backpack.display_items()

solutions_per_pop = 8
pop_size = (solutions_per_pop, item_number.shape[0])
num_generations = 50

genetic_algorithm = GeneticAlgorithm(backpack, pop_size, num_generations)
genetic_algorithm.run_experiment()
genetic_algorithm.plot_fitness_history()
