from board import Board
from search import SearchProblem, ucs
import util


FREE = -1
Y = 0
X = 1
BIG_NUMBER = 100000000

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
        self.corners = ((0, 0), (board_w-1, 0), (0, board_h-1), (board_w-1, board_h-1))

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

        #util.raiseNotDefined()

    # def get_corners(self):
    #     return [i for i in self.corners]


def manhattan_heuristic(state, problem, targets):

    width = problem.board.board_w
    height = problem.board.board_h
    distance_to_targets = [BIG_NUMBER for i in targets]
    for y  in range(width):
        for x in range(height):
            if not state.get_position(y, x) == FREE:
                for i, target in enumerate(targets):
                    dist = util.manhattanDistance(target, (x,y))
                    if dist < distance_to_targets[i]:
                        distance_to_targets[i] = dist
    return sum(distance_to_targets)

def free_targets_heuristic(state, targets):
    free_targets = len(targets)
    for target in targets:
        if not state.get_position(target[Y], target[X]) == FREE:
            free_targets -= 1
    return free_targets


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

def combination_heuristic(state, problem, targets):
    # If the path to one of the targets is blocked
    if target_neighbors_heuristic(state, problem, targets):
        return BIG_NUMBER
    # heuristic_sum = free_targets_heuristic(state, targets)
    heuristic_sum = manhattan_heuristic(state, problem, targets)
    return heuristic_sum


def target_neighbors_heuristic(state, problem, targets):
    for target in targets:
        if state.get_position(target[Y], target[X]) == FREE:
            for neighbor in (get_adjacent(target, problem.board.board_w - 1, problem.board.board_h - 1)):
                if not state.get_position(neighbor[Y], neighbor[X]) == FREE:
                    return BIG_NUMBER
    return 0



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

    return combination_heuristic(state, problem, problem.corners)


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
        return cost   # TODO: is this KEFEL code ?


def blokus_cover_heuristic(state, problem):
    "*** YOUR CODE HERE ***"

    return combination_heuristic(state, problem, problem.targets)
    util.raiseNotDefined()


class ClosestLocationSearch:
    """
    In this problem you have to cover all given positions on the board,
    but the objective is speed, not optimality.
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0),
                 targets=(0, 0)):
        self.expanded = 0
        self.targets = targets.copy()
        "*** YOUR CODE HERE ***"

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def solve(self):
        """
        This method should return a sequence of actions that covers all target locations on the board.
        This time we trade optimality for speed.
        Therefore, your agent should try and cover one target location at a time. Each time, aiming for the closest uncovered location.
        You may define helpful functions as you wish.

        Probably a good way to start, would be something like this --

        current_state = self.board.__copy__()
        backtrace = []

        while ....

            actions = set of actions that covers the closets uncovered target location
            add actions to backtrace

        return backtrace
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


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
