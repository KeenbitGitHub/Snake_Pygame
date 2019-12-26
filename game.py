import pygame
import snake

pygame.init()
WIN_SIZE = WIN_WIDTH, WIN_HEIGHT = 800, 800
BLOCK_SIZE = BLOCK_WIDTH, BLOCK_HEIGHT = 50, 50 
CAPTION = "AI plays snake"
game_running = False
win = pygame.display.set_mode(WIN_SIZE)
snake_instance = None
direction = (1, 0)

def initialize():
    global WIN_SIZE, WIN_WIDTH, WIN_HEIGHT, CAPTION, game_running, snake_instance
    game_running = True
    snake_instance = snake.Snake((WIN_WIDTH/2, WIN_HEIGHT/2), 4)
    
    pygame.display.set_caption(CAPTION)
    
    
def player_input():
    global game_running, direction, BLOCK_SIZE
    UPDATE_SPEED = 400
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            game_running = False
            UPDATE_SPEED = 0
            break
        elif (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_LEFT and direction != (1, 0)):
                direction = (-1, 0)
            elif (event.key == pygame.K_RIGHT and direction != (-1, 0)):
                direction = (1, 0)
            elif (event.key == pygame.K_DOWN and direction != (0, -1)):
                direction = (0, 1)
            elif (event.key == pygame.K_UP and direction != (0, 1)):
                direction = (0, -1)
    
    snake_instance.move(direction, BLOCK_SIZE)
    print(snake_instance.head)
    print(snake_instance.moved_from)
    print(snake_instance.body)
    pygame.time.delay(UPDATE_SPEED)
    
    
def render():
    global BLOCK_WIDTH, BLOCK_HEIGHT, snake_instance, win
    for part in snake_instance.body:
        pygame.draw.rect(win, (0, 255, 0), (part[0], part[1], BLOCK_WIDTH, BLOCK_HEIGHT))
    pygame.draw.rect(win, (0, 200, 0), (snake_instance.head[0], snake_instance.head[1], BLOCK_WIDTH, BLOCK_HEIGHT))
    if (snake_instance.moved_from[0] != None and snake_instance.moved_from[1] != None):
        pygame.draw.rect(win, (0, 0, 0), (snake_instance.moved_from[0], snake_instance.moved_from[1], BLOCK_WIDTH, BLOCK_HEIGHT))
    pygame.display.update()

def main():
    global game_running, snake_instance
    
    initialize()
    
    while snake_instance.alive and game_running:
        player_input()
        render()
    
    pygame.quit()
    
main()