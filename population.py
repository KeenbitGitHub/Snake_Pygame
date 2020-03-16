import numpy as np
import game

class Population:
    def __init__(self, size):
        self.size = size
        self.population = np.array([])
        self.best_snake = 0
        
        for i in range(self.size):
            if (i == self.best_snake):
                self.population = np.append(self.population, game.Game(True, True, size))
            else:
                self.population = np.append(self.population, game.Game(False, False, size))
                
        self.update_population()
            
    def check_if_all_dead(self):
        for instance in self.population:
            if (instance.snake_instance.alive):
                return False
            
        return True
    
    def update_population(self):
        while (not self.check_if_all_dead()):
            for instance in self.population:
                instance.main()