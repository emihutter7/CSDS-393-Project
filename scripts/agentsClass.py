import pygame

# Represents agents (students and faculty) on the screen
class Agent:
    def __init__(self, x, y, color, speed, path_end):
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed
        self.path_start = (x, y)
        self.path_end = path_end
        self.direction = 1  # 1 = forward, -1 = backward
        if x < path_end[0] or y < path_end[1]:
            self.direction = 1
        else:
            self.direction = -1

# Moves agents straight between start and end; reverse when hitting endpoints
    def move_along_path(self):
        sx, sy = self.path_start
        ex, ey = self.path_end

        # Horizontal movement
        if sy == ey:
            self.x += self.speed * self.direction

            # Check boundaries
            if self.direction == 1 and self.x >= ex:
                self.x = ex
                self.direction = -1
            elif self.direction == -1 and self.x <= sx:
                self.x = sx
                self.direction = 1

        # Vertical movement
        elif sx == ex:
            self.y += self.speed * self.direction

            # Check boundaries
            if self.direction == 1 and self.y >= ey:
                self.y = ey
                self.direction = -1
            elif self.direction == -1 and self.y <= sy:
                self.y = sy
                self.direction = 1

    def draw(self, window):
        pass  # Defined in subclasses

# Class creating students on the map represented by green triangles
class Student(Agent):
    def draw(self, window):
        # Draw a small green triangle
        points = [
            (self.x, self.y - 8),
            (self.x - 6, self.y + 6),
            (self.x + 6, self.y + 6)
        ]
        pygame.draw.polygon(window, (0, 255, 0), points)

# Class creating administration on the map represented by circles
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
