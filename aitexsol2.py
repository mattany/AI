import random
# from anytree import Node, RenderTree
# from anytree.dotexport import RenderTreeGraph
#
# SPACE = 0
# X = 1
# O = -1
#
#
# class Board:
#
#     def __init__(self):
#         self.state = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
#
#     def insert(self, row, col, symbol):
#         assert (symbol == "x" or symbol == "o" or symbol == "none")
#
#         if symbol == "x":
#             self.state[row][col] = 1
#         elif symbol == "o":
#             self.state[row][col] = -1
#         elif symbol == "none":
#             self.state[row][col] = 0
#         else:
#             assert False
#
#     # def eval(self, board):
#
#     def __str__(self):
#         string = list()
#         for i in range(3):
#             for j in range(3):
#                 symbol = self.state[i][j]
#                 # if j == 0 and i != 0:
#                 #     string.append("    ")
#                 if symbol == SPACE:
#                     string.append("|  ")
#                 elif symbol == X:
#                     string.append("|x")
#                 elif symbol == O:
#                     string.append("|o")
#                 else:
#                     assert False
#                 if j == 2:
#                     string.append("|\n")
#         return ''.join(string)
#


def board():
    tuples = [[0,[]] for i in range(3)]
    for i, item in enumerate(tuples):
        teams = ['a', 'b', 'c', 'd']
        tuples[i][0] = random.randint(1,8)
        num_teams = len(teams)
        for j in range(num_teams):
            k = random.randint(0,len(teams) - 1)
            tuples[i][1].append(teams.pop(k))
    return tuples

def smith():
    tuples = board()

def success(winning_set, losing_set, tuples):
    return borda_winner(tuples) in losing_set

def black(tuples):
    condorcet = winner_exists(tuples)
    if condorcet[0]:
        return condorcet[1]
    return borda_winner(tuples)

def borda_winner(tuples):
    candidates = tuples[0][1]
    counts = dict()
    for candidate in candidates:
        score = 0
        for tuple in tuples:
            score += tuples[0] * tuple[1].index(candidate)
        counts[candidate] = score
    k = list(counts.keys())
    v = list(counts.values())
    return k[v.index(max(v))]


def winner_exists(tuples):
    candidates = tuples[0][1]
    for candidate in candidates:
        if condorcet_winner(candidate, tuples):
            return (True, candidate)
    return (False, False)

def smith_sets(a, tuples):

    candidates = tuples[0][1]
    candidates.pop(a)
    for candidate in candidates:
        score = 0
        for tuple in tuples:
            if tuple[1].index(a) > tuple[1].index(candidate):
                score += tuple[0]
            else:
                score -= tuple[0]
        if score <= 0:
            return False
    return True


def condorcet_winner(a, tuples):
    candidates = tuples[0][1]
    candidates.pop(a)
    for candidate in candidates:
        score = 0
        for tuple in tuples:
            if tuple[1].index(a) > tuple[1].index(candidate):
                score += tuple[0]
            else:
                score -= tuple[0]
        if score <= 0:
            return False
    return True


if __name__ == '__main__':
    print(board())
# board = Board()
# a = Node(str(board))
# board_list = [[0] for i in range(9)]
# for i in range(3):
#     for j in range(3):
#         board.insert(i, j, "x")
#         b = Node(str(board), parent=a)
#         board_list[3*i+j][0]=b
# print(board_list)
#         # added = list()
#         # for k in range(3):
#         #     for l in range(3):
#         #         if i != k or j != l:
#         #             for (m, n) in added:
#         #                 if i - m == k - i and j - n == j - l:
#         #                     board.insert(m, n, "o")
#         #                     Node(str(board), parent=b)
#         #                     board.insert(m, n, "none")
#         #                     break
#         #                 elif i - m == l - i and j - n == j - k:
#         #                     board.insert(m, n, "o")
#         #                     Node(str(board), parent=b)
#         #                     board.insert(m, n, "none")
#         #                     break
#         #                 elif i - m == l - j and i - n == j - k:
#         #                     board.insert(m, n, "o")
#         #                     Node(str(board), parent=b)
#         #                     board.insert(m, n, "none")
#         #                     break
#         #                 elif i - m == k - j and i - n == j - l:
#         #                     board.insert(m, n, "o")
#         #                     Node(str(board), parent=b)
#         #                     board.insert(m, n, "none")
#         #                     break
#         #             else:
#         #                 board.insert(k, l, "o")
#         #                 Node(str(board), parent=b)
#         #                 board.insert(k, l, "none")
#         #                 added.append((k, l))
#         #
#
#
#                     # if (k, l) in [(0, 0), (1, 1), (2, 2), (0, 2), (0, 1), (1, 2)] or (i == l and j == k):
#                     #     a.insert(k, l, "o")
#                     #     Node(str(a), parent=b)
#                     #     a.insert(k, l, "none")
#                     # else:
#                     #     a.insert(l, k, "o")
#                     #     Node(str(a), parent=b)
#                     #     a.insert(l, k, "none")
#
#         # board.insert(i, j, "none")
#
# # RenderTreeGraph(a).to_picture("ree.png")
# # for pre, fill, node in RenderTree(empty):
# #     print("%s%s" % (pre, node.name))
