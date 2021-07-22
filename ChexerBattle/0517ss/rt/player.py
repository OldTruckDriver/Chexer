import random

class ExamplePlayer:
    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the 
        game state you would like to maintain for the duration of the game.

        The parameter colour will be a string representing the player your 
        program will play as (Red, Green or Blue). The value will be one of the 
        strings "red", "green", or "blue" correspondingly.
        """
        # TODO: Set up state representation.
        self.colour = colour
        self.board = Board(colour)
        self.state = State(self.board.piece_hexes, self.board)


    def action(self):
        """
        This method is called at the beginning of each of your turns to request 
        a choice of action from your program.

        Based on the current state of the game, your player should select and 
        return an allowed action to play on this turn. If there are no allowed 
        actions, your player must return a pass instead. The action (or pass) 
        must be represented based on the above instructions for representing 
        actions.
        """
        # TODO: Decide what action to take.
        # print("action", self.colour)
        # print(self.board.players_hexes)
        # print(self.state.board.players_hexes)
        # print(self.board.piece_hexes)
        # print(self.state.piece_hexes)
        # print()

        count = 0
        random_number = random.randint(1, len(self.state.actions_successors()))
        for i in self.state.actions_successors():
            count += 1
            if count == random_number:
                self.state = i[1]
                return i[0]
        return ("PASS", None)


    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s 
        turns) to inform your player about the most recent action. You should 
        use this opportunity to maintain your internal representation of the 
        game state and any other information about the game you are storing.

        The parameter colour will be a string representing the player whose turn
        it is (Red, Green or Blue). The value will be one of the strings "red", 
        "green", or "blue" correspondingly.

        The parameter action is a representation of the most recent action (or 
        pass) conforming to the above in- structions for representing actions.

        You may assume that action will always correspond to an allowed action 
        (or pass) for the player colour (your method does not need to validate 
        the action/pass against the game rules).
        """
        # TODO: Update state representation in response to action.
        # print("update",colour)
        self.board.update_board(colour, action)
        self.state.board = self.board
        self.state.piece_hexes = self.board.piece_hexes
        # print(self.board.players_hexes)
        # print(self.state.board.players_hexes)
        # print(self.board.piece_hexes)
        # print(self.state.piece_hexes)
        # print()

class Board:
    """
    Represent an (empty) single-player Chexers game board
    (it's just a grid of hexes, some of which are blocked)
    """

    def __init__(self, colour):
        """
        Board constructor
        - colour is a string 'red', 'green', or 'blue' (determines exit edge)
        - blocks is an iterable of the coordinates of hexes occupied by blocks
        """
        self.colour = colour
        self.red_piece_hexes = {(-3, 3), (-3, 2), (-3, 1), (-3, 0)}
        self.green_piece_hexes = {(0, -3), (1, -3), (2, -3), (3, -3)}
        self.blue_piece_hexes = {(3, 0), (2, 1), (1, 2), (0, 3)}

        self.players_hexes= {
            'red': {(-3, 3), (-3, 2), (-3, 1), (-3, 0)},
            'green': {(0, -3), (1, -3), (2, -3), (3, -3)},
            'blue': {(3, 0), (2, 1), (1, 2), (0, 3)},
        }

        if colour == 'red':
            self.exit_hexes = {(3, -3), (3, -2), (3, -1), (3, 0)}
            self.piece_hexes = self.red_piece_hexes
            self.block_hexes = self.green_piece_hexes.copy()
            self.block_hexes.update(self.blue_piece_hexes)
        if colour == 'green':
            self.exit_hexes = {(-3, 3), (-2, 3), (-1, 3), (0, 3)}
            self.piece_hexes = self.green_piece_hexes
            self.block_hexes = self.red_piece_hexes.copy()
            self.block_hexes.update(self.blue_piece_hexes)
        if colour == 'blue':
            self.exit_hexes = {(-3, 0), (-2, -1), (-1, -2), (0, -3)}
            self.piece_hexes = self.blue_piece_hexes
            self.block_hexes = self.red_piece_hexes.copy()
            self.block_hexes.update(self.green_piece_hexes)

            # set of all hexes (for easy bounds checking):
        ran = range(-3, +3 + 1)
        self.all_hexes = {(q, r) for q in ran for r in ran if -q - r in ran}

    def update_board(self, colour, action):
        act = action[0];
        if act == "EXIT":
            move_from = action[1]
            self.players_hexes[colour].remove(move_from)
        if act == "MOVE":
            move_from = action[1][0]
            move_to = action[1][1]
            self.players_hexes[colour].remove(move_from)
            self.players_hexes[colour].add(move_to)
        if act == "JUMP":
            move_from = action[1][0]
            move_to = action[1][1]
            x = int(move_from[0] + (move_to[0] - move_from[0]) / 2)
            y = int(move_from[1] + (move_to[1] - move_from[1]) / 2)
            changed_piece = (x, y)
            for key in self.players_hexes:
                if key != colour and changed_piece in self.players_hexes[key]:
                    self.players_hexes[key].remove(changed_piece)
                    self.players_hexes[colour].add(changed_piece)
            self.players_hexes[colour].remove(move_from)
            self.players_hexes[colour].add(move_to)

        self.update_blocks()
        self.piece_hexes = self.players_hexes[self.colour]

    def update_blocks(self):
        if self.colour == 'red':
            self.block_hexes = self.players_hexes["green"].copy()
            self.block_hexes.update(self.players_hexes["blue"])
        if self.colour == 'green':
            self.block_hexes = self.players_hexes["red"].copy()
            self.block_hexes.update(self.players_hexes["blue"])
        if self.colour == 'blue':
            self.block_hexes = self.players_hexes["red"].copy()
            self.block_hexes.update(self.players_hexes["green"])

    def exit_dist(self, qr):
        """how many hexes away from a coordinate is the nearest exiting hex?"""
        q, r = qr
        if self.colour == 'red':
            return 3 - q
        if self.colour == 'green':
            return 3 - r
        if self.colour == 'blue':
            return 3 - (-q - r)

    def can_exit_from(self, qr):
        """can a piece exit the board from this hex?"""
        return qr in self.exit_hexes

    def is_blocked(self, qr):
        """is this hex occupied by a block?"""
        return qr in self.block_hexes

    def __contains__(self, qr):
        """allows bounds checking with e.g. `(3, -2) in board` """
        return qr in self.all_hexes


