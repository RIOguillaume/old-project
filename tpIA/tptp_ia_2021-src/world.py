import time
import pygame.gfxdraw
import pygame
import numpy as np

# Dimensions du monde (constantes)
WIDTH = 10
HEIGHT = 10


def random_position():
    """
    Génère une position aléatoire dans le monde
    """
    x = np.random.randint(0, WIDTH)
    y = np.random.randint(0, HEIGHT)

    return x, y

def generate_grid(seed = 1,level = 0):
    global WIDTH,HEIGHT
    """
    Génère la grille
    """    
    WIDTH += level;
    HEIGHT += level;
    np.random.seed(seed)
    grid = [[0]*WIDTH for h in range(HEIGHT)]

    for obstacle in range(25+(level*level+15)):
        x, y = random_position()
        grid[x][y] = 1

    x, y = random_position()
    grid[x][y] = 2

    return grid

def get_target_position(grid):
    """
    Retourne la position cible (à atteindre) dans le monde
    """
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if grid[x][y] == 2:
                return x, y

def possible_actions():
    return 'left', 'right', 'up', 'down'

def possible_moves(grid, x, y):
    """
    Retourne la liste des mouvements possibles, sous forme de
    tuples (mouvement, (x, y)
    """
    moves = []

    for move in possible_actions():
        target_x, target_y = apply_move(x, y, move)
        if is_reachable(grid, target_x, target_y):
            moves.append((move, (target_x, target_y)))

    return moves

def is_reachable(grid, x, y):
    """
    Indique si une position cible est atteignable
    Elle n'est pas atteignable si elle est en dehors de la zone ou sur un obstacle
    """
    if x >= 0 and y >= 0 and x < WIDTH and y < WIDTH and grid[x][y] != 1:
        return True

    return False

def is_success(grid, x, y):
    """
    Indique si une case est la case cible
    """
    return grid[x][y] == 2

def random_reachable_position(grid):
    """
    Génère une position aléatoire atteignable (pas sur un obstacle)
    """
    while True:
        x, y = random_position()
        if is_reachable(grid, x, y) and grid[x][y] != 2:
            return x, y

def apply_move(x, y, move):
    """
    Applique un mouvement donné et retourne la nouvelle position
    """
    if move == 'left':
        x -= 1
    elif move == 'right':
        x += 1
    elif move == 'up':
        y -= 1
    elif move == 'down':
        y += 1

    return x, y

# Les variables pour le rendu avec pygame
    

def render(grid, robot_position = None, path = None, values = None):
    cell_size = 50
    size = (cell_size*WIDTH, cell_size*HEIGHT)
    pygame.init()
    screen = pygame.display.set_mode(size, 0, 32)
    robot_image = pygame.image.load('robot.png')
    arrow_image = pygame.image.load('arrow.png')
    question_image = pygame.image.load('question.png')
    font = pygame.font.SysFont(None, 24)
    t = 0
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                return
           

        for x in range(WIDTH):
            for y in range(HEIGHT):
                col = (255, 255, 255)
                if grid[x][y] == 1:
                    col = (0, 0, 0)
                elif grid[x][y] == 2:
                    col = (128, 255, 128)
                elif x%2 != y%2:
                    col = (235, 235, 235)
                pygame.draw.rect(screen, col, (x*cell_size, y*cell_size, cell_size, cell_size))
        
        if values is not None:
            for entry in values:
                img = font.render('%d' % values[entry], True, (170, 170, 245))
                screen.blit(img, (5+entry[0]*cell_size, 5+entry[1]*cell_size))

        if robot_position is not None:
            screen.blit(robot_image, (robot_position[0]*cell_size, robot_position[1]*cell_size))

            if path is not None:
                k = 0
                position = list(robot_position)
                for move in path:
                    k += 0.2
                    if k > t:
                        break

                    before = position.copy()
                    position[0], position[1] = apply_move(position[0], position[1], move)
                
                    if move == 'giveup':
                        screen.blit(question_image, (before[0]*cell_size, before[1]*cell_size))
                    else:
                        angle = {'right': 0, 'left': 180, 'down': 270, 'up': 90}[move]
                        rot = pygame.transform.rotate(arrow_image, angle)
                        screen.blit(rot, (before[0]*cell_size, before[1]*cell_size))         

        pygame.display.flip()
        time.sleep(0.01)
        t += 0.01
