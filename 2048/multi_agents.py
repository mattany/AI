import numpy as np
import abc
import math
import util
from game import Agent, Action

ROW = 0
COL = 1

ACTION = 1

STATE = 0

VERBOSE = False


# scalars
RADIAL = 0
ROUGH = 0
STEEP = 1
SMOOTH = 83.5
MONOTONE = 0
FREE_TILES = 0
MAX_TILE = 0

OUR_AGENT = 0
OPPONENT = 1
MAX = True
MIN = False


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def get_action(self, game_state):
        """
        You do not need to change this method, but you're welcome to.

        get_action chooses among the best options according to the evaluation function.


        get_action takes a game_state and returns some Action.X for some X in the set {UP, DOWN, LEFT, RIGHT, STOP}
        """

        # Collect legal moves and successor states
        legal_moves = game_state.get_agent_legal_actions()

        # Choose one of the best actions
        scores = [self.evaluation_function(game_state, action) for action in legal_moves]
        best_score = max(scores)
        best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
        chosen_index = np.random.choice(best_indices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legal_moves[chosen_index]

    def evaluation_function(self, current_game_state, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (GameState.py) and returns a number, where higher numbers are better.

        """
        successor_game_state = current_game_state.generate_successor(action=action)
        return -roughness_heuristic(successor_game_state)


def score_evaluation_function(current_game_state):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return current_game_state.score


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinmaxAgent, AlphaBetaAgent & ExpectimaxAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evaluation_function='scoreEvaluationFunction', depth=2):
        self.evaluation_function = util.lookup(evaluation_function, globals())
        self.depth = depth

    @abc.abstractmethod
    def get_action(self, game_state):
        return



class MinmaxAgent(MultiAgentSearchAgent):
    def get_action(self, game_state):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        game_state.get_legal_actions(agent_index):
            Returns a list of legal actions for an agent
            agent_index=0 means our agent, the opponent is agent_index=1

        Action.STOP:
            The stop direction, which is always legal

        game_state.generate_successor(agent_index, action):
            Returns the successor game state after an agent takes an action
        """
        actions = game_state.get_legal_actions(OUR_AGENT)
        states = [(game_state.generate_successor(OUR_AGENT, action), action) for action in actions]

        # The first maximizing agent call. Needed to get the successor state
        # that yields the best score, rather than the score by itself.
        return max([(self.min_value(state[STATE], self.depth), state[ACTION]) for state in states],
                   key=lambda x: x[STATE])[ACTION]

    def max_value(self, game_state, depth):
        """
        our agent move in 2048 game
        :param game_state: current state
        :param depth: keep track to know when to stop
        :return: value of state
        """
        if depth == 0:
            return self.evaluation_function(game_state)

        actions = game_state.get_legal_actions(OUR_AGENT)
        states = [(game_state.generate_successor(OUR_AGENT, action)) for action in actions]
        value = -np.inf  # minus infinity

        for state in states:
            value = max(value, self.min_value(state, depth))
        return value

    def min_value(self, game_state, depth):
        """
        opponent move in 2048 game
        :param game_state: current state
        :param depth: keep track to know when to stop
        :return: value of state
        """

        actions = game_state.get_legal_actions(OPPONENT)
        states = [(game_state.generate_successor(OPPONENT, action)) for action in actions]
        value = np.inf  # infinity

        for state in states:
            value = min(value, self.max_value(state, depth - 1))
        return value


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def get_action(self, game_state):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        actions = game_state.get_legal_actions(OUR_AGENT)
        states = [(game_state.generate_successor(OUR_AGENT, action), action) for action in actions]

        # The first maximizing agent call. Needed to get the successor state that yields the best score, rather than the
        # score by itself.
        return max([(self.min_value(state[STATE], -np.inf, np.inf, self.depth), state[ACTION]) for state in states],
                   key=lambda x: x[STATE])[ACTION]

    def max_value(self, game_state, alpha, beta, depth):
        """
        our agent move in 2048 game
        :param game_state: current state
        :param depth: keep track to know when to stop
        :return: value of state
        """

        if depth == 0:
            return self.evaluation_function(game_state)

        actions = game_state.get_legal_actions(OUR_AGENT)
        states = [game_state.generate_successor(OUR_AGENT, action) for action in actions]
        value = -np.inf  # minus infinity

        for state in states:
            value = max(value, self.min_value(state, alpha, beta, depth))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value

    def min_value(self, game_state, alpha, beta, depth):
        """
        opponent move in 2048 game
        :param game_state: current state
        :param depth: keep track to know when to stop
        :return: value of state
        """

        actions = game_state.get_legal_actions(OPPONENT)
        states = [game_state.generate_successor(OPPONENT, action) for action in actions]
        value = np.inf  # infinity

        for state in states:
            value = min(value, self.max_value(state, alpha, beta, depth - 1))
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 4)
    """

    def get_action(self, game_state):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        game_state.get_legal_actions(agent_index):
            Returns a list of legal actions for an agent
            agent_index=0 means our agent, the opponent is agent_index=1

        Action.STOP:
            The stop direction, which is always legal

        game_state.generate_successor(agent_index, action):
            Returns the successor game state after an agent takes an action
        """
        actions = game_state.get_legal_actions(OUR_AGENT)
        states = [(game_state.generate_successor(OUR_AGENT, action), action) for action in actions]

        # The first maximizing agent call. Needed to get the successor state that yields the
        # best score, rather than the score by itself.
        return max([(self.expected_value(state[STATE], self.depth), state[ACTION]) for state in states],
                   key=lambda x: x[STATE])[ACTION]

    def max_value(self, game_state, depth):
        """
        our agent move in 2048 game
        :param game_state: current state
        :param depth: keep track to know when to stop
        :return: value of state
        """

        if depth == 0:
            return self.evaluation_function(game_state)

        actions = game_state.get_legal_actions(OUR_AGENT)
        states = [(game_state.generate_successor(OUR_AGENT, action)) for action in actions]
        value = -np.inf  # minus infinity

        for state in states:
            value = max(value, self.expected_value(state, depth))
        return value

    def expected_value(self, game_state, depth):
        """
        opponent move in 2048 game
        :param game_state: current state
        :param depth: keep track to know when to stop
        :return: value of state
        """

        actions = game_state.get_legal_actions(OPPONENT)
        states = [(game_state.generate_successor(OPPONENT, action)) for action in actions]
        value = sum(self.max_value(state, depth - 1) for state in states)/len(states)
        return value


def better_evaluation_function(current_game_state):
    """
    Your extreme 2048 evaluation function (question 5).

    DESCRIPTION: A weighted sum of 2 heuristic functions. Each function is described in its own
    docstring
    """
    h1 = smoothness_heuristic(current_game_state) * SMOOTH
    h5 = steepness_heuristic(current_game_state) * STEEP
    return h1 + h5


def log_2(number):
    return math.log(number, 2)


def steepness_heuristic(game_state):
    """
    :param game_state: a given game state
    :return: The steepness score of the board, defined by a weight matrix that gives higher scores
    to boards that focus the weight in one corner.
    Note that the given matrix works only for 4x4 boards.
    """
    board = game_state.board
    score = 0
    weight_matrix = [[0, 1, 2, 3],
                     [1, 2, 3, 4],
                     [2, 3, 4, 5],
                     [3, 4, 5, 6]]
    for i in range(game_state._num_of_rows):
        for j in range(game_state._num_of_columns):
            score += weight_matrix[i][j] * board[i][j]
    return score


def smoothness_heuristic(game_state):
    """
    :param game_state: a given game state
    :return: The smoothness score of the board, defined as the negative of the sum of differences
    between adjacent tiles on a board. The differences are in base 2 to signify the number of tile
    merges needed for the lower tile to reach the higher tile
    """
    board = game_state.board
    sum_of_differences = 0
    coords = [(i, j) for i in range(game_state._num_of_rows) for j in range(game_state._num_of_columns) if board[i][j]]
    for coord in coords:
        i = coord[ROW]
        j = coord[COL]
        if i + 1 < game_state._num_of_rows and board[i + 1][j] != 0:
            sum_of_differences += abs(log_2(board[i + 1][j]) - log_2(board[i][j]))
        if j + 1 < game_state._num_of_columns and board[i][j + 1] != 0:
            sum_of_differences += abs(log_2(board[i][j]) - log_2(board[i][j + 1]))

    return -sum_of_differences


def roughness_heuristic(game_state):
    """
    :param game_state: a given game state
    :return: same as smoothness, but without log. This worked better for reflex agent.
    """
    board = game_state.board
    # score = game_state.score
    sum_of_differences = 0
    for i in range(game_state._num_of_rows):
        for j in range(game_state._num_of_columns - 1):
            sum_of_differences += abs(board[i][j] - board[i][j + 1])
    for j in range(game_state._num_of_columns):
        for i in range(game_state._num_of_rows - 1):
            sum_of_differences += abs(board[i][j] - board[i + 1][j])
    return sum_of_differences


# Abbreviation
better = better_evaluation_function
