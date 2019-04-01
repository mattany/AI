from board import Board
from search import SearchProblem, ucs
import util
import numpy as np

FREE = -1
Y = 0
X = 1
ILLEGAL_PATH = 100000000

STATE = 0
ACTION = 1


class BlokusFillProblem(SearchProblem):
    """
    A one-player Blokus game as a search problem.
    This problem is implemented for you. You should NOT change it!
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.expanded = 0

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        """
        state: Search state
        Returns True if and only if the state is a valid goal state
        """
        return not any(state.pieces[0])

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, 1) for move in
                state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves
        """
        return len(actions)


#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################
class BlokusCornersProblem(SearchProblem):
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.expanded = 0
        "*** YOUR CODE HERE ***"
        self.corners = (
            (0, 0), (board_w - 1, 0), (0, board_h - 1),
            (board_w - 1, board_h - 1))

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        """
        state: Search state
        Returns True if and only if the state is a valid goal state
        """
        "*** YOUR CODE HERE ***"
        for corner in self.corners:
            if state.get_position(corner[X], corner[Y]) == FREE:
                return False
        return True

        # util.raiseNotDefined()

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for
                move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves
        """
        "*** YOUR CODE HERE ***"
        cost = 0
        for move in actions:
            cost += move.piece.get_num_tiles()
        return cost


def get_adjacent(coordinates, maxY, maxX):
    y = coordinates[Y]
    x = coordinates[X]
    adjacent = list()
    if y + 1 <= maxY:
        adjacent.append((y + 1, x))
    if x + 1 <= maxX:
        adjacent.append((y, x + 1))
    if y - 1 >= 0:
        adjacent.append((y - 1, x))
    if x - 1 >= 0:
        adjacent.append((y, x - 1))
    return adjacent


def min_distances_to_targets(problem, state, distance_metric, targets):
    width = problem.board.board_w
    height = problem.board.board_h
    min_distances = [ILLEGAL_PATH for i in targets]
    for y in range(width):
        for x in range(height):
            if not state.get_position(y, x) == FREE:
                for i, target in enumerate(targets):
                    dist = distance_metric((x, y), target)
                    if dist < min_distances[i]:
                        min_distances[i] = dist
    return min_distances


def chebyshev_distance(xy1, xy2):
    return max(abs(xy1[Y] - xy2[Y]), abs(xy1[X] - xy2[X]))


def distance_heuristic(state, problem, targets):
    return max(min_distances_to_targets(problem, state, chebyshev_distance, targets))


def free_targets_heuristic(state, targets):
    """
    :return the number of free targets
    """
    free_targets = len(targets)
    for target in targets:
        if not state.get_position(target[Y], target[X]) == FREE:
            free_targets -= 1
    return free_targets


def dead_end_heuristic(state, problem, targets):
    for target in targets:
        if state.get_position(target[Y], target[X]) == FREE:
            for neighbor in (get_adjacent(target, problem.board.board_w - 1,
                                          problem.board.board_h - 1)):
                if not state.get_position(neighbor[Y], neighbor[X]) == FREE:
                    return ILLEGAL_PATH
    return 0


def frame_cost(state):
    width = state.board_w
    height = state.board_h
    return width * height - max(width - 2, 0) * max(height - 2, 0)


def min_needed_cost(state, targets):
    pieces = np.array(state.piece_list.pieces)
    sorted_available_pieces = sorted(pieces[np.where(state.pieces[0])], key=lambda x: x.num_tiles)
    number_of_targets_left = target_distances_heuristic(state, targets, sorted_available_pieces)
    if target_distances_heuristic(state, targets, sorted_available_pieces) == ILLEGAL_PATH:
        return ILLEGAL_PATH
    if number_of_targets_left > len(sorted_available_pieces):
        return ILLEGAL_PATH
    min_cost = 0
    index = number_of_targets_left - 1
    while index >= 0:
        min_cost += sorted_available_pieces[index].num_tiles
        index -= 1
    return min_cost


def combination_heuristic(state, problem, targets):
    # If the path to one of the targets is blocked
    if dead_end_heuristic(state, problem, targets):
        return ILLEGAL_PATH
    # return distance_heuristic(state, problem, targets)


def blokus_corners_heuristic(state, problem):
    """
    Your heuristic for the BlokusCornersProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come up
    with an admissible heuristic; almost all admissible heuristics will be consistent
    as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the other hand,
    inadmissible or inconsistent heuristics may find optimal solutions, so be careful.
    """

    return combination_heuristic(state, problem, list(problem.corners))


class BlokusCoverProblem(SearchProblem):
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0),
                 targets=[(0, 0)]):
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.targets = targets.copy()
        self.expanded = 0
        "*** YOUR CODE HERE ***"

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        for target in self.targets:
            if state.get_position(target[X], target[Y]) == FREE:
                return False
        return True

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for
                move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        "*** YOUR CODE HERE ***"

        cost = 0
        for move in actions:
            cost += move.piece.get_num_tiles()
        return cost


def blokus_cover_heuristic(state, problem):
    "*** YOUR CODE HERE ***"
    return combination_heuristic(state, problem, list(problem.targets))


def target_distances_heuristic(state, targets, sorted_available_pieces):
    # number_of_targets_left = free_targets_heuristic(state, targets)
    # pieces = np.array(state.piece_list.pieces)
    # sorted_available_pieces = sorted(pieces[np.where(state.pieces[0])], key=lambda x: x.num_tiles)
    max_tiles = ILLEGAL_PATH
    if len(sorted_available_pieces) > 0:
        max_tiles = sorted_available_pieces[-1].num_tiles
    else:
        return max_tiles
    maximum_discreet_nodes = 0
    for i in targets:
        discreet_target_set = {i}
        for j in targets:
            to_add = True
            for item in discreet_target_set:
                if (util.manhattanDistance(item, j) - 1) < max_tiles:
                    to_add = False
                    break
            if to_add:
                discreet_target_set.add(j)
        discreet_nodes = len(discreet_target_set)
        if discreet_nodes > maximum_discreet_nodes:
            maximum_discreet_nodes = discreet_nodes
    return maximum_discreet_nodes


class ClosestLocationSearch:
    """
    In this problem you have to cover all given positions on the board,
    but the objective is speed, not optimality.
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0),
                 targets=(0, 0)):
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.expanded = 0
        self.targets = targets.copy()

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        for target in self.targets:
            if state.get_position(target[X], target[Y]) == FREE:
                return False
        return True

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for
                move in state.get_legal_moves(0)]

    def solve(self):
        """
        This method should return a sequence of actions that covers all target
        locations on the board. This time we trade optimality for speed.
        Therefore, your agent should try and cover one target location at a time.
        Each time, aiming for the closest uncovered location.
        """
        backtrace = []
        current_state = self.get_start_state()
        while not self.is_goal_state(current_state):
            distances = min_distances_to_targets(self, current_state, util.manhattanDistance, self.targets)
            min_distance = min(i for i in distances if i > 0)
            # select the closest target base on the distance from each target
            target = self.targets[distances.index(min_distance)]
            # get closer to target each time until its covered
            while current_state.get_position(target[X], target[Y]) == FREE:
                best_action = None
                successors = self.get_successors(current_state)
                for successor in successors:
                    distance = min_distances_to_targets(self, successor[STATE], util.manhattanDistance, [target])[0]
                    if distance < min_distance:
                        min_distance = distance
                        current_state = successor[STATE]
                        best_action = successor[ACTION]
                backtrace.append(best_action)
        return backtrace


class MiniContestSearch:
    """
    Implement your contest entry here
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0),
                 targets=(0, 0)):
        self.targets = targets.copy()
        "*** YOUR CODE HERE ***"

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def solve(self):
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()
