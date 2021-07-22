# The minimum and maximum coordinates on the q and r axes
MIN_COORDINATE = -3
MAX_COORDINATE = 3

# Delta values which give the corresponding cells by adding them to the current
# cell
MOVE_DELTA = [(0, 1), (1, 0), (-1, 1), (0, -1), (-1, 0), (1, -1)]
JUMP_DELTA = [(delta_q * 2, delta_r * 2) for delta_q, delta_r in MOVE_DELTA]

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