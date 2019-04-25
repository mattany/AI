import time
import multi_agents
import math
import numpy as np
import matplotlib.pyplot as plt
VERBOSE = True

REMARKS = ""



class SummaryDisplay(object):
    def __init__(self):
        super(SummaryDisplay, self).__init__()
        self.scores = []
        self.highest_tile = []
        self.game_durations = []
        self.game_start_time = None

    def initialize(self, initial_state):
        self.game_start_time = time.time()

    def update_state(self, new_state, action, opponent_action):
        if new_state.done:
            game_end_time = time.time()
            game_duration = game_end_time - self.game_start_time
            if VERBOSE:
                print("score: %s\nhighest tile: %s\ngame_duration: %s" % (new_state.score, new_state.board.max(),
                                                                      game_duration))
            self.scores.append(new_state.score)
            self.highest_tile.append(new_state.board.max())
            self.game_durations.append(game_duration)

    def mainloop_iteration(self):
        pass

    def tile_rate(self, tile):
        return self.highest_tile.count(tile)/len(self.highest_tile)

    def population_mean(self, list):
        return sum(list) / len(list)

    def population_variance(self, list):
        mean = self.population_mean(list)
        return sum([math.sqrt(pow((x - mean), 2)) for x in list]) / len(list)

    def print_stats(self):
        win_rate = len(list(filter(lambda x: x >= 2048, self.highest_tile))) / len(self.highest_tile)
        threshold_rate = len(list(filter(lambda  x: x >= 7000, self.scores))) / len(self.scores)
        games = len(self.scores)
        print("="*30)
        print("scores: %s" % self.scores)
        print("highest tile: %s" % self.highest_tile)
        print("Heuristics: smooth: %s steep %s" % (multi_agents.SMOOTH, multi_agents.STEEP))
        print("number of games played: %s" % games)
        print("win rate: %s" % win_rate)
        print("average score: %s" % self.population_mean(self.scores))
        print("variance: %s" % self.population_variance(self.scores))
        print("7000+ proportion: %s" % threshold_rate)
        print("less than 1024 rate: %s" % (1 - sum(self.tile_rate(x) for x in [2 ** y for y in range(10, 15, 1)])))
        # print("1024 rate: %s" % self.tile_rate(2 ** 10))
        # print("2048 rate: %s" % self.tile_rate(2 ** 11))
        # print("4096 rate: %s" % self.tile_rate(2 ** 12))
        print("average time: %s" % (sum(self.game_durations)/len(self.game_durations)))
        print("average high tile: %s" % (sum(self.highest_tile)/len(self.highest_tile)))
        print("max score: %s min score: %s" % (max(self.scores), min(self.scores)))
        # plt.hist(self.scores, bins=100)
        # plt.ylabel('Probability')
        # plt.xlabel('scores Smooth:%s Steep:%s' % (multi_agents.SMOOTH, multi_agents.STEEP))
        # plt.show()
        # plt.hist(self.highest_tile, bins=6)
        # plt.ylabel('Probability')
        # plt.xlabel('power of 2 Smooth:%s Steep:%s' % (multi_agents.SMOOTH, multi_agents.STEEP))
        # plt.show()








#_________________________________________________OFFICIAL_FILE____________________________________________________#

# import time
#
#
# class SummaryDisplay(object):
#     def __init__(self):
#         super(SummaryDisplay, self).__init__()
#         self.scores = []
#         self.highest_tile = []
#         self.game_durations = []
#         self.game_start_time = None
#
#     def initialize(self, initial_state):
#         self.game_start_time = time.time()
#
#     def update_state(self, new_state, action, opponent_action):
#         if new_state.done:
#             game_end_time = time.time()
#             game_duration = game_end_time - self.game_start_time
#             print("score: %s\nhighest tile: %s\ngame_duration: %s" % (new_state.score, new_state.board.max(),
#                                                                       game_duration))
#             self.scores.append(new_state.score)
#             self.highest_tile.append(new_state.board.max())
#             self.game_durations.append(game_duration)
#
#     def mainloop_iteration(self):
#         pass
#
#     def print_stats(self):
#         win_rate = len(list(filter(lambda x: x >= 2048, self.highest_tile))) / len(self.highest_tile)
#         print("="*30)
#         print("scores: %s" % self.scores)
#         print("highest tile: %s" % self.highest_tile)
#         print("game_durations: %s" % self.game_durations)
#         print("win rate: %s" % win_rate)