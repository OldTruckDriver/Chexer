"""
This module is used to simulate the max-n algorithm, which allows the player
to find the best action in a game with more than two players.
"""
from learning_player.utils import (PASS, EXIT_CELLS, TOTAL_DIST, TO_EXIT,
    CAN_EXIT, OPPONENT_EXITED, COLOURS, get_weights, evaluate, next_p, result)
from learning_player.state import State

# max depth of looking ahead
max_depth = 3

def get_best_action(state):
    weights = get_weights()
    return max_n(state, 0, state.colour, weights)[1]

# Inputs: state, colour of player
# Output: (utility vector, best action)
def max_n(state, depth, colour, weights):
    if depth >= len(COLOURS):
        return (evaluate(state, weights), (PASS, None))

    # 3 dimensions
    v_max = (-float('Inf'), -float('Inf'), -float('Inf'))
    best_action = (PASS, None)

    curr_player = COLOURS.index(colour)
    if (len(state.get_possible_actions(colour)) == 0):
        curr_player = next_p(state, curr_player)
        colour = COLOURS[curr_player]
    next_player = next_p(state, curr_player)

    for action in state.get_possible_actions(colour):
        v, _ = max_n(result(state, colour, action), depth + 1, COLOURS[next_player], weights)
        if v[curr_player] > v_max[curr_player]:
            v_max = v
            best_action = action
    return (v_max, best_action)
