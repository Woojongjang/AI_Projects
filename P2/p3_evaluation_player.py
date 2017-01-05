# -*- coding: utf-8 -*-
__author__ = 'wojang@ucsd.edu,A97105059,a1heng@ucsd.edu,A11308554,sharoon@ucsd.edu,A10938989'

from assignment2 import Player, State, Action


class EvaluationPlayer(Player):
    def move(self, state):
        """Calculates the best move after 1-step look-ahead with a simple
        evaluation function.
        :param state: State, the current state of the board.
        :return: Action, the next move
        """

        # *You do not need to modify this method.*
        best_value = -1.0

        actions = state.actions()
        if not actions:
            actions = [None]

        best_move = actions[0]
        for action in actions:
            result_state = state.result(action)
            value = self.evaluate(result_state, state.player_row)
            if value > best_value:
                best_value = value
                best_move = action

        # Return the move with the highest evaluation value
        return best_move

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

