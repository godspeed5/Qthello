import pygame
from pygame.locals import *
import numpy as np
from quantum_part import *
"""
 Example program to show using an array to back a grid on-screen.
 
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
 Explanation video: http://youtu.be/mdTeqiWyFnc
"""

qb = quantum_backend()

def countDigit(n): 
    count = 0
    while n != 0: 
        n //= 10
        count+= 1
    return count 
def isvalid(matrix, row, column):
       adjlist=[]
       for i in range(row-1, row+2):
               for j in range(column-1, column+2):
                       if (i in range(8)) and (j in range(8)):
                               adjlist.append(matrix[i][j])
       return np.any([i>0 for i in adjlist])

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (144,0,144)
PINK = (188,0,100)
LG = (144,238,144)
GRAY = (200,200,200)
 
# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 50
HEIGHT = 50
 
# This sets the margin between each cell
MARGIN = 3
 
# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = []
for row in range(10):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(10):
        grid[row].append(0)  # Append a cell
 
# Set row 1, cell 5 to one. (Remember rows and
# column numbers start at zero.)
playable = np.ones((8,8))
grid[4][3] = 1
grid[3][4] = 1
grid[4][4] = 2
grid[3][3] = 2
grid[8][0] = 1
grid[8][1] = 2

# Initialize pygame
pygame.init()
 
# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [WIDTH*8+MARGIN*7, HEIGHT*10+MARGIN*9]
screen = pygame.display.set_mode(WINDOW_SIZE)
 
# Set title of screen
pygame.display.set_caption("Qthello")
 
# Loop until the user clicks the close button.
done = False

#initialize game-tracking variables
movenumber=0
measured = np.zeros((8,8))
for i in range(3,5):
    for j in range(3,5):
        measured[i][j] = 1
ismeasure = 0
qplayed = np.zeros((8,8))
for i in range(3,5):
    for j in range(3,5):
       if i==j:
               qplayed[i][j] = 2
       else:
               qplayed[i][j] = 1
qmax = np.ones((8,8))
for i in [1,6]:
    for j in [1,6]:
        qmax[i][j] = 2
for i in range(3,5):
    for j in range(3,5):
        qmax[i][j] = 0
