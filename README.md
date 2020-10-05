# # Qthello

# Quantum Othello:
The aim of the game is to have more of your colour on the board than your opponent. Classical Othello rules of flipping flanked discs apply here as well, but these rules kick in only after measurement. The twist is in Qthello you are likely to play against yourself, so be careful!

Note: You must have qiskit and pygame installed to run the program. If you do not, just run:

pip install qiskit

pip install pygame

After this you can just run python game.py to play the game.

# Rules:

Connectedness: You must play qubits such that one of the nearest neighbours has been played on already (not necessarily measured). This includes diagonals. This condition, however, is relaxed for measurement moves.

If you do not have any valid moves left, the move passes to the other player.

For 2 qubit gates, the first qubit played is control, while the second is target.
For the CX gates, the two qubit output is mapped to a single output: "00","11" to 0(green), "01","10" to 1(black).
The EN gates are special, in the sense that the move is played on both ends of the the board. The measurement collapses in the same order as played.

Gates on board:

X: NOT 

CX: Controlled NOT

H: Hadamard

EN: The simple Bell circuit with H followed by CNOT; Diagonals are connected.


You can play a qubit or measure (the red m square) each turn.
Qubits that you can play:

|0>

|1>

|+>: (|0>+|1>)/sqrt(2)

|->: (|0>-|1>)/sqrt(2)

75|0>: (sqrt(3)*|0>-|1>)/2

75|1>: (sqrt(3)*|1>+|0>)/2
