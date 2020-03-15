import numpy as np
import game

class Population:
    def __init__(self, size):
        self.size = size
        self.population = np.array([])
        self.best_snake = np.random.randint(0, self.size) # first snake to simulate chosen randomly
        
        for i in range(self.size):
            if (i == i):
                self.population = np.append(self.population, game.Game(True, False))
            else:
                self.population = np.append(self.population, game.Game(False, False))
                
        self.update_population()
            
    def check_if_all_dead(self):
        for instance in self.population:
            if (instance.snake_instance.alive):
                return False
            
        return True
    
    def update_population(self):
        for instance in self.population:
            if (instance.snake_instance.alive):
                instance.main()