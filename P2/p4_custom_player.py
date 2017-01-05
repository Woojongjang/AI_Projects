# -*- coding: utf-8 -*-

__author__ = 'wojang@ucsd.edu,A97105059,a1heng@ucsd.edu,A11308554,sharoon@ucsd.edu,A10938989'

from assignment2 import Player, State, Action


class AlvinPlayer(Player):
    """The custom player implementation.
    """

    def __init__(self):
        """Called when the Player object is initialized. You can use this to
        store any persistent data you want to store for the  game.

        For technical people: make sure the objects are picklable. Otherwise
        it won't work under time limit.
        """
        self.cache ={}

    def evaluate(self, state, my_row):
        """
        Evaluates the state for the player with the given row
        """
        if my_row == 0:
            evalret = float (state.board[State.M] - state.board[((2*State.M)+1)] + (self.numberOfStones(state))[0] - (self.numberOfStones)(state)[1])/(2 * State.M * State.N)
        else:
            evalret = float (state.board[((2*State.M)+1)] - state.board[State.M] + (self.numberOfStones(state))[1] - (self.numberOfStones)(state)[0])/(2 * State.M * State.N)

        return evalret

    def numberOfStones(self, state):
        bottomStones = 0
        upperStones = 0
        for i in state.board[0:(State.M)]:
            bottomStones += i
        for i in state.board[(State.M + 1):(2*State.M+1)]:
            upperStones += i
        return (bottomStones,upperStones)

    def max_val(self, state, alpha, beta, depth):

        # Base case
        if depth == 0 or self.is_time_up():
            if state.is_terminal():
                self.cache[state.ser()] = state.utility(self)
            else:
                self.cache[state.ser()] = self.evaluate(state, state.player_row)
            return self.cache[state.ser()], alpha, beta
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
                tmp, alpha, beta = self.min_val(nextState, alpha, beta, depth - 1)
                v = max(v, tmp)

            if self.is_time_up():
                return v

        # Cache this state
        self.cache[state.ser()] = v;

        # (Prune and) update parent beta value
        if v >= beta:
            return v, alpha, beta
        alpha = max(alpha, v)
        return v, alpha, beta

    def min_val(self, state, alpha, beta, depth):

        if depth == 0 or self.is_time_up():
            if state.is_terminal():
                self.cache[state.ser()] = state.utility(self)
            else:
                self.cache[state.ser()] = self.evaluate(state, state.player_row)
            return self.cache[state.ser()], alpha, beta
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
                tmp, alpha, beta = self.max_val(nextState, alpha, beta, depth - 1)
                v = min(v, tmp)

            if self.is_time_up():
                return v

        # Cache this state
        self.cache[state.ser()] = v;

        # (Prune and) Update parent alpha value
        if v <= alpha:
            return v, alpha, beta
        beta = min(beta, v)
        return v, alpha, beta

    def move(self, state):
        """
        You're free to implement the move(self, state) however you want. Be
        run time efficient and innovative.
        :param state: State, the current state of the board.
        :return: Action, the next move
        """

        # Calculate utility from minimax-alpha-beta
        min_utility = -1
        max_utility = 1
        best_action, best_utility = None, min_utility
        depth = 1
        while (not self.is_time_up() and depth < 1000): # arbitrary depth for testing (useless)
            v, alpha, beta = self.max_val(state, min_utility, max_utility, depth - 1)

            # Search for action/state with utility v
            for a in state.actions():
                choice = state.result(a)
                if choice.ser() in self.cache and self.cache[choice.ser()] == v and best_utility < v:
                    best_action, best_utility = a, v;
            depth = depth + 1
        return best_action