#To run: python astar.py < board-x-x.txt
class PriorityQueue:
    def __init__(self):
        self.nodes = []

    def is_empty(self):
        return len(self.nodes) == 0

    def push(self, node):
        self.nodes.append(node)
        self.nodes.sort(key = lambda x: x.f) #sort by f

    def pop(self):
        return self.nodes.pop()

class Node:
    def __init__(self, position):
        self.position = position
        self.parent = None
        self.g = None
        self.h = None
        self.f = None
        self.weight = None

def a_star(board, start_node, goal_node):
    closed_set = []

    open_set = PriorityQueue()
    start_node.f = 0
    open_set.push(start_node)

    while not open_set.is_empty():
        print open_set.pop().position

def main():
    board = read_board()

    for line in board:
        print line

    a_star(board, start_node(board), goal_node(board))

#Board reading functions
def read_board():
    from sys import stdin

    board = []
    for x in stdin.readlines(): #read board from stdin
        board.append(x.strip())
    return board


def start_node(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 'A':
                return Node((i, j))

def goal_node(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 'B':
                return Node((i, j))

def is_goal_node(position_tuple, board):
    return board[position_tuple[0]][position_tuple[1]] == "B"

def is_wall(position_tuple, board):
    return board[position_tuple[0]][position_tuple[1]] == "#"


if __name__ == '__main__':
    main()
