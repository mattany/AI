"""
In search.py, you will implement generic search algorithms
"""

import util



PATH = 1


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
    #
    # start_state = problem.get_start_state()
    # cur_node = (start_state, None, None)
    # actions = list()
    # stack = util.Stack()
    # visited = {cur_node}
    # stack.push(cur_node)
    # while not stack.isEmpty():
    #     prev_node = cur_node
    #     cur_node = stack.pop()
    #     if cur_node[STATE] != start_state:
    #         actions.append((cur_node[ACTION], prev_node[STATE], cur_node[STATE]))
    #     neighbors = problem.get_successors(cur_node[STATE])
    #     if any(neighbor not in visited for neighbor in neighbors):
    #         for neighbor in neighbors:
    #             if problem.is_goal_state(neighbor[STATE]):
    #                 actions.append((neighbor[ACTION], cur_node[STATE], neighbor[STATE]))
    #                 return [i[MOVE] for i in actions]
    #         for neighbor in neighbors:
    #             if neighbor not in visited:
    #                 stack.push(neighbor)
    #                 visited.add(neighbor)
    #     else:
    #         last_action = actions[-1]
    #         while last_action[SRC] not in neighbors:
    #             if len(actions) > 0:
    #                 del actions[-1]
    #             if len(actions) > 0:
    #                 last_action = actions[-1]
    #
    #
    return []
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
    start_state = problem.get_start_state()
    current = (start_state, [], 0)
    fringe = util.PriorityQueue()
    visited = set()
    fringe.push(current, current[COST])
    while not fringe.isEmpty():
        current = fringe.pop()
        if problem.is_goal_state(current[STATE]):
            return current[PATH]
        elif current[STATE] not in visited:
            neighbors = problem.get_successors(current[STATE])
            for triplet in neighbors:
                path_to = current[PATH]
                path_to.append(triplet[ACTION])
                neighbor = (triplet[STATE], path_to, current[COST]+triplet[COST])
                fringe.push(neighbor, neighbor[COST])
            visited.add(current[STATE])
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
    start_state = problem.get_start_state()
    current = (start_state, [], heuristic(start_state, problem))
    fringe = util.PriorityQueue()
    visited = set()
    fringe.push(current, current[COST])
    while not fringe.isEmpty():
        current = fringe.pop()
        if problem.is_goal_state(current[STATE]):
            return current[PATH]
        elif current[STATE] not in visited:
            neighbors = problem.get_successors(current[STATE])
            for triplet in neighbors:
                path_to = current[PATH]
                path_to.append(triplet[ACTION])
                neighbor = (triplet[STATE], path_to, triplet[COST] + heuristic(triplet[STATE], problem))
                fringe.push(neighbor, neighbor[COST])
            visited.add(current[STATE])

    util.raiseNotDefined()



# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search
