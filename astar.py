#To run: python astar.py < board-x-x.txt
import heapq
class Heap: #We want a max-heap while heapq gives us a min-heap, so we invert all values
    def __init__(self):
        self.nodes = []

    def is_empty(self):
        return len(self.nodes) == 0

    def push(self, node):

        heapq.push

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

    open_set = [start_node]
    start_node.g = 0

def main():
    board = read_board()

    for line in board:
        print line

    print goal_node(board).position
    print walls(board)

#Board reading functions
def read_board():
    from sys import stdin

    board = []
    for x in stdin.readlines(): #les brettet fra stdin
        board.append(x.strip())
    return board

def get_board_nodes(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 'A':
                return Node((i, j))

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

def walls(board):
    list_of_walls = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == '#':
                wall_node = Node((i,j))
                wall_node.weight = 100 #Represent the node being a wall
                list_of_walls.append(wall_node)
    return list_of_walls

def is_wall(position_tuple, board):
    return board[position_tuple[0]][position_tuple[1]] == "#"


if __name__ == '__main__':
    main()
