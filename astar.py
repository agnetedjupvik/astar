#To run: python astar.py < board-x-x.txt
import heapq
class PriorityQueue: #store in a min-heap
    def __init__(self):
        self.nodes = []

    def __cmp__(self, other):
        return cmp(self.f, other.f) #order heap by f(n) value

    def is_empty(self):
        return len(self.nodes) == 0

    def push(self, node):
        heapq.heappush(self.nodes, node)

    def pop(self):
        return heapq.heappop(self.nodes)

class Node:
    def __init__(self, position):
        self.position = position
        self.parent = None
        self.g = float("Inf") #Infinity values for g and h so that we can improve them later
        self.h = float("Inf")
        self.f = self.g + self.h
        self.weight = None
        self.representation = '.' #Used for printing the board to console

    def __str__(self):
        return self.representation

def a_star(board, start_node, goal_node):
    closed_set = []

    open_set = PriorityQueue()
    start_node.g = 0
    start_node.h = manhattan_distance(start_node, goal_node)
    start_node.f = manhattan_distance(start_node, goal_node) #f for initial node is completely heuristic
    open_set.push(start_node)

    while not open_set.is_empty():
        current = open_set.pop()

        if current == goal_node:
            return path(current)

        closed_set.append(current) #could have had this as a PriorityQueue, but didn't really see the point
        for node in getNeighbours(current, board):
            if node in closed_set:
                continue

            neighbor_g = current.g + manhattan_distance(current, node) #use manhattan_distance? else: TODO

            if node not in open_set: #discover new node, visit sometime
                open_set.push(node)
            elif neighbor_g >= node.g: #this path is not an augmenting one
                continue

            #Record our amazing progress on finding a good node which is possibly in the path
            node.parent = current
            node.g = parent.g
            node.h = manhattan_distance(node, goal_node)
            node.f = parent.g + manhattan_distance(node, goal_node)

    return 0



def main():
    board = read_board()

    print_board(board)

    a_star(board, start_node(board), goal_node(board))

#Get walkable neighbours for a node
def getNeighbours(node, board):
    neighbours = []
    current_x = node.position[0]
    current_y = node.position[1]
    possible_positions = [(current_x, current_y+1), (current_x, current_y-1), (current_x+1, current_y), (current_x-1, current_y)]
    for position in possible_positions:
        if (not position[0] == -1) and (not position[1] == -1): #avoid exiting through the beginning of the board
            for line in board: #not optimal.. should be refactored sometime
                for node in line:
                    if node.position == position:
                        if not is_wall(node.position, board):
                            neighbours.append(node)
    return neighbours

#Calculate heuristic
def manhattan_distance(node, goal_node):
    node_x = node.position[0]
    node_y = node.position[1]

    goal_node_x = goal_node.position[0]
    goal_node_y = goal_node.position[1]

    return abs(node_x - goal_node_x) + abs(node_y - goal_node_y)

#Get path back to start_node
def path(node):
    path = [node.position] #Can alter this to return the entire objects, not just their positions
    while node.parent != None:
        path.append(node.parent.position)
        node = node.parent
    return path

#Board reading functions
def read_board():
    from sys import stdin

    board = []
    i = 0
    for line in stdin.readlines(): #read board from stdin
        board_line = []
        for j in range(len(line)):
            new_node = Node((i, j))
            new_node.representation = line[j]
            board_line.append(new_node) #create node representation of board
        board.append(board_line)
        i += 1

    return board

def print_board(board):
    board_representation = []
    for line in board:
        line_array = []
        for node in line:
            line_array.append(str(node)) #same as node.representation
        board_representation.append(line_array)

    for line in board_representation:
        print ''.join(line)


def start_node(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if str(board[i][j]) == 'A':
                return Node((i, j))

def goal_node(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if str(board[i][j]) == 'B':
                return Node((i, j))

def is_goal_node(position_tuple, board):
    return str(board[position_tuple[0]][position_tuple[1]]) == "B"

def is_wall(position_tuple, board):
    return str(board[position_tuple[0]][position_tuple[1]]) == "#"


if __name__ == '__main__':
    main()
