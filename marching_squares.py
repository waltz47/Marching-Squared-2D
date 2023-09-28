import numpy as np
import time
from perlin_noise import PerlinNoise

class SquareMarch:
    pe = []
    grid = []
    iso = 0.5
    def __init__(self, ROWS, COLS, CELL_WIDTH, CELL_HEIGHT):
        self.ROWS = ROWS
        self.COLS = COLS
        self.CELL_WIDTH = CELL_WIDTH
        self.CELL_HEIGHT = CELL_HEIGHT
        # print(self.ROWS, self.COLS, self.CELL_WIDTH, self.CELL_HEIGHT)
        self.reseed()
        self.build_grid()

    def reseed(self):
        rng = np.random.default_rng(int(time.time_ns()))
        # self.pe = rng.random((self.ROWS,self.COLS))
        noise = PerlinNoise(octaves = 25,seed=int(time.time_ns()))
        self.pe = [[noise([i/self.ROWS, j/self.COLS]) for j in range(self.ROWS)] for i in range(self.COLS)]
        self.pe = (self.pe-np.min(self.pe))/(np.max(self.pe)-np.min(self.pe))
        # print(self.pe)

    def build_grid(self):
        #  self.reseed()
        self.grid = []
        for x in range(self.ROWS):
            k = []
            for y in range(self.COLS):
                if self.pe[x][y] >= self.iso:
                    k.append(1)
                else:
                    k.append(0)
            self.grid.append(k)
        
        # print(self.grid)

        
    def lerp(self,f1, f2):
        # print(f1,f2)
        v2 = max(f1,f2)
        v1 = min(f1,f2)
        if v1 == v2:
            return 0.5
        return (self.iso - v1) / (v2 - v1)

    def mid(self,A,B):
        t = self.lerp(self.pe[A[0]][A[1]], self.pe[B[0]][B[1]])

        x = (1-t) * A[0] * self.CELL_HEIGHT + t * B[0] * self.CELL_HEIGHT
        y = (1-t) * A[1] * self.CELL_WIDTH + t * B[1] * self.CELL_WIDTH
        
        # print("x and y: {} {}".format(x,y))
        return (int(x),int(y))
    
    def get_polygons(self):
        lines = []

        for i in range(self.ROWS-1):
            for j in range(self.COLS-1):
                tr = [i+1,j]
                tl = [i,j]
                bl = [i,j+1]
                br = [i+1,j+1]

                # print(tl, tr, bl, br)

                #going CW from left 
                a = self.mid(tl.copy(), bl.copy())
                b = self.mid(tl.copy(), tr.copy())
                c = self.mid(tr.copy(), br.copy())
                d = self.mid(bl.copy(), br.copy())
                
                tl[0] *= self.CELL_WIDTH
                tl[1] *= self.CELL_HEIGHT
                            
                tr[0] *= self.CELL_WIDTH
                tr[1] *= self.CELL_HEIGHT
                
                bl[0] *= self.CELL_WIDTH
                bl[1] *= self.CELL_HEIGHT

                br[0] *= self.CELL_WIDTH
                br[1] *= self.CELL_HEIGHT
                
                assert(i+1 < len(self.grid) and j+1 < len(self.grid[0]))
                lookup = (self.grid[i][j]*8) | (self.grid[i+1][j] * 4) | (self.grid[i+1][j+1] * 2) | (self.grid[i][j+1] * 1)
                if lookup == 0:
                    pass
                elif lookup == 1:
                    lines.append((a,d,bl))
                elif lookup == 2:
                    lines.append((c,br,d))
                elif lookup == 3:
                    lines.append((a,c,br,bl))
                elif lookup == 4:
                    lines.append((b,tr,c))
                elif lookup == 5:
                    lines.append((b,tr,c))
                    lines.append((a,d,bl))
                elif lookup == 6:
                    lines.append((b,tr,br,d))
                elif lookup == 7:
                    lines.append((a,b,tr,br,bl))
                elif lookup == 8:
                    lines.append((a,tl,b))
                elif lookup == 9:
                    lines.append((b,d,bl,tl))
                elif lookup == 10:
                    lines.append((a,tl,b))
                    lines.append((c,br,d))
                elif lookup == 11:
                    lines.append((b,c,br,bl,tl))
                elif lookup == 12:
                    lines.append((a,tl,tr,c))
                elif lookup == 13:
                    lines.append((c,d,bl,tl,tr))
                elif lookup == 14:
                    lines.append((d,a,tl,tr,br))
                elif lookup == 15:
                    lines.append((tl,tr,br,bl))
            
        return lines