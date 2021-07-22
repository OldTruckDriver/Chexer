import random
import copy
import math

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
        self.score = 0


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

        maximum_depth = 3
        root_player = 1
        alpha = -1
        new_state = copy.deepcopy(self.state)
        score = {1: 0, 2: 0, 3: 0}

        ran = range(-3, +3 + 1)
        all_nodes = []
        for qr in ((q, r) for q in ran for r in ran if -q - r in ran):
            all_nodes.append(qr)
        all_nodes = tuple(all_nodes)
        root = Node(self.colour, ("PASS", None), new_state, root_player, [(4, ("PASS", None))], score, all_nodes)
        maxn_value = self.MAXN(root, maximum_depth, root_player, alpha, self.colour)
        best = maxn_value[0]
        best_node = maxn_value[1]
        print(best)
        print(best_node.state.board.players_hexes)
        print(best_node.actions)
        print("--------------best!!!!!!!!!")

        print(best_node.actions[2][1])
        best_action = best_node.actions[2][1]

        if self.score == 3:
            print(self.score)
            for i in self.state.actions_successors():
                if i[0][0] == "EXIT":
                    return i[0]
        for i in self.state.actions_successors():
            if i[0] == best_action:
                print("0      action-----------", best)
                if best_action[0] == "EXIT":
                    self.score = self.score + 1
                print(self.score)
                return i[0]


        # for i in self.state.actions_successors():
        #
        #     # print("in_board", i[1].board.piece_hexes)
        #     new_board = copy.deepcopy(i[1].board)
        #     new_board.update_board(self.colour, i[0])
        #     i[1].piece_hexes = new_board.piece_hexes
        #     # print(i[1].piece_hexes)
        #     print(new_board.players_hexes)
        #     for j in i[1].actions_successors():
        #         new_board = copy.deepcopy(j[1].board)
        #         print(new_board.players_hexes)
        #         new_board.update_board(self.colour, j[0])
        #         j[1].piece_hexes = new_board.piece_hexes
        #         if len(j[1].piece_hexes) == len(best_node.state.board.players_hexes[self.colour]):
        #             if len(j[1].piece_hexes - best_node.state.board.players_hexes[self.colour]) == 0:
        #                 # print("this")
        #                 # print(i[1].piece_hexes)
        #                 self.state = i[1]
        #                 print("1      action-----------", best)
        #                 return i[0]



        count = 0
        random_number = random.randint(1, len(self.state.actions_successors()))
        for i in self.state.actions_successors():
            count += 1
            if count == random_number:
                self.state = i[1]
                print("2         action--------")
                return i[0]
        return ("PASS", None)

    def evaluation(self, node, root_colour):
        v = node.state.board.evaluation(root_colour, node.all_nodes)
        if len(node.state.board.players_hexes[self.colour]) + node.score[1] > 4 - self.score:
            v_1 = v[0] + node.score[1] * 2000
            v_2 = v[1] + node.score[2] * 2000
            v_3 = v[2] + node.score[3] * 2000
        elif len(node.state.board.players_hexes[self.colour]) + node.score[1] == 4 - self.score:
            v_1 = v[0] + node.score[1] * 1001
            v_2 = v[1] + node.score[2] * 1001
            v_3 = v[2] + node.score[3] * 1001
        else:
            v_1 = v[0] + node.score[1] * 500
            v_2 = v[1] + node.score[2] * 500
            v_3 = v[2] + node.score[3] * 500
        v = (v_1, v_2, v_3)
        # print(node.score)
        return v

    def MAXN(self, node, depth, current_player, alpha, root_colour):
        if depth <= 0:
            evaluate_result = self.evaluation(node, root_colour)
            # print("f: 1    ",node.state.board.players_hexes)
            # print("f: 1",node.state.board.colour, node.state.piece_hexes)
            # print("f: 1", "    d:", depth, "p:", current_player, "e:", evaluate_result)
            return (evaluate_result, node)

        best = (-100, -100, -100)
        best_node = node
        for c in node.children():
            maxn_result = self.MAXN(c, depth - 1, node.next_player, best[current_player - 1], root_colour)
            result = maxn_result[0]
            if result[current_player - 1] > best[current_player - 1]:
                best = result
                best_node = maxn_result[1]
        if depth == 3:
            # print("                                                             f: 3    ",node.state.board.players_hexes)
            # print("                                                             f: 3", node.state.board.colour, node.state.piece_hexes)
            # print("                                                             f: 3", "    d:", depth, "p:", current_player, "b:", best)
            return (best, best_node)
        # print("                                f: 2    ", node.state.board.players_hexes)
        # print("                                f: 2", node.state.board.colour, node.state.piece_hexes)
        # print("                                f: 2", "    d:", depth, "p:", current_player, "b:", best)
        return (best, best_node)

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

