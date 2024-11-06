import world

# Les états, liste de tuples (x, y)
states = []

# Ce dictionnaire correspond à la fonction de valeur
values = {}

def initialize_states(grid):
    """
    Liste les états et initialise la fonction de valeur à 0
    """
    global states, values

    for x in range(world.WIDTH):
        for y in range(world.HEIGHT):
            if world.is_reachable(grid, x, y):
                state = (x, y)
                states.append(state)
                values[state] = 0

def find_best_action(grid, state):
    """
    Pour un état donné, trouve la meilleure action et sa valeur si l'on suit une politique
    gourmande (maximise r + v(s'))

    Retourne un tuple (action, valeur)
    """
    best = 'giveup', -100
    for move, new_state in world.possible_moves(grid, state[0], state[1]):
        if world.is_success(grid, new_state[0], new_state[1]):
            return move, -1
        else:
            value = -1 + values[new_state]

            if best is None or value > best[1]:
                best = move, value

    return best

def do_iterations(grid):
    """
    Fais les iterations pour construire la fonction de valeur optimale
    """
    k = 0
    changed = True
    while changed:
        k += 1
        print('Iteration %d...' % k)
        changed = False
        for state in states:
            (move, value) = find_best_action(grid,state)
            if  values[state] != value:
                changed = True
                values[state] = value
          
            

def find_path(grid, start):
    """
    Trouve le chemin permettant d'atteindre la cible à partir de la position de départ
    et find_best_action
    """
    pos = start
    path = []
    while not world.is_success(grid, pos[0], pos[1]):
        (move, value) = find_best_action(grid,pos)
        pos = world.apply_move(pos[0],pos[1],move)
        path.append(move)
    return path

def solve(grid, start):
    states.clear()
    values.clear()
    # Liste les états et initialise la fonction de valeur
    initialize_states(grid)

    # Fais les itérations
    do_iterations(grid)

    # Trouve le chemin
    return find_path(grid, start)
