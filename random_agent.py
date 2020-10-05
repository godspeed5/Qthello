import numpy as np
from itertools import product

class random_agent:
    def __init__(self, name = "Random Agent", p_number = 1):
        self.p_number = p_number
        self.name = name
        self.pos = []
        self.all_pos = []
        for i in product(range(0,8,1),repeat = 2):
            self.all_pos += [i]
        for i in [(3,3),(3,4),(4,3),(4,4)]:
            self.all_pos.remove(i)
        # print(len(self.all_pos))
    
    def choose_pos(self, isvalid, qplayed):
        x, y = self.all_pos[np.random.randint(0, len(self.all_pos))]
        while(isvalid(qplayed, x, y)!=1):
            x, y = self.all_pos[np.random.randint(0, len(self.all_pos))]
            # print(self.pos)
        # print(len(self.all_pos))
        self.pos = [x,y]
    
    def ret_move(self, isvalid, bag, measured, qplayed):
        # print(bag)
        i = 0
        p = np.random.randint(0,10)
        self.choose_pos(isvalid, qplayed)
        while(p >= 5 or np.count_nonzero(bag[self.p_number] == 0)==6):
            if(measured[self.pos[0], self.pos[1]] == 1):
                self.choose_pos(isvalid, qplayed)
                continue
            return 0
        qubit = 0
        while(i == 0):
            qubit = np.random.randint(1,7)
            if bag[self.p_number][qubit-1] == 0:
                continue
            i = 1
        return qubit