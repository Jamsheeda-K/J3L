from src.a_star import find_path
import numpy as np

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


class A_star_supermarket:
    def __init__(self):
        contents = [list(row) for row in MARKET.split("\n")]
        nr = len(contents)
        nc = len(contents[0])
        self.grid = np.zeros((nr,nc),int)
        for i in range(nr):
            for j in range(nc):
                if(contents[i][j] not in ['G', '.']):
                    self.grid[i,j] = 1
        #print(self.grid)
        self.p_moves = [(0,1),(0,-1),(1,0),(-1,0)]
        #self.p_moves = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]


    def find_path(self, start, end):
        #print('find_path ',start,end)
        return find_path(self.grid, tuple(start), tuple(end), self.p_moves)

