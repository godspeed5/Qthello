import numpy as np

class random_agent:
    def __init__(self, name = "Random Agent"):
        self.name = name
    
    def ret_move(self, isvalid, bag):
        i = 0
        qubit = 0
        while(i == 0):
            qubit = np.random.randint(1,7)
            if bag[qubit] == 0:
                continue
            i = 1
        ii = np.where(isvalid == 1)
        l = len(ii[0])
        x, y = np.random.randint(0,l), np.random.randint(0,l)
        move = [ii[0][x],ii[1][y]]
        return move,qubit