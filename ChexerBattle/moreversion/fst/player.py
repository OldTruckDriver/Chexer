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
        if self.colour == 'red':
            self.colours = ('red', 'green', 'blue')
        elif self.colour == 'green':
            self.colours = ('green', 'blue', 'red')
        elif self.colour == 'blue':
            self.colours = ('blue', 'red', 'green')
        self.board = Board(colour, self.colours)
        self.state = State(self.board.piece_hexes, self.board)
        self.score = {self.colours[0]: 0, self.colours[1]: 0, self.colours[2]: 0}
        self.cases = [('safety', 'killed'), ('safety', ''
                                                       ''), ('safety', 'killed')]

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
        root_action = ("PASS", None)
        root_actions = ((4, ("PASS", None)))
        root_player = 1
        root_state = copy.deepcopy(self.state)
        root_score = (0, 0, 0)
        ran = range(-3, +3 + 1)
        all_nodes = []
        for qr in ((q, r) for q in ran for r in ran if -q - r in ran):
            all_nodes.append(qr)
        all_nodes = tuple(all_nodes)
        root_killed = (0, 0, 0)

        root = Node(root_action, root_state, root_player, root_actions, root_score, all_nodes,
                    root_killed)

        # set additional evaluation case according to pieces a player have
        # self.cases[0] = ('killed', 'safety', 'danger')
        # self.cases[1] = ('killed', 'safety', 'danger')
        # self.cases[2] = ('killed', 'safety', 'danger')
        self.cases[0] = ('killed', 'danger', 'safety')
        self.cases[1] = ('killed', 'danger', 'safety')
        self.cases[2] = ('killed', 'danger', 'safety')
        # player_index = 0
        # for colour in self.colours:
        #     num_pieces = len(self.board.players_hexes[colour]) + self.score[colour]
        #     if num_pieces < 4:
        #         self.cases[player_index] = ('killed', 'safety', 'danger')
        #     elif num_pieces == 4:
        #         self.cases[player_index] = ('killed', 'safety', 'danger')
        #     elif num_pieces > 4:
        #         self.cases[player_index] = ('danger', 'safety', 'killed')
        #     player_index = player_index + 1
        print(self.cases)
        print(self.score)

        # maxn return a best action and a best node
        maxn_value = self.MAXN(root, maximum_depth, root_player)
        best = maxn_value[0]
        best_node = maxn_value[1]

        print(best)
        print(best_node.state.board.players_hexes)
        print(best_node.actions)
        print(best_node.action)
        print("--------------best!!!!!!!!!")
        print(best_node.actions[2][1])

        best_action = best_node.actions[2][1]

        # if an action is able to take to win, then do it
        if self.score[self.colour] == 3:
            print(self.score[self.colour])
            for i in self.state.actions_successors():
                if i[0][0] == "EXIT":
                    return i[0]

        for i in self.state.actions_successors():
            if i[0] == best_action:
                print("0      action-----------", best)
                return i[0]

        count = 0
        random_number = random.randint(1, len(self.state.actions_successors()))
        for i in self.state.actions_successors():
            count += 1
            if count == random_number:
                self.state = i[1]
                print("2         action--------")
                return i[0]
        return ("PASS", None)

    def MAXN(self, node, depth, current_player):
        evaluate_player = node.last_player
        if depth <= 0:
            v = self.evaluation(node, evaluate_player)
            evaluate_result = (-100, -100, v)
            return (evaluate_result, node)

        best = (-100, -100, -100)
        best_node = node
        for c_node in node.children():
            maxn_result = self.MAXN(c_node, depth - 1, node.next_player)
            result = maxn_result[0]
            result_node = maxn_result[1]

            # calculate the evaluation value for the player
            # print(current_player)
            # print(current_player)
            if current_player != 3:
                result = list(result)
                evaluate_result = self.evaluation(result_node, current_player)
                result[current_player - 1] = evaluate_result
                result = tuple(result)

            # compare current player's evaluation value
            if result[current_player - 1] > best[current_player - 1]:
                # if (best[2] != -100):
                #     print('--------------------best')
                #     print(best)
                #     print(best)
                best = result
                best_node = result_node
            elif result[current_player - 1] == best[current_player - 1]:
                # if evaluate_player == 1:
                #     print(evaluate_player, self.colours[evaluate_player - 1], self.cases[evaluate_player - 1])
                # if evaluate_player == 2:
                #     print("   ", evaluate_player, self.colours[evaluate_player - 1], self.cases[evaluate_player - 1])
                # if evaluate_player == 3:
                #     print("        ", evaluate_player, self.colours[evaluate_player - 1], self.cases[evaluate_player - 1])

                case_index = 0
                for case in self.cases[current_player - 1]:
                    result_ae = self.additional_evaluation(result_node, current_player, case)
                    if best_node.best_case_result[case_index] == -1000000:
                        best_ae = self.additional_evaluation(best_node, current_player, case)
                        best_node.best_case_result[case_index] = best_ae
                    # if current_player == 1:
                            # print(self.cases[current_player - 1])
                            # print(case_index, result_ae, best_node.best_case_result)
                            # print(best_node.state.board.players_hexes)
                            # print(result_node.state.board.players_hexes)
                    if result_ae > best_node.best_case_result[case_index]:
                        # print("changebest")
                        # if current_player == 1:
                        #     print("changebest")
                        # print(case)
                        best_node = result_node
                        best_node.best_case_result[case_index] = result_ae
                        break
                    if result_ae < best_node.best_case_result[case_index]:
                        break
                    case_index = case_index + 1


        # if depth == 3:
            # print("f: 1    ", best_node.state.board.players_hexes)
            # print("f: 1", best_node.state.board.colour, best_node.state.piece_hexes)
            # print("f: 1", "    d:", depth, "p:", current_player, "b:", best, best_node.best_case_result, self.colours[current_player - 1])
        return (best, best_node)

    def evaluation(self, node, evaluate_player):
        player = evaluate_player
        # if player == 1:
        #     print(player)
        # if player == 2:
        #     print("   ", player)
        # if player == 3:
        #     print("        ", player)
        current_index = player - 1
        current_board = node.state.board
        # weight for num of pieces
        w_num = 1000

        # weight for exit
        w_score = 0
        num_to_exit = 4 - self.score[self.colours[player - 1]]
        num_have = len(node.state.board.players_hexes[self.colours[player - 1]]) + node.score[player - 1]
        if num_have > num_to_exit:
            w_score = 2000
        elif num_have == num_to_exit:
            w_score = 1000

        # weight for move to exit
        w_h = 0
        if self.score[self.colours[player - 1]] + len(current_board.players_hexes[self.colours[player - 1]]) >= 4:
            w_h = 10

        # calculate evaluation value v
        num_pieces = len(current_board.players_hexes[self.colours[current_index]]) * w_num
        exit_score = node.score[player - 1] * w_score
        exit_distance = current_board.dis_exit(self.colours[current_index]) * w_h
        v = num_pieces + exit_score - exit_distance
        # if player == 1:
        #     if num_pieces > 4500:
        #         print(num_pieces)
        #         print(v)
        #         print(current_board.players_hexes)
        return v

    # more evaluation made if there is a tie
    def additional_evaluation(self, node, evaluate_player, case):
        player = evaluate_player
        current_board = node.state.board
        colour_compare = self.colours[player - 1]
        if case == 'danger':
            num = -1 * current_board.danger(colour_compare, node.all_nodes)
        elif case == 'safety':
            num = -1 * current_board.safety(colour_compare)
            # print(current_board.players_hexes[colour_compare])
            # print(num)
        elif case == 'killed':
            num = node.killed[player - 1]
        return num

    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player???s 
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
        if action[0] == "EXIT":
            print('------EXIT------')
            self.score[colour] = self.score[colour] + 1
        print(self.score)