class Node:
    def __init__(self, colour, action, state, player, actions, score, all_nodes):
        self.all_nodes = all_nodes
        self.colour = colour
        self.state = state
        self.player = player
        self.next_player = 0
        self.last_player = 0
        if player == 1:
            self.next_player = 2
            self.last_player = 3
        elif player == 2:
            self.next_player = 3
            self.last_player = 1
        elif player == 3:
            self.next_player = 1
            self.last_player = 2
        self.action = action
        self.actions = actions
        self.actions.append((player, action))
        self.score = score
        if action[0] == "EXIT":
            print("---------EXIT")
            self.score[self.last_player] = self.score[self.last_player] + 1

    def children(self):
        children = []
        # print(self.player, self.state.board.colour)
        for i in self.state.colour_actions_successors():
            children.append(Node(self.colour, i[0], i[1], self.next_player, self.actions.copy(), self.score.copy(),
                                 self.all_nodes))
            # print(self.player, self.colour, i[1].board.colour)
        return children

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
        elif colour == 'green':
            self.exit_hexes = {(-3, 3), (-2, 3), (-1, 3), (0, 3)}
            self.piece_hexes = self.green_piece_hexes
            self.block_hexes = self.red_piece_hexes.copy()
            self.block_hexes.update(self.blue_piece_hexes)
        elif colour == 'blue':
            self.exit_hexes = {(-3, 0), (-2, -1), (-1, -2), (0, -3)}
            self.piece_hexes = self.blue_piece_hexes
            self.block_hexes = self.red_piece_hexes.copy()
            self.block_hexes.update(self.green_piece_hexes)

            # set of all hexes (for easy bounds checking):
        ran = range(-3, +3 + 1)
        self.all_hexes = {(q, r) for q in ran for r in ran if -q - r in ran}

    def safety(self, colour, all_nodes):
        self_colour = colour
        piece_hexes = self.players_hexes[self_colour]
        un_safe = []
        for piece in piece_hexes:
            (x1, y1) = piece
            for key in self.players_hexes:
                if key != self_colour:
                    for enemy in self.players_hexes[key]:
                        (x2, y2) = enemy
                        dis = (abs(x1 - x2) + abs(x1 + y1 - x2 - y2) + abs(y1 - y2)) / 2
                        if dis == 1:
                            # print(1)
                            x = enemy[0] + (piece[0] - enemy[0]) * 2
                            y = enemy[1] + (piece[1] - enemy[1]) * 2
                            move_to = (x, y)
                            # print(piece, enemy, move_to)
                            if move_to in all_nodes:
                                for i in self.players_hexes.values():
                                    if not (move_to in i):
                                        # piece is unsafe, check if enemy is safe
                                        changed_players_hexes = copy.deepcopy(self.players_hexes)
                                        changed_players_hexes[key].remove(enemy)
                                        changed_players_hexes[self_colour].remove(piece)
                                        changed_players_hexes[key].add(enemy)
                                        changed_players_hexes[key].add(piece)
                                        (c_x1, c_y1) = move_to
                                        enemy_not_safe = 0
                                        for c_key in changed_players_hexes:
                                            if c_key != key:
                                                for c_enemy in changed_players_hexes[c_key]:
                                                    (c_x2, c_y2) = c_enemy
                                                    dis = (abs(c_x1 - c_x2) + abs(c_x1 + c_y1 - c_x2 - c_y2) + abs(
                                                        c_y1 - c_y2)) / 2
                                                    if dis == 1:
                                                        x = c_enemy[0] + (piece[0] - c_enemy[0]) * 2
                                                        y = c_enemy[1] + (piece[1] - c_enemy[1]) * 2
                                                        c_move_to = (x, y)
                                                        if c_move_to in all_nodes:
                                                            for j in changed_players_hexes.values():
                                                                if not (c_move_to in j):
                                                                    enemy_not_safe = 1
                                                                    break
                                                    if enemy_not_safe == 1:
                                                        break
                                            if enemy_not_safe == 1:
                                                break
                                        if enemy_not_safe == 0:
                                            # add piece to un_safe if enemy is safe
                                            if not (piece in un_safe):
                                                un_safe.append(piece)
                                        break
                        if piece in un_safe:
                            break
                if piece in un_safe:
                    break
        # if len(un_safe) >= 1:
        #     print(colour, un_safe)
        return len(un_safe)

    def evaluation(self, root_colour, all_nodes):
        if root_colour == 'red':
            num_1 = len(self.players_hexes['red'])
            safe_1 = self.safety('red', all_nodes)
            h_1 = self.h('red')
            num_2 = len(self.players_hexes['green'])
            safe_2 = self.safety('green', all_nodes)
            h_2 = self.h('green')
            num_3 = len(self.players_hexes['blue'])
            safe_3 = self.safety('blue', all_nodes)
            h_3 = self.h('blue')
        if root_colour == 'green':
            num_1 = len(self.players_hexes['green'])
            safe_1 = self.safety('green', all_nodes)
            h_1 = self.h('green')
            num_2 = len(self.players_hexes['blue'])
            safe_2 = self.safety('blue', all_nodes)
            h_2 = self.h('blue')
            num_3 = len(self.players_hexes['red'])
            safe_3 = self.safety('red', all_nodes)
            h_3 = self.h('red')
        if root_colour == 'blue':
            num_1 = len(self.players_hexes['blue'])
            safe_1 = self.safety('blue', all_nodes)
            h_1 = self.h('blue')
            num_2 = len(self.players_hexes['red'])
            safe_2 = self.safety('red', all_nodes)
            h_2 = self.h('red')
            num_3 = len(self.players_hexes['green'])
            safe_3 = self.safety('green', all_nodes)
            h_3 = self.h('green')
        # print(h_1, h_2, h_3)
        v_1 = num_1 * 1000 - h_1 * 10 - safe_1
        v_2 = num_2 * 1000 - h_2 * 10 - safe_2
        v_3 = num_3 * 1000 - h_3 * 10 - safe_3
        # v_1 = - h_1
        # v_2 = - h_2
        # v_3 = - h_3
        return (v_1, v_2, v_3)

    def h(self, colour):
        hexes = self.players_hexes[colour]
        return sum(self.exit_dist(qr, colour) for qr in hexes)

    def exit_dist(self, qr, colour):
        """how many hexes away from a coordinate is the nearest exiting hex?"""
        q, r = qr
        if colour == 'red':
            return 3 - q
        elif colour == 'green':
            return 3 - r
        elif colour == 'blue':
            return 3 - (-q - r)

    def change_colour(self):
        if self.colour == 'red':
            self.colour = 'green'
            self.exit_hexes = {(-3, 3), (-2, 3), (-1, 3), (0, 3)}
        elif self.colour == 'green':
            self.colour = 'blue'
            self.exit_hexes = {(-3, 0), (-2, -1), (-1, -2), (0, -3)}
        elif self.colour == 'blue':
            self.colour = 'red'
            self.exit_hexes = {(3, -3), (3, -2), (3, -1), (3, 0)}
        self.piece_hexes = self.players_hexes[self.colour].copy()
        self.update_blocks()

    def update_board(self, colour, action):
        act = action[0];
        if act == "EXIT":
            move_from = action[1]
            self.players_hexes[colour].remove(move_from)
        elif act == "MOVE":
            move_from = action[1][0]
            move_to = action[1][1]
            self.players_hexes[colour].remove(move_from)
            self.players_hexes[colour].add(move_to)
        elif act == "JUMP":
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
        elif self.colour == 'green':
            self.block_hexes = self.players_hexes["red"].copy()
            self.block_hexes.update(self.players_hexes["blue"])
        elif self.colour == 'blue':
            self.block_hexes = self.players_hexes["red"].copy()
            self.block_hexes.update(self.players_hexes["green"])

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

    def colour_actions_successors(self):
        successors = self.actions_successors()
        for i in successors:
            new_board = copy.deepcopy(i[1].board)
            new_board.update_board(i[1].board.colour, i[0])
            new_board.change_colour()
            i[1].board = new_board
            i[1].piece_hexes = new_board.piece_hexes
        return successors

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