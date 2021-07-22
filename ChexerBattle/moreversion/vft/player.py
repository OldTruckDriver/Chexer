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
        self.state = State()
        self.colour_to_index = {'red': 0, 'green': 1, 'blue': 2}

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
        self.update(self.colour_to_index[colour], action)

class State:
    def __init__(self):
        self.players_hexes = (((-3, 3), (-3, 2), (-3, 1), (-3, 0)),
                              ((0, -3), (1, -3), (2, -3), (3, -3)),
                              ((3, 0), (2, 1), (1, 2), (0, 3)))

    def update(self, index, action):
        act = action[0]
        players_hexes = list(self.players_hexes)
        if act == "EXIT":
            move_from = action[1]
            player_hexes = list(players_hexes[index])
            player_hexes.remove(move_from)
            players_hexes[index] = tuple(player_hexes)
            self.players_hexes = tuple(players_hexes)
        if act == "MOVE":
            move_from = action[1][0]
            move_to = action[1][1]
            player_hexes = list(players_hexes[index])
            player_hexes.remove(move_from)
            player_hexes.append(move_to)
            players_hexes[index] = tuple(player_hexes)
            self.players_hexes = tuple(players_hexes)
        if act == "JUMP":
            move_from = action[1][0]
            move_to = action[1][1]
            player_hexes = list(players_hexes[index])
            x = int(move_from[0] + (move_to[0] - move_from[0]) / 2)
            y = int(move_from[1] + (move_to[1] - move_from[1]) / 2)
            changed_piece = (x, y)

            enemy_index = 0
            for enemy_hexes in players_hexes:
                if enemy_hexes != index and changed_piece in enemy_hexes:
                    enemy_hexes = list(enemy_hexes)
                    enemy_hexes.remove(changed_piece)
                    player_hexes.append(changed_piece)
                    player_hexes.remove(move_from)
                    player_hexes.append(move_to)
                    players_hexes[index] = tuple(player_hexes)
                    players_hexes[enemy_index] = tuple(enemy_hexes)
                    self.players_hexes = tuple(players_hexes)
                    break
                enemy_index += 1

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