class Node:
    def __init__(self, action, state, player, actions, score, all_nodes, killed):
        self.all_nodes = all_nodes
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
        self.score = score
        self.killed = killed
        self.best_case_result = [-1000000, -1000000, -1000000]

    def children(self):
        children = []
        for i in self.state.colour_actions_successors():
            action = i[0]
            state = i[1]
            actions = list(self.actions)
            killed = list(self.killed)
            score = list(self.score)
            actions.append((self.player, action))
            if action[0] == "JUMP":
                if len(self.state.piece_hexes) > len(state.piece_hexes):
                    killed[self.player - 1] = killed[self.player - 1] + 1
            elif action[0] == "EXIT":
                score[self.player - 1] = score[self.player - 1] + 1
            killed = tuple(killed)
            score = tuple(score)
            actions = tuple(actions)
            children.append(Node(action, state, self.next_player, actions, score, self.all_nodes, killed))
        return children


class Board:
    """
    Represent an (empty) single-player Chexers game board
    (it's just a grid of hexes, some of which are blocked)
    """

    def __init__(self, colour, colours):
        """
        Board constructor
        - colour is a string 'red', 'green', or 'blue' (determines exit edge)
        - blocks is an iterable of the coordinates of hexes occupied by blocks
        """
        self.colour = colour
        self.colours = colours
        self.players_hexes= {
            'red': {(-3, 3), (-3, 2), (-3, 1), (-3, 0)},
            'green': {(0, -3), (1, -3), (2, -3), (3, -3)},
            'blue': {(3, 0), (2, 1), (1, 2), (0, 3)},
        }

        if colour == 'red':
            self.exit_hexes = {(3, -3), (3, -2), (3, -1), (3, 0)}
            self.piece_hexes = self.players_hexes['red']
            self.block_hexes = self.players_hexes['green'].copy()
            self.block_hexes.update(self.players_hexes['blue'])
        elif colour == 'green':
            self.exit_hexes = {(-3, 3), (-2, 3), (-1, 3), (0, 3)}
            self.piece_hexes = self.players_hexes['green']
            self.block_hexes = self.players_hexes['red'].copy()
            self.block_hexes.update(self.players_hexes['blue'])
        elif colour == 'blue':
            self.exit_hexes = {(-3, 0), (-2, -1), (-1, -2), (0, -3)}
            self.piece_hexes = self.players_hexes['blue']
            self.block_hexes = self.players_hexes['red'].copy()
            self.block_hexes.update(self.players_hexes['green'])

        # set of all hexes (for easy bounds checking):
        ran = range(-3, +3 + 1)
        self.all_hexes = {(q, r) for q in ran for r in ran if -q - r in ran}

    def safety(self, colour):
        safety = 0
        piece_hexes = self.players_hexes[colour]
        for piece in piece_hexes:
            (x1, y1) = piece
            for friend_piece in piece_hexes:
                if piece != friend_piece:
                    (x2, y2) = friend_piece
                    dis = (abs(x1 - x2) + abs(x1 + y1 - x2 - y2) + abs(y1 - y2)) / 2
                    safety = safety + dis
        return safety

    def danger(self, colour, all_nodes):
        # print()
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
                                        # piece is unsafe if no friend protection
                                        have_protection = 0
                                        for piece_friend in self.players_hexes[self_colour]:
                                            (f_x2, f_y2) = piece_friend
                                            f_dis = (abs(x1 - f_x2) + abs(x1 + y1 - f_x2 - f_y2) + abs(y1 - f_y2)) / 2
                                            if f_dis == 1:
                                                f_x = piece_friend[0] + (piece[0] - piece_friend[0]) * 2
                                                f_y = piece_friend[1] + (piece[1] - piece_friend[1]) * 2
                                                f_move_to = (f_x, f_y)
                                                # print(piece, enemy, move_to)
                                                if f_move_to in all_nodes:
                                                    for f in self.players_hexes.values():
                                                        if not(f_move_to in f):
                                                            have_protection = 1
                                                            break
                                            if have_protection == 1:
                                                break
                                        if have_protection == 0:
                                            if not (piece in un_safe):
                                                un_safe.append(piece)
                                            break
                                        # piece is unsafe, but have friend piece, check if enemy is threaten by friend
                                        if len(self.players_hexes[self_colour]) < 4:
                                            if not (piece in un_safe):
                                                un_safe.append(piece)
                                            break
                                        else:
                                            changed_players_hexes = copy.deepcopy(self.players_hexes)
                                            changed_players_hexes[key].remove(enemy)
                                            changed_players_hexes[self_colour].remove(piece)
                                            changed_players_hexes[key].add(enemy)
                                            changed_players_hexes[key].add(piece)
                                            (c_x1, c_y1) = move_to
                                            enemy_not_safe = 0
                                            # for c_key in changed_players_hexes:
                                            #     if c_key != key:
                                            for c_enemy in changed_players_hexes[self_colour]:
                                                (c_x2, c_y2) = c_enemy
                                                dis = (abs(c_x1 - c_x2) + abs(c_x1 + c_y1 - c_x2 - c_y2) + abs(
                                                    c_y1 - c_y2)) / 2
                                                if dis == 1:
                                                    c_x = c_enemy[0] + (move_to[0] - c_enemy[0]) * 2
                                                    c_y = c_enemy[1] + (move_to[1] - c_enemy[1]) * 2
                                                    c_move_to = (c_x, c_y)
                                                    if c_move_to in all_nodes:
                                                        for j in changed_players_hexes.values():
                                                            if not (c_move_to in j):
                                                                enemy_not_safe = 1
                                                                break
                                                if enemy_not_safe == 1:
                                                    break
                                                # if enemy_not_safe == 1:
                                                #     break
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

    def dis_exit(self, colour):
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
        act = action[0]
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