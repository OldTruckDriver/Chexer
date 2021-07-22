import json
import copy

# String constants to avoid typos
MOVE = "MOVE"
JUMP = "JUMP"
EXIT = "EXIT"
PASS = "PASS"

TOTAL_DIST = "total_dist"
TO_EXIT = "to_exit"
CAN_EXIT = "can_exit"
OPPONENT_EXITED = "opponent_exited"

COLOURS = ["red", "green", "blue"]

# The minimum and maximum coordinates on the q and r axes
MIN_COORDINATE = -3
MAX_COORDINATE = 3

# Delta values which give the corresponding cells by adding them to the current
# cell
MOVE_DELTA = [(0, 1), (1, 0), (-1, 1), (0, -1), (-1, 0), (1, -1)]
JUMP_DELTA = [(delta_q * 2, delta_r * 2) for delta_q, delta_r in MOVE_DELTA]

# The exit cells for pieces of each colour
EXIT_CELLS = {
    "red": [(3, -3), (3, -2), (3, -1), (3, 0)],
    "blue": [(0, -3), (-1, -2), (-2, -1), (-3, 0)],
    "green": [(-3, 3), (-2, 3), (-1, 3), (0, 3)]
}

def all_cells():
    """
    generate the coordinates of all cells on the board.
    """
    ran = range(MIN_COORDINATE, MAX_COORDINATE + 1)
    return [(q, r) for q in ran for r in ran if -q-r in ran]


ALL_CELLS = all_cells()

def generate_cells(cell, delta_pairs):
    """
    generate a list of cells by adding delta values
    """
    return [(cell[0] + delta_q, cell[1] + delta_r)
                            for delta_q, delta_r in delta_pairs]


def moveable_cells(curr_cell, occupied):
    """
    moveable_cells are cells next to the current_cell with nothing occupied
    """
    neighbours = generate_cells(curr_cell, MOVE_DELTA)
    return [cell for cell in neighbours
                    if cell in ALL_CELLS and cell not in occupied]

def jumpable_cells(curr_cell, occupied):
    """
    jumpable_cells are cells that are one cell apart from the current cell
    and cells in the middle must be occupied by either a block or a piece
    """
    generated_cells = generate_cells(curr_cell, JUMP_DELTA)
    jumpable = []
    for cell in generated_cells:
        if cell in ALL_CELLS and cell not in occupied:
            middle_cell = tuple(map(lambda x, y: (x + y) // 2, curr_cell, cell))
            if middle_cell in ALL_CELLS and middle_cell in occupied:
                jumpable.append(cell)
    return jumpable

def exit_dist(colour, qr):
    """
    how many hexes away from a coordinate is the nearest exiting hex?
    Reference from sample solution for part A
    """
    q, r = qr
    if colour == 'red':
        return 3 - q
    if colour == 'green':
        return 3 - r
    if colour == 'blue':
        return 3 - (-q-r)

def get_exit_cells(colour):
    """
    Get a player's own exit cells.
    """
    return EXIT_CELLS[colour]

def get_weights():
    with open('learning_player/weight.json') as json_file:
        weights = json.load(json_file)
    return weights

#_______________________________________________________________________________

def next_p(state, curr_player):
    next_player = curr_player + 1
    while(1):
        next_player %= 3
        if len(state.piece_locs[COLOURS[next_player]]) > 0:
            break
        next_player += 1
    return next_player

def result(state, colour, action):
    next_state = copy.deepcopy(state)
    next_state.update(colour, action)
    return next_state

def evaluate(state, weights):
    v = []
    for colour in COLOURS:
        e = myeval(state, weights, colour)
        v.append(e)
    return tuple(v)

def myeval(state, weights, colour):
    if not state:
        return -float('Inf')

    e = 0

    # The sum of the distance between each piece to the exit cell
    e += state.get_feature(TOTAL_DIST, colour) * weights[TOTAL_DIST] * -1

    # The number of pieces that need to exit to win the game
    e += state.get_feature(TO_EXIT, colour) * weights[TO_EXIT] * -1

    # Whether the player has enough pieces to win the game.
    e += state.get_feature(CAN_EXIT, colour) * weights[CAN_EXIT]

    # The sum of the number of exited pieces for our opponents. If the player
    # deosn't have enough pieces to win the game, that player will be ignored.
    e += state.get_feature(OPPONENT_EXITED, colour) * weights[OPPONENT_EXITED] * -1

    return e
