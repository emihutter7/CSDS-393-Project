import numpy as np
import sys
import pygame
import random

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
        print(f"START={self.path_start[1]}, END={self.path_end[1]}, CURRENT={self.y}")


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
