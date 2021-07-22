import json
import numpy as np
from learning_player.utils import (PASS, COLOURS, get_weights, evaluate, next_p, result, myeval)
from learning_player.state import dict_to_state

def get_states():
    with open('learning_player/states.json') as json_file:
        states = json.load(json_file)
        for i in range(0, len(states)):
            for colour, pieces in states[i]['piece_locs'].items():
                pieces = [tuple(p) for p in pieces ]
                states[i][colour] = pieces
        return states

def update_weights(l, states):
    weights = get_weights()

    colour = states[0]['colour']

    for feature in list(weights.keys()):
        w = weights[feature]
        newW = w
        for j in range(0, len(states) - 1):

            curr_state = dict_to_state(states[j])
            next_state = dict_to_state(states[j + 1])
            curr_score = myeval(curr_state, weights, colour)
            next_score = myeval(next_state, weights, colour)

            td = np.tanh(next_score) - np.tanh(curr_score)
            newW += 1000 * (((1 / np.cosh(curr_score)) ** 2) * curr_state.get_feature(feature, colour) * td)
        weights[feature] = newW

    with open('learning_player/weight.json', 'w') as json_file:
        json.dump(weights, json_file)

def reset_states(state):
    with open('learning_player/states.json', 'w') as json_file:
        json.dump([state.__dict__], json_file)

def learning():
    states = get_states()
    update_weights(0, states)


def write_best_leaf(state):
    weights = get_weights()
    _, _, best_leaf = get_best_leaf(state, 0, state.colour, weights)
    best_leaf.write_to_file()

def get_best_leaf(state, depth, colour, weights):
    if depth >= len(COLOURS):
        return (evaluate(state, weights), (PASS, None), state)

    # 3 dimensions
    v_max = (-float('Inf'), -float('Inf'), -float('Inf'))
    best_action = (PASS, None)
    curr_player = COLOURS.index(colour)
    next_player = next_p(state, curr_player)
    best_leaf = None

    if (len(state.get_possible_actions(colour)) == 0):
        curr_player = next_p(state, curr_player)
        next_player = next_p(state, curr_player)
        colour = COLOURS[curr_player]

    for action in state.get_possible_actions(colour):
        v, _, leaf = get_best_leaf(result(state, colour, action), depth + 1, COLOURS[next_player], weights)
        if v[curr_player] > v_max[curr_player]:
            v_max = v
            best_action = action
            best_leaf = leaf
    return (v_max, best_action, best_leaf)
