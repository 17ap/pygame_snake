import pygame
import sys
import random
import pickle

FOOD_TO_LEVEL_UP = 7

# Game Initialization
pygame.init()
bg_raw = pygame.image.load("bg.jpg")

# Game Parameters
width = 800
height = 600
bg = pygame.transform.scale(bg_raw, (width, height))

cell_size = 20
cell_width = width // cell_size
cell_height = height // cell_size

food_raw = pygame.image.load("apple.png")
food = pygame.transform.scale(food_raw, (cell_height, cell_height))
delay = 10

# Colors
WHITE = (255, 255, 255)
GREEN = (79, 121, 66)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (105, 105, 105)
BROWN = (98, 42, 15)

# Game Window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game with Obstacles')
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont('Arial', 30)

# Snake
snake_pos = [[100, 50], [90, 50], [80, 50]]
snake_speed = [0, cell_size]
snake_skin = pygame.Surface((cell_size, cell_size))
snake_skin.fill(GREEN)

def collision(c1, c2):
    return abs(c1[0] - c2[0]) < cell_size and abs(c1[1] - c2[1]) < cell_size
def big_collision(c1, c2):
    return abs(c1[0] - c2[0]) < cell_size*2 and abs(c1[1] - c2[1]) < cell_size*2


# Obstacles
num_obstacles = 10
global obstacles
obstacles = []
obstacle_color = GREY


for i in range(num_obstacles):
    pos = [random.randrange(1, cell_width - 1) * cell_size, random.randrange(1, cell_height - 1) * cell_size]
    obstacles.append(pos)
# Food
# food = pygame.Surface((cell_size, cell_size))
# food.fill(RED)


def gen_food(obstacles):
    while (True):
        food_pos = [random.randrange(1, cell_width - 1) * cell_size, random.randrange(1, cell_height - 1) * cell_size]
        for o in obstacles:
            if big_collision(o, food_pos):
                food_pos = [random.randrange(1, cell_width - 1) * cell_size, random.randrange(1, cell_height - 1) * cell_size]

        return food_pos

food_pos = gen_food(obstacles)
food_eaten = 0


def game_over():
    screen.fill(BLACK)
    message = font.render('Game Over! Press Esc to quit', True, WHITE)
    score = font.render(f'Your score is {food_eaten}', True, WHITE)

    screen.blit(message, (width // 2 - message.get_width() // 2, height // 2 - message.get_height() // 2))
    screen.blit(score, (width // 2 - score.get_width() // 2, height // 3 - score.get_height() // 2))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    return
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

level_changed = False
while True:
    # 2 LEVEL
    if (food_eaten == FOOD_TO_LEVEL_UP and not level_changed):
        level_changed = True
        obstacles = []
        snake_skin.fill(BLACK)
        obstacle_color = BROWN
        num_obstacles += 5
        for i in range(num_obstacles):
            pos = [random.randrange(1, cell_width - 1) * cell_size, random.randrange(1, cell_height - 1) * cell_size]
            obstacles.append(pos)
        bg_raw = pygame.image.load("bg3.jpg")
        bg = pygame.transform.scale(bg_raw, (width, height))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_speed[1] != cell_size:
                snake_speed = [0, -cell_size]
            elif event.key == pygame.K_DOWN and snake_speed[1] != -cell_size:
                snake_speed = [0, cell_size]
            elif event.key == pygame.K_LEFT and snake_speed[0] != cell_size:
                snake_speed = [-cell_size, 0]
            elif event.key == pygame.K_RIGHT and snake_speed[0] != -cell_size:
                snake_speed = [cell_size, 0]

    snake_pos[0][0] += snake_speed[0]
    snake_pos[0][1] += snake_speed[1]

    for pos in snake_pos[1:]:
        if collision(snake_pos[0], pos):
            game_over()
            snake_pos = [[100, 50], [90, 50], [80, 50]]
            snake_speed = [0, cell_size]
    for obs in obstacles:
        if collision(snake_pos[0], obs):
            game_over()
            snake_pos = [[100, 50], [90, 50], [80, 50]]
            snake_speed = [0, cell_size]
            

    # Snake collision with walls
    if (snake_pos[0][0] < 0 or snake_pos[0][0] >= width
            or snake_pos[0][1] < 0 or snake_pos[0][1] >= height):
        game_over()
        snake_pos = [[100, 50], [90, 50], [80, 50]]
        snake_speed = [0, cell_size]

    # Snake eats food
    if collision(snake_pos[0], food_pos):
        food_pos = gen_food(obstacles)
        snake_pos.append([0, 0])
        food_eaten += 1

    # Move snake body
    for i in range(len(snake_pos) - 1, 0, -1):
        snake_pos[i] = list(snake_pos[i - 1])

    # Draw the screen
    # # screen.fill(BLACK)
    screen.blit(bg, (0, 0))

    # Draw the snake
    for pos in snake_pos:
        screen.blit(snake_skin, pos)

    # Draw the food
    screen.blit(food, food_pos)

    # Draw the obstacles
    for obs in obstacles:
        pygame.draw.rect(screen, obstacle_color, pygame.Rect(obs[0], obs[1], cell_size, cell_size))

    # Update the display
    pygame.display.update()
    clock.tick(delay)
