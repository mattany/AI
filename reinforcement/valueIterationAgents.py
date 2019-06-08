# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html
import mdp, util, numpy as np

from learningAgents import ValueEstimationAgent

QVALUE = 0

ACTION = 1

UTILITY = 0

PROB = 1
STATE = 0

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """

    def q_value(self, state, action):
        return sum(tup[PROB] * self.values[tup[STATE]] for tup in self.mdp.getTransitionStatesAndProbs(state, action))

    def reward(self, state, action):
        # return sum(tup[PROB] * (self.mdp.getReward(state, action, tup[STATE]) + (vals[tup[STATE]]*self.discount))
        #            for tup in self.mdp.getTransitionStatesAndProbs(state, action))
        return sum(tup[PROB] * self.mdp.getReward(state, action, tup[STATE]) for tup in self.mdp.getTransitionStatesAndProbs(state, action))

    def utility(self, state, action):
        return sum(tup[PROB] * (self.mdp.getReward(state, action, tup[STATE]) + (self.values[tup[STATE]]*self.discount))
                   for tup in self.mdp.getTransitionStatesAndProbs(state, action))

    def set_policies(self):
        for state in self.mdp.getStates():
            if not self.mdp.isTerminal(state):
                self.policies[state] = max([(self.q_value(state, action), action)
                                            for action in
                                            self.mdp.getPossibleActions(state)], key=lambda x: x[QVALUE])[ACTION]
                continue
            self.policies[state] = None

    def set_q_values(self):
        for state in self.mdp.getStates():
            if not self.mdp.isTerminal(state):
                for action in self.mdp.getPossibleActions(state):
                    self.q_values[(state, action)] = self.q_value(state, action)

    def __init__(self, mdp, discount=0.9, iterations=100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter()  # A Counter is a dict with default
        self.policies = util.Counter()
        self.q_values = util.Counter()

        for i in range(iterations):
            temp = self.values.copy()
            for state in mdp.getStates():
                if not mdp.isTerminal(state):
                    temp[state] = max(self.utility(state, action) for action in mdp.getPossibleActions(state))
            self.values = temp

        self.set_q_values()
        self.set_policies()



    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def getQValue(self, state, action):
        """
          The q-value of the state action pair
          (after the indicated number of value iteration
          passes).  Note that value iteration does not
          necessarily create this quantity and you may have
          to derive it on the fly.
        """
        return self.q_values[(state, action)]
        # return self.q_value(state, action, self.values)

    def getPolicy(self, state):
        """
          The policy is the best action in the given state
          according to the values computed by value iteration.
          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        policy = None
        # max_value = -np.inf
        # for action in self.mdp.getPossibleActions(state):
        #     for (prob, next_state) in self.mdp.getTransitionStatesAndProbs(state, action):
        #         if self.values[next_state] > max_value:
        #             max_value = self.values[next_state]
        #             policy = action
        # return policy

        return self.policies[state]
        # if not self.mdp.isTerminal(state):
        #     policy = max([(self.q_value(state, action, self.values), action) for action in self.mdp.getPossibleActions(state)],
        #                  key=lambda x: x[QVALUE])[ACTION]
        # return policy

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.getPolicy(state)
