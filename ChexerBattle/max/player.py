from max.state import (State, MOVE, JUMP, EXIT, PASS)
from max.max_n import get_best_action

import math
import random
import time

class ExpertPlayer:
    def __init__(self, colour):
        """
        Set up state representation.
        """
        self.state = State(colour)
        self.start_time = time.time()


    def action(self):
        """
        Decide what action to take.
        """
        possible_actions = self.state.get_possible_actions(self.state.colour)

        if (len(possible_actions) == 0):
            return (PASS, None)
        elif (time.time() - self.start_time) > 52:
            return random.choice(possible_actions)
        else:
            return get_best_action(self.state)


    def update(self, colour, action):
        """
        Update state representation in response to action.
        """
        self.state.update(colour, action)
