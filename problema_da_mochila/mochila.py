import numpy as np
import random as rd
from random import randint
import matplotlib.pyplot as plt

class Knapsack:
    def __init__(self, num_items, max_weight):
        self.item_numbers = np.arange(1, num_items + 1)
        self.weights = np.random.randint(1, 15, size=num_items)
        self.values = np.random.randint(10, 750, size=num_items)
        self.threshold = max_weight

    def display_items(self):
        print('Item No.   Weight   Value')
        for i in range(len(self.item_numbers)):
            print('{}          {}         {}'.format(self.item_numbers[i], self.weights[i], self.values[i]))

class GeneticAlgorithm:
    def __init__(self, knapsack, solutions_per_pop, num_generations):
        self.solutions_per_pop = solutions_per_pop
        self.pop_size = (solutions_per_pop, len(knapsack.item_numbers))
        self.num_generations = num_generations
        self.knapsack = knapsack

    def create_initial_population(self):
        return np.random.randint(2, size=self.pop_size).astype(int)

    def cal_fitness(self, population):
        fitness = np.empty(population.shape[0])
        for i in range(population.shape[0]):
            S1 = np.sum(population[i] * self.knapsack.values)
            S2 = np.sum(population[i] * self.knapsack.weights)
            if S2 <= self.knapsack.threshold:
                fitness[i] = S1
            else:
                fitness[i] = 0
        return fitness.astype(int)

    def selection(self, fitness, num_parents, population):
        fitness = list(fitness)
        parents = np.empty((num_parents, population.shape[1]))
        for i in range(num_parents):
            max_fitness_idx = np.where(fitness == np.max(fitness))
            parents[i, :] = population[max_fitness_idx[0][0], :]
            fitness[max_fitness_idx[0][0]] = -999999
        return parents

    def crossover(self, parents, num_offsprings):
        offsprings = np.empty((num_offsprings, parents.shape[1]))
        crossover_point = int(parents.shape[1] / 2)
        crossover_rate = 0.8
        i = 0
        while parents.shape[0] < num_offsprings:
            parent1_index = i % parents.shape[0]
            parent2_index = (i + 1) % parents.shape[0]
            x = rd.random()
            if x > crossover_rate:
                continue
            offsprings[i, 0:crossover_point] = parents[parent1_index, 0:crossover_point]
            offsprings[i, crossover_point:] = parents[parent2_index, crossover_point:]
            i += 1
        return offsprings

    def mutation(self, offsprings):
        mutants = np.empty((offsprings.shape))
        mutation_rate = 0.4
        for i in range(mutants.shape[0]):
            random_value = rd.random()
            mutants[i, :] = offsprings[i, :]
            if random_value > mutation_rate:
                continue
            int_random_value = randint(0, offsprings.shape[1] - 1)
            if mutants[i, int_random_value] == 0:
                mutants[i, int_random_value] = 1
            else:
                mutants[i, int_random_value] = 0
        return mutants

    def optimize(self):
        population = self.create_initial_population()
        for _ in range(self.num_generations):
            fitness = self.cal_fitness(population)
            parents = self.selection(fitness, int(self.solutions_per_pop / 2), population)
            offsprings = self.crossover(parents, self.solutions_per_pop - parents.shape[0])
            mutants = self.mutation(offsprings)
            population[0:parents.shape[0], :] = parents
            population[parents.shape[0]:, :] = mutants

        fitness_last_gen = self.cal_fitness(population)
        max_fitness = np.where(fitness_last_gen == np.max(fitness_last_gen))
        parameters = population[max_fitness[0][0], :]
        return parameters
