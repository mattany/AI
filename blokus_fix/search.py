"""
In search.py, you will implement generic search algorithms
"""

import util

STATE = 0
ACTION = 1
COST = 2

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def is_goal_state(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()




def depth_first_search(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches
    the goal. Make sure to implement a graph search algorithm.
    """
    "*** YOUR CODE HERE ***"
    print("Start:", problem.get_start_state().state)
    print("Is the start a goal?", problem.is_goal_state(problem.get_start_state()))
    print("Start's successors:", problem.get_successors(problem.get_start_state()))
    #
    #
    start_state = problem.get_start_state()
    current_node = (None, start_state, None)
    stack = util.Stack()
    visited = set()
    stack.push(current_node)
    while not stack.isEmpty():
        current_node = stack.pop()
        neighbors = problem.get_successors(current_node[STATE])
        for neighbor in neighbors:
            if problem.is_goal_state(neighbor[STATE]):
                path = []
                while not stack.isEmpty() and current_node[STATE] != start_state:
                    path.insert(0, stack.pop()[ACTION])
                return path
        for neighbor in neighbors:
            if neighbor not in visited:
                stack.push(neighbor)
                visited.add(neighbor)
    # if any(problem.is_goal_state(neighbor) for neighbor in neighbors):
    # neighbors = problem.get_successors
    #
    # visited.add(current_node)
    # stack.push(current_node)
    # if problem.is_goal_state(current_node):
    #     path = []
    #     while not stack.isEmpty():
    #         path[0] = stack.pop()
    #     return path
    # while not stack.isEmpty():
    #     current_node = stack.pop()
    #     if current_node not in visited:
    #         visited.add(current_node)
    #         for neighbor in neighbors:
    #             stack.push(neighbor)
    util.raiseNotDefined()


def breadth_first_search(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


def uniform_cost_search(problem):
    """
    Search the node of least total cost first.
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


def null_heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def a_star_search(problem, heuristic=null_heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()



# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search
