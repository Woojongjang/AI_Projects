# -*- coding: utf-8 -*-
__author__ = 'wojang@ucsd.edu,A97105059,a1heng@ucsd.edu,A11308554,sharoon@ucsd.edu,A10938989'

from assignment2 import Player, State, Action

class MinimaxPlayer(Player):
    def __init__(self):
        self.cache ={}

    def max_val(self, state):

        # Base case
        if state.is_terminal():
            self.cache[state.ser()] = state.utility(self)
            return self.cache[state.ser()]
        v = -1

        # No possible moves
        actions = state.actions()
        if len(actions) == 0:
            actions = [None]
        for action in actions:
            nextState = state.result(action)

            # Check cache for next state
            if nextState.ser() in self.cache:
                v = max(v, self.cache[nextState.ser()])
            else:
                v = max(v, self.min_val(nextState))

        # Cache this state
        self.cache[state.ser()] = v;
        return v

    def min_val(self, state):

        # Base case
        if state.is_terminal():
            self.cache[state.ser()] = state.utility(self)
            return self.cache[state.ser()]
        v = 1

        # No possible moves
        actions = state.actions()
        if len(actions) == 0:
            actions = [None]
        for action in actions:
            nextState = state.result(action)

            # Check cache for next state
            if nextState.ser() in self.cache:
                v = min(v, self.cache[nextState.ser()])
            else:
                v = min(v, self.max_val(nextState))

        # Cache this state
        self.cache[state.ser()] = v;
        return v

    def move(self, state):
        """
        Calculates the best move from the given board using the minimax
        algorithm.
        :param state: State, the current state of the board.
        :return: Action, the next move
        """
        # Calculate utility from minimax-alpha-beta
        v = self.max_val(state)

        # Search for action/state with utility v
        for a in state.actions():
            choice = state.result(a)
            if self.cache[choice.ser()] == v:
                return a;
        return None