import numpy as np
import abc
import util
from game import Agent, Action

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
        best_score = min(scores)
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

        # Useful information you can extract from a GameState (game_state.py)

        successor_game_state = current_game_state.generate_successor(action=action)
        smoothness_heuristic(successor_game_state)


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
        states = list()
        actions = game_state.get_legal_actions(OUR_AGENT)
        for action in actions:
            states.append((game_state.generate_successor(OUR_AGENT, action), action))  # (state, action_to_that_state)
        # return the action lead to max state
        return max([(self.min_value(state[0], 1), state[1]) for state in states], key=lambda x: x[0])[1]

    def max_value(self, game_state, depth):
        """
        our agent move in 2048 game
        :param game_state: current state
        :param depth: keep track to know when to stop
        :return: value of state
        """
        if depth == self.depth:
            return self.evaluation_function(game_state)

        depth += 1
        states = list()

        v = -np.inf  # minus infinity

        for action in game_state.get_legal_actions(OUR_AGENT):
            states.append(game_state.generate_successor(OUR_AGENT, action))
        for state in states:
            v = max(v, self.min_value(state, depth))
        return v

    def min_value(self, game_state, depth):
        """
        opponent move in 2048 game
        :param game_state: current state
        :param depth: keep track to know when to stop
        :return: value of state
        """
        if depth == self.depth:
            return self.evaluation_function(game_state)
        states = list()

        v = np.inf  # infinity

        for action in game_state.get_legal_actions(OPPONENT):
            states.append(game_state.generate_successor(OPPONENT, action))
        for state in states:
            v = min(v, self.max_value(state, depth))
        return v


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def get_action(self, game_state):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        states = list()
        actions = game_state.get_legal_actions(OUR_AGENT)
        for action in actions:
            states.append((game_state.generate_successor(OUR_AGENT, action), action))  # (state, action_to_that_state)
        # return the action lead to max state
        return max([(self.min_value(state[0], -np.inf, np.inf, 1), state[1]) for state in states], key=lambda x: x[0])[
            1]

    def max_value(self, game_state, a, b, depth):
        """
        our agent move in 2048 game
        :param game_state: current state
        :param depth: keep track to know when to stop
        :return: value of state
        """
        if depth == self.depth:
            return self.evaluation_function(game_state)

        depth += 1
        states = list()

        v = -np.inf  # minus infinity

        for action in game_state.get_legal_actions(OUR_AGENT):
            states.append(game_state.generate_successor(OUR_AGENT, action))
        for state in states:
            v = max(v, self.min_value(state, a, b, depth))
            if v >= b:
                return v
            a = max(a, v)
        return v

    def min_value(self, game_state, a, b, depth):
        """
        opponent move in 2048 game
        :param game_state: current state
        :param depth: keep track to know when to stop
        :return: value of state
        """
        if depth == self.depth:
            return self.evaluation_function(game_state)
        states = list()

        v = np.inf  # infinity

        for action in game_state.get_legal_actions(OPPONENT):
            states.append(game_state.generate_successor(OPPONENT, action))
        for state in states:
            v = min(v, self.max_value(state, a, b, depth))
            if v >= b:
                return v
            b = min(b, v)
        return v


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 4)
    """

    def get_action(self, game_state):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        The opponent should be modeled as choosing uniformly at random from their
        legal moves.
        """
        """*** YOUR CODE HERE ***"""
        util.raiseNotDefined()


def better_evaluation_function(current_game_state):
    """
    Your extreme 2048 evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    h1 = smoothness_heuristic(current_game_state)
    h2 = monotonicity_heuristic(current_game_state)
    # print("S: ", 5*h1/current_game_state.score, " M: ", current_game_state.score/h2, "T: ",  h1/current_game_state.score + current_game_state.score/h2)
    return 2.5*h1/current_game_state.score + current_game_state.score/h2

def monotonicity_heuristic(game_state):
    board = game_state.board
    score = 100

    for i in range(game_state._num_of_rows):
        row_grade = 0
        for j in range(game_state._num_of_columns - 1):
            difference =  board[i][j] - board[i][j + 1]
            if difference > 0:
                row_grade += 1
            elif difference < 0:
                row_grade -= 1
        score -= abs(row_grade)

    for j in range(game_state._num_of_columns):
        col_grade = 0
        for i in range(game_state._num_of_rows - 1):
            difference = board[i][j] - board[i + 1][j]
            if difference > 0:
                col_grade += 1
            elif difference < 0:
                col_grade -= 1
        score -= abs(col_grade)

    return score



def smoothness_heuristic(game_state):
    board = game_state.board
    # score = game_state.score
    sum_of_differences = 0
    for i in range(game_state._num_of_rows):
        for j in range(game_state._num_of_columns - 1):
            sum_of_differences += abs(board[i][j] - board[i][j + 1])
    for j in range(game_state._num_of_columns):
        for i in range(game_state._num_of_rows - 1):
            sum_of_differences += abs(board[i][j] - board[i + 1][j])
    # return 0 if sum_of_differences == 0 else sum_of_differences/score
    return sum_of_differences


# Abbreviation
better = better_evaluation_function
