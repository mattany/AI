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
    a = Board()
    empty = Node(str(a))
    for i in range(3):
        for j in range(3):
            a.insert(i, j, "x")
            b = Node(str(a), parent=empty)
            for k in range(3):
                for l in range(3):
                    if k != i or j != l:
                        a.insert(k, l, "o")
                        Node(str(a), parent=b)
                        a.insert(k, l, "none")
            a.insert(i, j, "none")
    RenderTreeGraph(empty).to_picture("tree.png")
    # for pre, fill, node in RenderTree(empty):
    #     print("%s%s" % (pre, node.name))
    #
