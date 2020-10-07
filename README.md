# # Qthello

# Quantum Othello:
The aim of the game is to have more of your colour on the board than your opponent. [Classical Othello](https://www.mastersofgames.com/rules/reversi-othello-rules.htm#:~:text=Basic%20Play,pieces%20are%20captured%20or%20reversed) rules of flipping flanked discs apply here as well, but these rules kick in only after measurement. The twist is in Qthello you are likely to play against yourself, so be careful!

Note: You must have qiskit and pygame installed to run the program. If you do not, just run:

pip install qiskit

pip install pygame

After this you can just run python game.py to play the game. Choose whether you want to play single or 2 players at the input prompt on terminal.

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

# How to play:
Click on the qubit you want to play from the second last row of the screen. The last row shows the number of qubits of a particular state left. After choosing the qubit, click on the tile you want to place it on. If you want to measure, click on the "m" button, and then the place you want to measure.
A turn change is indicated by the color of the number of qubits in the last row. You can measure only after a tile has been filled with a qubit, and in the case of 2 qubit gates, 2 qubits must have been played on the tile.
