class Node:
    def __init__(self, position, parent, g, h):
        self.position = position
        self.parent = parent
        self.g = g
        self.h = h
        self.f = g + h
