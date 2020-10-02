from qiskit import QuantumCircuit, execute, BasicAer
from qiskit.quantum_info import Statevector

import numpy as np

class quantum_backend:
    # Constructor for class. We can probably pass the players names here
    def __init__(self, players, N = 8):
        self.N = N
        self.player1 = players[0]
        self.player2 = players[1]

        # Two boards. One for the quantum states associated with the board
        # Other one to store the values after measurement
        self.quantum_board = np.zeros([N, N])
        self.classical_board = np.zeros([N, N])

        # Store the positions of the gates
        self.h_squares = [[0,2],[0,5],[2,0],[5,0],[2,7],[5,7],[7,2],[7,5]]
        self.x_squares = [[2,2],[2,5],[5,2],[5,5]]
        self.cx_squares = [[1,1],[1,6],[6,1],[6,6]]
        self.s_squares = [[0,0],[0,7],[7,0],[7,7]]

        # States corresponding to what the player chooses
        q0 = Statevector([1,0])
        q1 = Statevector([0,1])
        qp = Statevector([1/np.sqrt(2), 1/np.sqrt(2)])
        qm = Statevector([1/np.sqrt(2), -1/np.sqrt(2)])
        q075 = Statevector([np.sqrt(3)/2, -1/2])
        q175 = Statevector([1/2, np.sqrt(3)/2])
        self.state_dict = {0:q0, 1:q1, 2:qp, 3:qm, 4:q075, 5:q175}
    
    # Function to return the state given the circuit. The circuit would have
    # already been initialised with the state played
    def _get_state(self, circuit):
        backend = BasicAer.get_backend("statevector_simulator")
        state = execute(circuit, backend = backend).result().get_statevector()
        return state
    
    # If a move is played on one of the H squares
    def _h_move(self, state):
        qc = QuantumCircuit(1)
        qc.initialize(state, 0)
        qc.h(0)
        return self._get_state(qc)
    
    # If a move is played on one of the X squares
    def _x_move(self, state):
        qc = QuantumCircuit(1)
        qc.initialize(state, 0)
        qc.x(0)
        return self._get_state(qc)
    
    # If a move is played on one of the CX squares
    def _cx_move(self, state):
        qc = QuantumCircuit(2)
        qc.initialize(state, [0,1])
        qc.cx(0, 1)
        return self._get_state(qc)
    
    # If a move is played on one of the Swap squares
    def _en_move(self, state):
        qc = QuantumCircuit(2)
        qc.initialize(state, [0,1])
        qc.swap(0, 1)
        return self._get_state(qc)
    
    # When a player makes a measurement
    def _get_measurement(self, state):
        backend = BasicAer.get_backend("qasm_simulator")
        shots = 1
        # Get number of qubits
        n = np.sqrt(len(state)) # Maybe change this to log_2 later instead
        qc = QuantumCircuit(n)
        qc.initialize(state, range(n))
        # Make measurement
        qc.measure_all()
        results = execute(qc, backend = backend, shots = shots).result().get_counts()
        disc = None
        # Find the corresponding "disc"
        for key, _ in results.items():
            disc = key.count("1")%2
        return disc

    # Function to be called from outside when a move is played that is not a
    # measurement
    def move(self, move, state):
        x = move[0]
        y = move[1]
        if(move in self.h_squares):
            state = self.state_dict[state]
            self.quantum_board[x][y] = self._h_move(state)
        elif(move in self.x_squares):
            state = self.state_dict[state]
            self.quantum_board[x][y] = self._x_move(state)
        elif(move in self.cx_squares):
            state = self.state_dict[state[0]].expand(self.state_dict[state[1]])
            self.quantum_board[x][y] = self._cx_move(state)
        elif(move in self.s_squares):
            self.state_dict[state[0]].expand(self.state_dict[state[1]])
            self.quantum_board[x][y] = self._en_move(state)
    
    # Function to be called from outside when a measurement is made
    def measurement_move(self, move):
        x = move[0]
        y = move[1]
        self.classical_board[x][y] = self._get_measurement( \
                                    self.quantum_board[x][y])

