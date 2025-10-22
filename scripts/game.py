## imports
import numpy as np
import sys
import pygame
import random

## define constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

WINDOW_SIZE = (1200, 700) # set an arbitrary value, fix later
WINDOW_TITLE = "Kaler Simulator"

pygame.init()

WINDOW = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption(WINDOW_TITLE)
CLOCK = pygame.time.Clock()

player_x = 0 # initial x position of player
player_y = 0 # initial x position of player
player_input = {"left": False, "right": False, "up": False, "down": False, "select": False}
player_velocity = [0, 0] # [x, y] how much player changes

button_list = []

selected_button = None

def check_input(key, value):
    if key == pygame.K_LEFT:
        player_input["left"] = value or key == pygame.K_a
    elif key == pygame.K_RIGHT:
        player_input["right"] = value or key == pygame.K_d
    elif key == pygame.K_UP:
        player_input["up"] = value or key == pygame.K_w
    elif key == pygame.K_DOWN:
        player_input["down"] = value or key == pygame.K_s

def check_selection(mouse_pos):
    for button in button_list:
        if button.collidepoint(mouse_pos):
            selected_button = button
            print(f"Clicked {button}")
            return
    selected_button = None

class Agent:
    def __init__(self, x, y, color, speed, path_end):
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed
        self.path_start = (x, y)
        self.path_end = path_end
        self.direction = 1  # 1 = forward, -1 = backward

    def move_along_path(self):
        # Move horizontally for now
        self.x += self.speed * self.direction
        if (self.direction == 1 and self.x >= self.path_end[0]) or \
           (self.direction == -1 and self.x <= self.path_start[0]):
            self.direction *= -1  # reverse direction

    def draw(self, window):
        pass  # will be defined in subclasses

class Student(Agent):
    def draw(self, window):
        # Draw a small green triangle
        points = [
            (self.x, self.y - 8),
            (self.x - 6, self.y + 6),
            (self.x + 6, self.y + 6)
        ]
        pygame.draw.polygon(window, (0, 255, 0), points)

class Admin(Agent):
    def draw(self, window):
        pygame.draw.circle(window, (0, 0, 0), (int(self.x), int(self.y)), 6)


class Player:
    def __init__(self, x, y, color=(0, 0, 255)):
        self.x = x
        self.y = y
        self.color = color
        self.size = 15

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.size, self.size))

running = True
while running:

    WINDOW.fill(GRAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            check_input(event.key, True)
        elif event.type == pygame.KEYUP:
            check_input(event.key, False)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            check_selection(pygame.mouse.get_pos())
        elif event.type == pygame.MOUSEBUTTONUP:
            if selected_button:
                selected_button = None

    
    # Create player
    player = Player(200, 300)

    # Create agents with straight-line paths
    students = [Student(random.randint(100, 400), random.randint(100, 400),
                        (0, 255, 0), speed=1.5, path_end=(500, random.randint(100, 400)))
                for _ in range(5)]

    admins = [Admin(random.randint(100, 400), random.randint(100, 400),
                    (0, 0, 0), speed=1, path_end=(550, random.randint(100, 400)))
            for _ in range(2)]

    player_velocity[0] = player_input['right'] - player_input['left'] # velocity in X direction. If right is true then 1 - 0 = 1, if left is tru thenn 0 - 1 = -1
    player_velocity[1] = player_input['up'] - player_input['down'] # velocity in Y direction. If up is true then 1 - 0 = 1, if downn is tru thenn 0 - 1 = -1

    pygame.draw.rect(WINDOW, RED, (0, 0, 100, 100)) # (WINDOW, COLOR, (X, Y, WIDTH, HEIGHT))
    pygame.draw.circle(WINDOW, BLUE, (0, 0, 100, 100)) 

    building_rect = pygame.Rect(100, 100, 200, 150)  # x, y, width, height

    player_x += player_velocity[0] * 5
    player_y += player_velocity[1] * 5

    # Move & draw AI agents
    for s in students:
        s.move_along_path()
        s.draw(WINDOW)

    for a in admins:
        a.move_along_path()
        a.draw(WINDOW)

    # Draw player
    player.draw(WINDOW)

    CLOCK.tick(60)

    pygame.display.update()



    ## whenever keystroke is recognized/button is pressed, update using handlers here

pygame.quit()
sys.exit() # will not close in ipynb because it is an interactive environment, just displays the error