# Snake implementation in Python using Pygame

## Introduction
This is a fully functional Snake-game implementation in Python using Pygame.

## Background
Snake is a simple videogame from the 1970's. The goal of the game is to eat as much food as possible by controlling the snake, without hitting the walls or the snake itself. Each time some food is eaten, the length of the snake increases.

## Overview
[collision_detection.py](https://github.com/KeenbitGitHub/Snake_Pygame/blob/master/collision_detection.py) does all of the collision detection. This includes collision detection between the snake and a wall, the snake and some food and the snake and itself.

[food.py](https://github.com/KeenbitGitHub/Snake_Pygame/blob/master/food.py) contains a food-class, which is an implementation of the food, which the snake is supposed to eat.

[game.py](https://github.com/KeenbitGitHub/Snake_Pygame/blob/master/game.py) contains a game-class, which is an implementation of the fully functional game.

[ge.py](https://github.com/KeenbitGitHub/Snake_Pygame/blob/master/ge.py) is currently an empty file, however, later it will be used to implement an AI to play the snake game (currently, the plan is to do this by implementin the NEAT-algorithm)

[main.py](https://github.com/KeenbitGitHub/Snake_Pygame/blob/master/main.py) contains an instance of the game. Run this file, to run the game.

[snake.py](https://github.com/KeenbitGitHub/Snake_Pygame/blob/master/snake.py) contains a snake-class which is an implementation of the snake, which the player controls.

## User guide
### Requirements
To run the game, you will need pygame version 1.9.6 or later, and python version 3.7.3 or later.

### How to run
To run the game, simply open the terminal and type the following

```
python main.py
```

## How to play
To control the snake, simply use the arrow keys.