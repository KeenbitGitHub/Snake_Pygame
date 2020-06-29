import numpy as np
import pygame
import game
from candidate import candidate
import matplotlib.pyplot as plt

class population:
    def __init__(self, SIZE, N_GENS, mutation_rate = 0.1):
        self.SIZE = SIZE
        self.N_GENS = N_GENS
        self.mutation_rate = mutation_rate
        
        self.create_population()
        self.run()
        
    def create_population(self):
        self.population = []
        for _ in range(self.SIZE):
            self.population.append(candidate())
        
    def run(self):
        runs = []
        for GEN in range(self.N_GENS):
            print("Running GEN {} out of {}".format(GEN, self.N_GENS))
            e_fitness = []
            for c_index, element in enumerate(self.population):
                print("Running candidate {} out of {}".format(c_index, self.SIZE))
                element.run()
                e_fitness.append(element.fitness)
                print(element.fitness)
            runs.append(np.mean(e_fitness))

            self.reproduce(e_fitness)
            
        plt.plot(list(range(self.N_GENS)), runs)
        plt.savefig("test.png")
        
    def pick_parent(self, pop_fitness):
        # Randomly chooses parents. Better ai's have a greater chance of being picked.
        fitness_distribution = []
        s = np.sum(pop_fitness)
        
        for fit in pop_fitness:
            fitness_distribution.append(fit/s)
                
        return np.random.choice(self.population, p = fitness_distribution)
            
    def reproduce(self, pop_fitness):
        # Finds parents
        parent1 = self.pick_parent(pop_fitness)
        parent2 = self.pick_parent(pop_fitness)
        # Cross over
        reproduction = np.array([np.array(parent1.nn.layers[1].weights), np.array(parent1.nn.layers[2].weights)])
        rnd_layer = np.random.randint(1, parent1.nn.n_layers - 1)
        rnd_row = np.random.randint(0, parent1.nn.layers[rnd_layer].weights.shape[0])
        rnd_col = np.random.randint(0, parent1.nn.layers[rnd_layer].weights.shape[1])
        
        for l_index, layer in enumerate(reproduction):
            if (l_index < rnd_layer):
                continue
            for r_index, row in enumerate(layer):
                if (r_index < rnd_row):
                    continue
                for el_index, element in enumerate(row):
                    if (el_index < rnd_col):
                        continue
                    reproduction[l_index][r_index][el_index] = parent2.nn.layers[l_index + 1].weights[r_index][el_index]
        
        # Creating new population with the new neural network
        self.create_population()
        for candidate in self.population:
            candidate.nn.load_weights(reproduction)
            
            # Mutation
            rnd = np.random.uniform()
            if (rnd <= self.mutation_rate):
                mutation = []
                for layer in reproduction:
                    mutation.append(layer + (np.random.normal(0, 1, size = layer.shape)/np.random.randint(1, 10)))
                
                candidate.nn.load_weights(mutation)
            

            
pop = population(50, 50)