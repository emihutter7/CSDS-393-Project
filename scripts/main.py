## imports
import numpy as np
import sys
import pygame

## define constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

WINDOW_SIZE = (1200, 700) # set an arbitrary value, fix later
WINDOW_TITLE = "Kaler Simulator"
WINDOW = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption(WINDOW_TITLE)

pygame.init()
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    WINDOW.fill(GRAY)
    pygame.display.update()

    ## whenever keystroke is recognized/button is pressed, update using handlers here

pygame.quit()
sys.exit() # will not close in ipynb because it is an interactive environment, just displays the error