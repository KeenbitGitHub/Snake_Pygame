import game
from population import population

human_should_play = False
if (human_should_play):
    game_instance = game.Game()
else:
    pop = population(20, 100)