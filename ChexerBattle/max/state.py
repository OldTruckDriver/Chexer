from max.utils import (get_exit_cells, moveable_cells, jumpable_cells, MOVE, JUMP, EXIT, PASS)

class State:
    def __init__(self, colour):

        # Record the player's own colour
        self.colour = colour

        # Set a variable to record the number of already exited pieces
        self.num_of_exited = {
            "red": 0,
            "blue": 0,
            "green": 0
        }

        # Set the initial locations of Chexers pieces for each player
        self.piece_locs = {
            "red": [(-3, 0), (-3, 1), (-3, 2), (-3, 3)],
            "blue": [(0, 3), (1, 2), (2, 1), (3, 0)],
            "green": [(0, -3), (1, -3), (2, -3), (3, -3)]
        }

    def get_all_pieces(self):
        occupied = []
        for pieces in self.piece_locs.values():
            occupied += pieces
        return occupied

    def get_possible_actions(self, colour):
        possible_actions = []

        # Loop through all pieces of the current player
        for curr_cell in self.piece_locs[colour]:

            occupied = self.get_all_pieces()

            # Exit actions
            if curr_cell in get_exit_cells(colour):
                possible_actions += [(EXIT, curr_cell)]

            # Move actions
            for next_cell in moveable_cells(curr_cell, occupied):
                possible_actions += [(MOVE, (curr_cell, next_cell))]

            # Jump actions
            for next_cell in jumpable_cells(curr_cell, occupied):
                possible_actions += [(JUMP, (curr_cell, next_cell))]

        return possible_actions

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
            self.num_of_exited[colour] += 1

    def get_in_danger(self):
        in_danger = set()
        occupied = self.get_all_pieces()
        for curr_cell in self.piece_locs[self.colour]:
            neighbours = moveable_cells(curr_cell, [])
            for colour, pieces in self.piece_locs.items():
                if colour != self.colour:
                    for other_piece in pieces:
                        # melicious pieces
                        if other_piece in neighbours:
                            other_q, other_r = other_piece
                            curr_q, curr_r = curr_cell
                            target_piece = (curr_q * 2 - other_q, curr_r * 2 - other_r)
                            if target_piece in neighbours and (not target_piece in occupied):
                                in_danger.add(curr_cell)
        return len(in_danger)
