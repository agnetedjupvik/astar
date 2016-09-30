#To run: python weighted-astar.py < board-2-x.txt

'''
NODE REPRESENTATIONS
. not visited, walkable
# wall
A starting node
B goal node
o in the open set
c in the closed set
'''

'''
GRASS REPRESENTATIONS
m mountains, cost 50
f forests, cost 10
w water, cost 100
g grass, cost 5
r roads, cost 1
'''

class PriorityQueue: #store in a min-heap
    def __init__(self):
        self.nodes = []

    def __cmp__(self, other):
        return cmp(self.f, other.f) #order heap by f(n) value

    def contains(self, other):
        for node in self.nodes:
            if node.position == other.position:
                return True
        return False

    def is_empty(self):
        return len(self.nodes) == 0

    def push(self, node):
        self.nodes.append(node)
        self.nodes.sort(key=lambda x: x.f, reverse = True)

    def pop(self):
        self.nodes.sort(key=lambda x: x.f, reverse = True)
        node = self.nodes.pop()
        return node


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
    start_node.h = manhattan_distance(start_node, goal_node, board)
    start_node.f = manhattan_distance(start_node, goal_node, board) #f for initial node is completely heuristic
    open_set.push(start_node)
    print "We start out at", start_node.position

    while not open_set.is_empty():
        current = open_set.pop()

        if current.position == goal_node.position:
            print "Yay, we found the goal!"
            return path(current, board)

        closed_set.append(current) #could have had this as a PriorityQueue, but didn't really see the point
        current.representation = 'c'
        for node in getNeighbours(current, board):
            if node in closed_set:
                continue

            neighbor_g = get_total_cost(current) + node.g

            if not open_set.contains(node): #discover new node, visit at some later point
                open_set.push(node)
                node.representation = 'o'
            elif neighbor_g >= node.g: #this path is not an augmenting one
                continue

            #Record our amazing progress on finding a good node which is possibly in the path
            node.parent = current

            node.h = manhattan_distance(node, goal_node, board)
            node.f = neighbor_g + manhattan_distance(node, goal_node, board)
            print_board(board)

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

def get_total_cost(node):
    cost = node.g
    while node.parent != None:
        cost += node.parent.g
        node = node.parent
    return cost

#Calculate heuristic
def manhattan_distance(node, goal_node, board):
    node_x = node.position[0]
    node_y = node.position[1]

    goal_node_x = goal_node.position[0]
    goal_node_y = goal_node.position[1]

    return abs(node_x - goal_node_x) + abs(node_y - goal_node_y)

#Get path back to start_node
def path(node, board):
    path = [node.position] #Can alter this to return the entire objects, not just their positions
    while node.parent != None:
        path.append(node.parent.position)
        node = node.parent

    board = print_board(board)
    for item in path:
        board[item[0]][item[1]] = '-'

    for line in board:
        print ''.join(line).strip()
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
            if new_node.representation == 'w': #this could probably have been done in a more optimal way
                new_node.g = 100
            elif new_node.representation == "m":
                new_node.g = 50
            elif new_node.representation == 'f':
                new_node.g = 10
            elif new_node.representation == 'g':
                new_node.g = 5
            elif new_node.representation == 'r':
                new_node.g = 1
            else:
                new_node.g = 1
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

    return board_representation


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
