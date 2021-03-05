"""
Adpapt Gesa's A star algorithm to the supermarkte simulation
"""
import numpy as np
from src.a_star import find_path

MARKET = """
##################
##..............##
##..##..##..##..##
##..##..##..##..##
##..##..##..##..##
##..##..##..##..##
##..##..##..##..##
##...............#
##..CD..CD..CD...#
##..##..##..##...#
##...............#
##############GG##
""".strip()


class AstarSupermarket:
    "Adaptor between superamarket and Astar"
    def __init__(self):
        contents = [list(row) for row in MARKET.split("\n")]
        n_r = len(contents)
        n_c = len(contents[0])
        self.grid = np.zeros((n_r, n_c),int)
        for i in range(n_r):
            for j in range(n_c):
                if(contents[i][j] not in ['G', '.']):
                    self.grid[i,j] = 1
        self.p_moves = [(0,1),(0,-1),(1,0),(-1,0)]
        #self.p_moves = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]


    def find_path(self, start, end):
        "finds a path from start to end (which are postions as pairs)"
        return find_path(self.grid, tuple(start), tuple(end), self.p_moves)
