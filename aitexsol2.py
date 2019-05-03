from anytree import Node, RenderTree
from anytree.dotexport import RenderTreeGraph

SPACE = 0
X = 1
O = -1


class Board:

    def __init__(self):
        self.state = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def insert(self, row, col, symbol):
        assert (symbol == "x" or symbol == "o" or symbol == "none")

        if symbol == "x":
            self.state[row][col] = 1
        elif symbol == "o":
            self.state[row][col] = -1
        elif symbol == "none":
            self.state[row][col] = 0
        else:
            assert False

    # def eval(self, board):

    def __str__(self):
        string = list()
        for i in range(3):
            for j in range(3):
                symbol = self.state[i][j]
                # if j == 0 and i != 0:
                #     string.append("    ")
                if symbol == SPACE:
                    string.append("|  ")
                elif symbol == X:
                    string.append("|x")
                elif symbol == O:
                    string.append("|o")
                else:
                    assert False
                if j == 2:
                    string.append("|\n")
        return ''.join(string)


if __name__ == '__main__':
    board = Board()
    a = Node(str(board))
    board_list = [[0] for i in range(9)]
    for i in range(3):
        for j in range(3):
            board.insert(i, j, "x")
            b = Node(str(board), parent=a)
            board_list[3*i+j][0]=b
    print(board_list)
            # added = list()
            # for k in range(3):
            #     for l in range(3):
            #         if i != k or j != l:
            #             for (m, n) in added:
            #                 if i - m == k - i and j - n == j - l:
            #                     board.insert(m, n, "o")
            #                     Node(str(board), parent=b)
            #                     board.insert(m, n, "none")
            #                     break
            #                 elif i - m == l - i and j - n == j - k:
            #                     board.insert(m, n, "o")
            #                     Node(str(board), parent=b)
            #                     board.insert(m, n, "none")
            #                     break
            #                 elif i - m == l - j and i - n == j - k:
            #                     board.insert(m, n, "o")
            #                     Node(str(board), parent=b)
            #                     board.insert(m, n, "none")
            #                     break
            #                 elif i - m == k - j and i - n == j - l:
            #                     board.insert(m, n, "o")
            #                     Node(str(board), parent=b)
            #                     board.insert(m, n, "none")
            #                     break
            #             else:
            #                 board.insert(k, l, "o")
            #                 Node(str(board), parent=b)
            #                 board.insert(k, l, "none")
            #                 added.append((k, l))
            #


                        # if (k, l) in [(0, 0), (1, 1), (2, 2), (0, 2), (0, 1), (1, 2)] or (i == l and j == k):
                        #     a.insert(k, l, "o")
                        #     Node(str(a), parent=b)
                        #     a.insert(k, l, "none")
                        # else:
                        #     a.insert(l, k, "o")
                        #     Node(str(a), parent=b)
                        #     a.insert(l, k, "none")

            # board.insert(i, j, "none")

    # RenderTreeGraph(a).to_picture("tree.png")
    # for pre, fill, node in RenderTree(empty):
    #     print("%s%s" % (pre, node.name))