import numpy as np

class random_agent:
    def __init__(self, name = "Random Agent"):
        self.name = name
        self.move = []
    
    def choose_pos(self, isvalid):
        ii = np.where(isvalid == 1)
        l = len(ii[0])
        x, y = np.random.randint(0,l), np.random.randint(0,l)
        self.move = [ii[0][x],ii[1][y]]

    
    def ret_move(self, isvalid, bag, measured):
        i = 0
        p = np.random.randint(1,100)
        self.choose_pos(isvalid)
        while(p > 80 or bag.count(0)==6):
            if(measured[self.move] == 1):
                self.choose_pos(isvalid)
                continue
            return self.move, 0
        qubit = 0
        while(i == 0):
            qubit = np.random.randint(1,7)
            if bag[qubit] == 0:
                continue
            i = 1
        return self.move,qubit