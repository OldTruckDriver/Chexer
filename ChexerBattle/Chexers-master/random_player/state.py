# String constants to avoid typos
MOVE = "MOVE"
JUMP = "JUMP"
EXIT = "EXIT"
PASS = "PASS"

# The exit cells for pieces of each colour
EXIT_CELLS = {
    "red": [(3, -3), (3, -2), (3, -1), (3, 0)],
    "blue": [(0, -3), (-1, -2), (-2, -1), (-3, 0)],
    "green": [(-3, 3), (-2, 3), (-1, 3), (0, 3)]
}

class State:
    def __init__(self, colour):

        # Record the player's own colour
        self.colour = colour

        # Set the initial locations of Chexers pieces for each player
        self.piece_locs = {
                            "red": [(-3, 0), (-3, 1), (-3, 2), (-3, 3)],
                            "blue": [(0, 3), (1, 2), (2, 1), (3, 0)],
                            "green": [(0, -3), (1, -3), (2, -3), (3, -3)]
                        }


    def get_pieces(self):
        """
        Get a player's own Chexers' pieces.
        """
        return self.piece_locs[self.colour]

    def get_all_pieces(self):
        occupied = []
        for pieces in self.piece_locs.values():
            occupied += pieces
        return occupied
    
    def get_exit_cells(self):
        """
        Get a player's own exit cells.
        """
        return EXIT_CELLS[self.colour]
    
    def update(self, colour, action):
        """
        Update the board state according to the action of the player with the 
        specified colour.
        """
        (move, cells) = action
        if (move == MOVE or move == JUMP):
            (origin, dest) = cells

            if (move == JUMP):
                # Convert the captured piece to another colour accordingly
                middle_cell = tuple(map(lambda x, y: (x + y) // 2, origin, dest))
                for (piece_colour, pieces) in self.piece_locs.items():
                    if (middle_cell in pieces):
                        self.piece_locs[piece_colour].remove(middle_cell)
                        break
                self.piece_locs[colour].append(middle_cell)

            self.piece_locs[colour].remove(origin)
            self.piece_locs[colour].append(dest)

        elif (move == EXIT):
            origin = cells
            self.piece_locs[colour].remove(origin)