# These are the directions in which moves/jumps are allowed in the game:
HEX_STEPS = [(-1, +0), (+0, -1), (+1, -1), (+1, +0), (+0, +1), (-1, +1)]


class State:
    """
    Represent a particular configuration of a single-player
    Chexers game (consisting of a set of piece coordinates and an
    underlying board, some of whose hexes are blocked)
    """

    def __init__(self, piece_hexes, board):
        """
        State constructor
        - piece_hexes is a frozenset (immutable set) of piece coordinates
        - board is a Board representing the underlying game board
        """
        self.board = board
        self.piece_hexes = piece_hexes

    def actions_successors(self):
        """
        construct and return a list of all actions available from this state
        (and their resulting successor states)
        """
        actions_successors_list = []
        for action in self._actions():
            actions_successors_list.append((action, self._apply(action)))
        return actions_successors_list

    def _actions(self):
        """
        construct and return a list of all actions available from this state
        """
        available_actions_list = []
        for qr in self.piece_hexes:
            # consider possible exit action:
            if self.board.can_exit_from(qr):
                available_actions_list.append(('EXIT', qr))

            # This (subtle!) loop computes available move/jump actions:
            # Logic: In each direction, first try to move (step by 1). If this
            # works, a jump is not possible. If the move is blocked, a jump
            # may be possible: try it. Always make sure not to fall off board.
            q, r = qr
            for step_q, step_r in HEX_STEPS:
                for atype, dist in [('MOVE', 1), ('JUMP', 2)]:
                    qr_t = q + step_q * dist, r + step_r * dist  # qr_t = 'target' hex
                    if qr_t in self.board:
                        if not self.board.is_blocked(qr_t) \
                                and qr_t not in self.piece_hexes:
                            available_actions_list.append((atype, (qr, qr_t)))
                            break  # only try to jump if the move IS blocked
                    else:
                        break  # if a move goes off the board, a jump would too
        if not available_actions_list:
            # Note that this shouldn't happen in Part A, but:
            available_actions_list.append(('PASS', None))
        return available_actions_list

    def _apply(self, action):
        """
        compute and return the state resulting from taking a particular action
        in this state
        """
        atype, aargs = action
        if atype == 'PASS':
            return self  # no need for a new state
        elif atype == 'EXIT':
            return State(self.piece_hexes - {aargs}, self.board)
        else:  # if atype == 'MOVE' or atype == 'JUMP':
            return State(self.piece_hexes - {aargs[0]} | {aargs[1]}, self.board)

    def is_goal(self):
        """Goal test: The game is won when all pieces have exited."""
        return not self.piece_hexes

    # we need to store states in sets and dictionaries, so we had better make
    # them behave well with hashing and equality checking:
    def __eq__(self, other):
        """
        states should compare equal if they have the same pieces
        (all states should share an underlying board in our program, so
        there's no need to check that)
        """
        return self.piece_hexes == other.piece_hexes

    def __hash__(self):
        """
        likewise, we should only consider the set of pieces relevant when
        computing a hash value for a state
        """
        return hash(self.piece_hexes)