qselected = None
centerlist=[]
for row in range(10):
    alist=[]
    for column in range(8):
        alist.append(((MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN))
    centerlist.append(alist)

bag_rects = [centerlist[9][i] for i in range(6)]
bag_counts = np.ones((2,6))*6

# Set the font
font=pygame.font.SysFont('arial', 40)
font2=pygame.font.SysFont('arial', 20)

# Renders for all the gates on the board
en_text1=font.render('EN', True, PURPLE)
en_text2=font.render('EN', True, PURPLE)
en_rects=[centerlist[0][0],centerlist[0][7],centerlist[7][0],centerlist[7][7]]

cx_text=font.render('CX', True, BLUE)
cx_rects=[centerlist[1][1],centerlist[1][6],centerlist[6][1],centerlist[6][6]]

h_text=font.render('H', True, BLUE)
h_rects=[centerlist[0][2],centerlist[2][0],centerlist[0][5],centerlist[5][0],centerlist[7][5],centerlist[7][2],centerlist[5][7],centerlist[2][7]]

x_text=font.render('X', True, BLUE)
x_rects=[centerlist[2][2],centerlist[2][5],centerlist[5][2],centerlist[5][5]]

# Renders for our "bag" of discs
m_text=font.render('m', True, BLUE)
m_rect=centerlist[8][7]
q0_text=font2.render('|0>', True, BLUE)
q1_text=font2.render('|1>', True, WHITE)
qplus_text=font2.render('|+>', True, BLUE)
qminus_text=font2.render('|->', True, BLUE)
q750_text = font2.render('75|0>', True, BLUE)
q751_text = font2.render('75|1>', True, BLUE)

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to grid coordinates
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            # print("Click ", pos, "Grid coordinates: ", row, column)

        else: continue

        if row == 8 and column == 7:
            ismeasure=1
            qselected=None
        elif row==8 and column < 6:
            qselected=column
            ismeasure=0
        elif row<8 and playable[row][column]==1:
            # If user selected measure before this and the square he chose now has been played at and measurement has not been made there already
            if ismeasure and qplayed[row][column] != 0 and measured[row][column] == 0 and (countDigit(qplayed[row][column])==qmax[row][column]):
                qselected=None
                measured[row][column]=1
                movenumber+=1
                ismeasure = 0
                # measurement stuff: Call to measure move:
                qb.measurement_move([row,column])
                grid[row][column]=qb.classical_board[row][column]+1

            # Else if user has selected a qubit that is present in the bag, and user chooses a valid position
            elif (qselected is not None) and bag_counts[movenumber%2][qselected]>0 and ((countDigit(qplayed[row][column])<qmax[row][column]) or ([row,column] in [[3,5],[5,5],[3,3],[5,3]])) and isvalid(qplayed, row, column):
                qplayed[row][column] = 10*qplayed[row][column]+qselected+1
                bag_counts[movenumber%2][qselected] -= 1
                grid[row][column] = 10+qselected
                qselected = None
                movenumber+=1
                ismeasure=0
                # print(movenumber)
                # print(bag_counts)
                
                #qiskit stuff: Call to move:
                if(countDigit(qplayed[row][column])==qmax[row][column]):
                    qb.move([row,column], qplayed[row][column])
            else: continue
 
    # Set the screen background
    screen.fill(BLACK)
    fracts = [1,0,0.5,0.5,0.75,0.25]
 
    # Draw the grid
    for row1 in range(10):
        for column1 in range(8):
            color = WHITE
            if grid[row1][column1] == 1:
                color = GREEN
            if grid[row1][column1] == 2:
            	color = BLACK
            if grid[row1][column1] == 4:
            	color = LG
            if grid[row1][column1] == 3:
            	color = GRAY

            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column1 + MARGIN,
                              (MARGIN + HEIGHT) * row1 + MARGIN,
                              WIDTH,
                              HEIGHT])
            if row1<8:
            	if (countDigit(qplayed[row1][column1])==1 and measured[row1][column1]==0):
	            	pygame.draw.rect(screen,
	            		LG,
	            		[(MARGIN + WIDTH) * column1 + MARGIN,
	            		(MARGIN + HEIGHT) * row1 + MARGIN,
	            		WIDTH*(fracts[grid[row1][column1]-10]),
	            		HEIGHT])
	            	pygame.draw.rect(screen,
	                	GRAY,
	                	[(MARGIN + WIDTH) * column1 + MARGIN+WIDTH*(fracts[grid[row1][column1]-10]),
	                	(MARGIN + HEIGHT) * row1 + MARGIN,
	                	WIDTH*(1-fracts[grid[row1][column1]-10]),
	                	HEIGHT])
            	elif countDigit(qplayed[row1][column1])>1 and measured[row1][column1]==0:
            		pygame.draw.rect(screen,
	            		LG,
	            		[(MARGIN + WIDTH) * column1 + MARGIN,
	            		(MARGIN + HEIGHT) * row1 + MARGIN,
	            		WIDTH*(fracts[int(qplayed[row1][column1]/10)-1])/2,
	            		HEIGHT])
	            	pygame.draw.rect(screen,
	                	GRAY,
	                	[(MARGIN + WIDTH) * column1 + MARGIN+WIDTH*(fracts[int(qplayed[row1][column1]/10)-1])/2,
	                	(MARGIN + HEIGHT) * row1 + MARGIN,
	                	WIDTH*(1-(fracts[int(qplayed[row1][column1]/10)-1]))/2,
	                	HEIGHT])
            		pygame.draw.rect(screen,
            		LG,
            		[(MARGIN + WIDTH) * column1 + MARGIN+WIDTH/2,
            		(MARGIN + HEIGHT) * row1 + MARGIN,
            		WIDTH/2,
            		HEIGHT*(fracts[grid[row1][column1]-10])])
            		pygame.draw.rect(screen,
	                	GRAY,
	                	[(MARGIN + WIDTH) * column1 + MARGIN+WIDTH/2,
	                	(MARGIN + HEIGHT) * row1 + MARGIN+HEIGHT*(fracts[grid[row1][column1]-10]),
	                	WIDTH/2,
	                	HEIGHT*(1-fracts[grid[row1][column1]-10])])



            if row1==8:
                if(column1==2 or column1 == 3):
                    pygame.draw.rect(screen,
                             LG,
                             [(MARGIN + WIDTH) * column1 + MARGIN,
                              (MARGIN + HEIGHT) * row1 + MARGIN,
                              WIDTH/2,
                              HEIGHT])
                    pygame.draw.rect(screen,
                             GRAY,
                             [(MARGIN + WIDTH) * column1 + MARGIN+WIDTH/2,
                              (MARGIN + HEIGHT) * row1 + MARGIN,
                              WIDTH/2,
                              HEIGHT])
                if column1 == 4:
                    pygame.draw.rect(screen,
                             LG,
                             [(MARGIN + WIDTH) * column1 + MARGIN,
                              (MARGIN + HEIGHT) * row1 + MARGIN,
                              3*WIDTH/4,
                              HEIGHT])
                    pygame.draw.rect(screen,
                             GRAY,
                             [(MARGIN + WIDTH) * column1 + MARGIN+3*WIDTH/4,
                              (MARGIN + HEIGHT) * row1 + MARGIN,
                              WIDTH/4,
                              HEIGHT])
                if column1 == 5:
                    pygame.draw.rect(screen,
                             LG,
                             [(MARGIN + WIDTH) * column1 + MARGIN,
                              (MARGIN + HEIGHT) * row1 + MARGIN,
                              WIDTH/4,
                              HEIGHT])
                    pygame.draw.rect(screen,
                             GRAY,
                             [(MARGIN + WIDTH) * column1 + MARGIN+WIDTH/4,
                              (MARGIN + HEIGHT) * row1 + MARGIN,
                              3*WIDTH/4,
                              HEIGHT])
                if column1 == 7:
                    pygame.draw.rect(screen,
                             RED,
                             [(MARGIN + WIDTH) * column1 + MARGIN,
                              (MARGIN + HEIGHT) * row1 + MARGIN,
                              WIDTH,
                              HEIGHT])
            for i, rect in enumerate(en_rects):
                if(i%3==0):
            	    screen.blit(en_text1, rect)
                else:
                    screen.blit(en_text2, rect)
            
            for rect in cx_rects:
            	screen.blit(cx_text, rect)
            
            for rect in h_rects:
            	screen.blit(h_text, rect)
            
            for rect in x_rects:
            	screen.blit(x_text, rect)
            color = [GREEN, BLACK]
            for i in range(6):
            	text = font.render(str(int(bag_counts[movenumber%2][i])), True, color[movenumber%2])
            	screen.blit(text, bag_rects[i])
            screen.blit(m_text, m_rect)
            screen.blit(q0_text, centerlist[8][0])
            screen.blit(q1_text, centerlist[8][1])
            screen.blit(qplus_text, centerlist[8][2])
            screen.blit(qminus_text, centerlist[8][3])
            screen.blit(q750_text, centerlist[8][4])
            screen.blit(q751_text, centerlist[8][5])

 
    # Limit to 60 frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()