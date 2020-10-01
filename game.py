import pygame
from qiskit import *
from pygame.locals import *

"""
 Example program to show using an array to back a grid on-screen.
 
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
 Explanation video: http://youtu.be/mdTeqiWyFnc
"""
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
 
# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 80
HEIGHT = 80
 
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
grid[4][3] = 1
grid[3][4] = 1
grid[4][4] = 2
grid[3][3] = 2
# Initialize pygame
pygame.init()
 
# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [WIDTH*8+MARGIN*7, WIDTH*8+MARGIN*7]
screen = pygame.display.set_mode(WINDOW_SIZE)
 
# Set title of screen
pygame.display.set_caption("Qthello")
 
# Loop until the user clicks the close button.
done = False

# Set the font
font=pygame.font.SysFont('arial', 40)

centerlist=[]
for row in range(8):
    alist=[]
    for column in range(8):
        alist.append(((MARGIN + WIDTH) * column + MARGIN + WIDTH/3, (MARGIN + HEIGHT) * row + MARGIN + HEIGHT/3))
    centerlist.append(alist)

s_text=font.render('S', True, BLUE)
s_rects=[centerlist[0][0],centerlist[0][7],centerlist[7][0],centerlist[7][7]]

cx_text=font.render('CX', True, BLUE)
cx_rects=[centerlist[1][1],centerlist[1][6],centerlist[6][1],centerlist[6][6]]

h_text=font.render('H', True, BLUE)
h_rects=[centerlist[0][2],centerlist[2][0],centerlist[0][5],centerlist[5][0],centerlist[7][5],centerlist[7][2],centerlist[5][7],centerlist[2][7]]

x_text=font.render('X', True, BLUE)
x_rects=[centerlist[2][2],centerlist[2][5],centerlist[5][2],centerlist[5][5]]

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
            print("Click ", pos, "Grid coordinates: ", row, column)
 
    # Set the screen background
    screen.fill(BLACK)
 
    # Draw the grid
    for row1 in range(8):
        for column1 in range(8):
            color = WHITE
            if grid[row1][column1] == 1:
                color = GREEN
            if grid[row1][column1] == 2:
            	color = BLACK
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column1 + MARGIN,
                              (MARGIN + HEIGHT) * row1 + MARGIN,
                              WIDTH,
                              HEIGHT])
            
            for rect in s_rects:
            	screen.blit(s_text, rect)
            
            for rect in cx_rects:
            	screen.blit(cx_text, rect)
            
            for rect in h_rects:
            	screen.blit(h_text, rect)
            
            for rect in x_rects:
            	screen.blit(x_text, rect)
 
    # Limit to 60 frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()