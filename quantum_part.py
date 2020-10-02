from qiskit import QuantumCircuit, execute, BasicAer
from qiskit.quantum_info import Statevector

import numpy as np

# from qiskit.visualization import plot_histogram
# import matplotlib.pyplot as plt

class quantum_backend:
    # Constructor for class. We can probably pass the players names here
    def __init__(self, players = ["P1", "P2"]):
        N = 8
        self.player1 = players[0]
        self.player2 = players[1]

        # Two boards. One for the quantum states associated with the board
        # Other one to store the values after measurement
        self.quantum_board = [[None]*N for _ in range(N)]
        self.classical_board = np.zeros([N, N])

        # Store the positions of the gates
        self.h_squares = [[0,2],[0,5],[2,0],[5,0],[2,7],[5,7],[7,2],[7,5]]
        self.x_squares = [[2,2],[2,5],[5,2],[5,5]]
        self.cx_squares = [[1,1],[1,6],[6,1],[6,6]]
        self.en_squares = [[0,0],[0,7],[7,0],[7,7]]

        # States corresponding to what the player chooses
        q0 = Statevector([1,0])
        q1 = Statevector([0,1])
        qp = Statevector([1/np.sqrt(2), 1/np.sqrt(2)])
        qm = Statevector([1/np.sqrt(2), -1/np.sqrt(2)])
        q075 = Statevector([np.sqrt(3)/2, -1/2])
        q175 = Statevector([1/2, np.sqrt(3)/2])
        self.state_dict = {1:q0, 2:q1, 3:qp, 4:qm, 5:q075, 6:q175}
    
    # Function to return the state given the circuit. The circuit would have
    # already been initialised with the state played
    def _get_state(self, circuit):
        backend = BasicAer.get_backend("statevector_simulator")
        state = Statevector(execute(circuit, backend = backend).result().get_statevector())
        return state
    
    # If a move is played on one of the H squares
    def _h_move(self, state):
        qc = QuantumCircuit(1)
        qc.initialize(state.data, 0)
        qc.h(0)
        return self._get_state(qc)
    
    # If a move is played on one of the X squares
    def _x_move(self, state):
        qc = QuantumCircuit(1)
        qc.initialize(state.data, 0)
        qc.x(0)
        return self._get_state(qc)
    
    # If a move is played on one of the CX squares
    def _cx_move(self, state):
        qc = QuantumCircuit(2)
        qc.initialize(state.data, [0,1])
        qc.cx(0, 1)
        return self._get_state(qc)
    
    # If a move is played on one of the Swap squares
    def _en_move(self, state):
        qc = QuantumCircuit(2)
        qc.initialize(state.data, [0,1])
        qc.h(0)
        qc.cx(0,1)
        return self._get_state(qc)
    
    # When a player makes a measurement
    def _get_measurement(self, state):
        backend = BasicAer.get_backend("qasm_simulator")
        shots = 1
        # Get number of qubits
        n = int(np.log2(state.dim))
        qc = QuantumCircuit(n)
        qc.initialize(state.data, range(n))
        # Make measurement
        qc.measure_all()
        results = execute(qc, backend = backend, shots = shots).result().get_counts()
        # plot_histogram(results)
        # plt.show()

        # Find the measured state
        for key, _ in results.items():
            return key

    # Function to be called from outside when a move is played that is not a
    # measurement
    # Move is a list in the form [x,y] where x,y are the co-ordinates on the 
    # grid
    # State is the qubit played from the "bag". May be anything from 0-5. The
    # corresponding state is stored in a dictionary
    def move(self, move, state):
        x = move[0]
        y = move[1]

        # For one qubit gates just use the qubit selected
        if(move in self.h_squares):
            state = self.state_dict[state]
            self.quantum_board[x][y] = self._h_move(state)
        elif(move in self.x_squares):
            state = self.state_dict[state]
            self.quantum_board[x][y] = self._x_move(state)
        
        # For 2 qubit gates take tensor product of both the qubits
        elif(move in self.cx_squares):
            state = self.state_dict[state[0]].expand(self.state_dict[state[1]])
            self.quantum_board[x][y] = self._cx_move(state)
        elif(move in self.en_squares):
            state = self.state_dict[state[0]].expand(self.state_dict[state[1]])
            temp = self._en_move(state)
            self.quantum_board[x][y] = temp
            self.quantum_board[7-x][7-y] = temp
        else:
            self.quantum_board[x][y] = self.state_dict[state]
    
    # Function to be called from outside when a measurement is made
    # Move is a list in the form [x,y] where x,y are the co-ordinates on the 
    # grid
    def measurement_move(self, move):
        x = move[0]
        y = move[1]
        out_state = self._get_measurement(self.quantum_board[x][y])
        if move in self.en_squares:
            self.classical_board[x][y] = int(out_state[1])
            self.classical_board[7-x][7-y] = int(out_state[0])
        else:
            self.classical_board[x][y] = out_state.count("1")%2
