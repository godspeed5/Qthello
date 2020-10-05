# Qthello

Quantum Othello:
The aim of the game is to have more of your colour on the board than your opponent. Classical Othello rules of flipping flanked discs apply here as well, but these rules kick in only after measurement. The twist is in Qthello you are likely to play against yourself, so be careful!

Connectedness: You must play qubits such that one of the nearest neighbours has been played on already (not necessarily measured). This includes diagonals. This condition, however, is relaxed for measurement moves

Gates on board:
X: NOT 

CX: Controlled NOT

H: Hadamard

S: Swap (diagonals are connected)


You can play a qubit or measure (the red m square) each turn.
Qubits that you can play:

|0>

|1>

|+>: (|0>+|1>)/sqrt(2)

|->: (|0>-|1>)/sqrt(2)

75|0>: (sqrt(3)*|0>-|1>)/2

75|1>: (sqrt(3)*|1>+|0>)/2
