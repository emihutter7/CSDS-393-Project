import sys
import pygame as py
import random
import json
import os
#import tkinter as tk
#from tkinter import filedialog
from .config import *
from .Button import Button
from .agentsClass import Admin, Student, Player
#from .MetricsClass import Metrics
#from .Popups import PopupEvent
from .menu import Menu, MenuManager
import numpy as np

# main loop set up, with the screen, clock, and state manager created
class Game:
    def __init__(self):
        py.init()
        self.screen = py.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) #py.RESIZABLE - if we want to make it full screen, we have to resize EVERYTHING
        self.clock = py.time.Clock()

        self.current_state = "Main Menu"
        self.font = py.font.SysFont(None, 24)
        self.gameStateManager = GameStateManager(self.current_state)
        self.start = StartGame(self.screen, self.font, self.gameStateManager)
        self.load = LoadGame(self.screen, self.font, self.start, self.gameStateManager)
        self.main_opt = MainGameMenu(self.screen, self.font, self.gameStateManager)
        self.in_game_opt = InGameMenu(self.screen, self.font, self.start, self.gameStateManager)

        self.states = {
            "Main Menu" : self.main_opt,
            "Start Game" : self.start,
            "Load Game" : self.load,
            "In-Game Menu" : self.in_game_opt
        }

    # main run loop, calling run methods from the current state
    def run(self):
        while True:

            self.screen.fill(BLACK)

            self.states[self.gameStateManager.get_current_state()].run() 
            
            py.display.update()
            self.clock.tick(FPS)

# first game menu screen
# option to load or start a new game
class MainGameMenu():
    def __init__(self, screen, font, gameStateManager):
        self.screen = screen
        self.gameStateManager = gameStateManager
        self.font = font

        button_width = 300
        button_height = 90
        spacing = 50  # space between buttons
        center_x = WINDOW_WIDTH // 2 - button_width // 2
        title_y = WINDOW_HEIGHT // 5
        start_y = WINDOW_HEIGHT // 2 - button_height - spacing // 2
        load_y = start_y + button_height + spacing

        self.title_font = py.font.Font(None, 130)  # large clean title font
        self.title_y = title_y

        self.load_button = Button(dimensions=(center_x, start_y, button_width, button_height), # dimensions should be x,y,width,height
                                  text = "Load Saved Game",
                                  callback = lambda new_state = "Load Game" : self.gameStateManager.set_current_state(new_state),
                                  fontsize=46)
        
        self.start_button = Button(dimensions=(center_x, load_y, button_width, button_height), # dimensions should be x,y,width,height
                                  text = "Start New Game",
                                  callback = lambda : self.gameStateManager.set_current_state("Start Game"),
                                  fontsize=46)
        
    def run(self):

        self.screen.fill(BLACK)

        title_surface = self.title_font.render("Main Menu", True, WHITE)
        title_rect = title_surface.get_rect(center = (WINDOW_WIDTH // 2, self.title_y))
        self.screen.blit(title_surface, title_rect)


        self.load_button.draw(self.screen)
        self.start_button.draw(self.screen)

        for event in py.event.get():
            if event.type == py.QUIT:
                    py.quit()
                    sys.exit()

            self.load_button.handle_event(event)
            self.start_button.handle_event(event)

# this is where the core game logic is
# this starts the game - has the agents, menu manager (for the buildings), agents, next semester button
# FIXME need to incorporate the tasks/popups (can create menu callbacks like in show_building_menu) and the metrics/budget display
# FIXME for tasks - was thinking a dynamic list of buttons with a menu opening on click
# FIXME for metrics populating, we can create a metrics class object and have all the metrics in here? idk
# FIXME for building logic - we need to have a building class that can have a dictionary with building name as key and level #, need an upgrade building function
class StartGame():
    def __init__(self, screen, font, gameStateManager):
        # general game logic
        self.menu_manager = MenuManager(main_data=[])
        self.screen = screen
        self.gameStateManager = gameStateManager
        self.font = font
        self.panel_width = WINDOW_WIDTH // 6

        # metrics and popups
        self.budget = 100000
        self.tasks = [] # was thinking a list of buttons that will cause popup to open
        self.semester = 1
        self.help_button = Button(dimensions=(WINDOW_WIDTH - 125, 20, 120, 40), # dimensions should be x,y,width,height
                                  text="Help",
                                  callback=lambda: self.gameStateManager.set_current_state("In-Game Menu"),
                                  base_color=BUTTON_COLOR,
                                  hover_color=BUTTON_HOVER,
                                  text_color=TEXT_COLOR)
        self.next_semester_button = Button(dimensions=(10, WINDOW_HEIGHT - 150, 180, 60),
                                    text="Next Semester",
                                    callback=self.next_sem,
                                    base_color=BUTTON_COLOR,
                                    hover_color=BUTTON_HOVER,
                                    text_color=TEXT_COLOR)
        # for the menu manager - the last param is if you want it to be an image that you upload for the button
        # if we put all images in the images folder, the relative directory will be easier to follow
        # dimensions should be x,y,width,height
        self.building_data = [
            ("NRV Dorms", lambda : self.show_building_menu("NRV Dorms"), (370, 120, 80, 80), "../images/testing2.png"),
            ("Leutner", lambda : self.show_building_menu("Leutner"), (400, 70, 50, 50)),
            ("Wyant", lambda : self.show_building_menu("Wyant"), (500, 20, 50, 50)),
            ("PBL", lambda : self.show_building_menu("PBL"), (330, 310, 70, 70)),
            ("Tink UC", lambda : self.show_building_menu("Tink UC"), (400, 380, 50, 100)),
            ("Thwing", lambda : self.show_building_menu("Thwing"), (460, 430, 60, 40)),
            ("KSL", lambda : self.show_building_menu("KSL"), (345, 490, 70, 70)),
            ("SRV Dorms", lambda : self.show_building_menu("SRV Dorms"), (900, 600, 70, 70)),
            ("Allen Ford", lambda : self.show_building_menu("Allen Ford"), (480, 570, 50, 50)),
            ("Fribley", lambda : self.show_building_menu("Fribley"), (890, 675, 50, 50)),
            ("Veale", lambda : self.show_building_menu("Veale"), (800, 750, 70, 70)),
            ("Glennan", lambda : self.show_building_menu("Glennan"), (730, 770, 50, 50)),
            ("White", lambda : self.show_building_menu("White"), (680, 770, 50, 50)),
            ("Olin", lambda : self.show_building_menu("Olin"), (630, 770, 50, 50)),
            ("Nord", lambda : self.show_building_menu("Nord"), (570, 770, 50, 50)),
            ("Sears", lambda : self.show_building_menu("Sears"), (520, 770, 50, 50)),
            ("Wick.", lambda : self.show_building_menu("Wick."), (460, 770, 50, 50)),
            ("ISEB", lambda : self.show_building_menu("ISEB"), (410, 770, 50, 50)),
            ("Tomlinson", lambda : self.show_building_menu("Tomlinson"), (360, 770, 50, 50)),
            ("Crawford", lambda : self.show_building_menu("Crawford"), (340, 700, 50, 50)),
            ("Adelbert", lambda : self.show_building_menu("Adelbert"), (390, 630, 50, 50)),
            ("Rockefeller", lambda : self.show_building_menu("Rockefeller"), (480, 660, 50, 50)),
            ("Strosacker", lambda : self.show_building_menu("Strosacker"), (530, 660, 50, 50)),
            ("AW Smith", lambda : self.show_building_menu("AW Smith"), (580, 660, 50, 50)),
            ("Bingham", lambda : self.show_building_menu("Bingham"), (650, 700, 50, 50)),
            ("Schmitt", lambda : self.show_building_menu("Schmitt"), (540, 600, 50, 50)),
        ]
        self.menu_manager.main_setup(self.building_data)

        # player and agents data
        self.admins = [Admin(600, random.randint(10, 800), (0, 0, 0), speed=0.05, path_end=(600, 800)) for _ in range(2)]
        self.students = [Student(600, random.randint(10, 800), (0, 255, 0), speed=0.05, path_end=(600, 830)) for _ in range(4)]
        self.player = Player(200, 300)
        self.player_velocity = [0, 0]
        self.player_input = {"left": False, "right": False, "up": False, "down": False, "select": False}
        self.player_x = 0
        self.player_y = 0
    
    # FIXME need some way to make sure that it notifies user that you can't use it if task is not empty
    def next_sem(self):
        if self.semester < 8 and len(self.tasks) == 0:
            self.semester += 1

    # generic building menu
    def show_building_menu(self, building_name):
        def upgrade():
            # placeholder (have upgrade menu from the building_name dictionary or something
            # upgrade_building func should take in building name as param and update dictionary
            self.menu_manager.close_menu()

        def close_menu():
            print("Action: Start cancelled by user.")

        # Building menu
        menu = Menu(
            menu_manager=self.menu_manager,
            title= building_name + " Menu",
            text=f"Do you want to upgrade?",
            user_options=[
                ("UPGRADE", upgrade),
                ("CLOSE", close_menu)
            ],
            user_closable=True
        )
        self.menu_manager.open_menu(menu)
    
    # checking user input
    def check_input(self, key, value):
        if key == py.K_LEFT:
            self.player_input["left"] = value or key == py.K_a
        elif key == py.K_RIGHT:
            self.player_input["right"] = value or key == py.K_d
        elif key == py.K_UP:
            self.player_input["up"] = value or key == py.K_w
        elif key == py.K_DOWN:
            self.player_input["down"] = value or key == py.K_s

    # playing game loop
    def run(self):

        self.screen.fill(TAN_BG)

        # Left-side panels
        # --- Budget panel ---
        py.draw.rect(self.screen, PANEL_COLOR, (0, 0, self.panel_width, 100))
        py.draw.rect(self.screen, BORDER_COLOR, (0, 0, self.panel_width, 100), width=3)
        self.screen.blit(self.font.render("Budget", True, TEXT_COLOR), (15, 15))

        # --- Tasks panel ---
        py.draw.rect(self.screen, PANEL_COLOR, (0, 100, self.panel_width, 500))
        py.draw.rect(self.screen, BORDER_COLOR, (0, 100, self.panel_width, 500), width=3)
        self.screen.blit(self.font.render("Tasks", True, TEXT_COLOR), (15, 110))

        # --- Semester panel ---
        semester_panel_y = 600
        py.draw.rect(self.screen, PANEL_COLOR, (0, semester_panel_y, self.panel_width, 230))
        py.draw.rect(self.screen, BORDER_COLOR, (0, semester_panel_y, self.panel_width, 230), width=3)
        self.screen.blit(self.font.render(f"Semester: {self.semester}", True, TEXT_COLOR), (15, semester_panel_y + 15))

        # Right-side metrics panel (adjusted so Help button sits above)
        metrics_panel_x = WINDOW_WIDTH - self.panel_width
        py.draw.rect(self.screen, PANEL_COLOR, (metrics_panel_x, 70, self.panel_width, WINDOW_HEIGHT - 70))
        py.draw.rect(self.screen, BORDER_COLOR, (metrics_panel_x, 70, self.panel_width, WINDOW_HEIGHT - 70), width=3)
        self.screen.blit(self.font.render("Metrics", True, TEXT_COLOR), (metrics_panel_x + 15, 80))

        # event handling logic
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            if event.type == py.KEYDOWN:
                self.check_input(event.key, True)
            if event.type == py.KEYUP:
                self.check_input(event.key, False)
            self.menu_manager.handle_event(event)
            self.help_button.handle_event(event)
            self.next_semester_button.handle_event(event)

        # agents logic
        self.students = [Student(600, random.randint(10, 800), (0, 255, 0), speed=0.05, path_end=(600, 830)) for _ in range(4)]
        self.admins = [Admin(600, random.randint(10, 800), (0, 0, 0), speed=0.01, path_end=(600, 800)) for _ in range(2)]

        self.player_velocity[0] = self.player_input['right'] - self.player_input['left'] # velocity in X direction. If right is true then 1 - 0 = 1, if left is tru thenn 0 - 1 = -1
        self.player_velocity[1] = self.player_input['up'] - self.player_input['down'] # velocity in Y direction. If up is true then 1 - 0 = 1, if downn is tru thenn 0 - 1 = -1

        self.player_x += self.player_velocity[0] * 5
        self.player_y += self.player_velocity[1] * 5

        # move & draw AI agents
        for s in self.students:
            s.move_along_path()
            s.draw(self.screen)

        for a in self.admins:
            a.move_along_path()
            a.draw(self.screen)

        # draw all other buttons
        self.next_semester_button.draw(self.screen)
        self.help_button.draw(self.screen)
        self.menu_manager.draw(self.screen)

# this is the loading screen - must prompt user to select a file off of desktop and load
# FIXME func of load_game not implemented, need sql database
class LoadGame():
    def __init__(self, screen, font, start, gameStateManager):
        self.screen = screen
        self.gameStateManager = gameStateManager
        self.font = font
        self.start = start
        self.title_font = py.font.Font(None, 130)

        button_width = 300
        button_height = 90
        spacing = 50  # space between buttons
        center_x = WINDOW_WIDTH // 2 - button_width // 2
        title_y = WINDOW_HEIGHT // 5
        start_y = WINDOW_HEIGHT // 2 - button_height - spacing // 2
        load_y = start_y + button_height + spacing
        
        self.title_y = title_y

        self.back_button = Button(dimensions=(center_x, load_y, button_width, button_height),
                                  text="Back",
                                  callback=lambda: self.gameStateManager.set_current_state("Main Menu"),
                                  fontsize=46)
        self.load_button = Button(dimensions=(center_x, start_y, button_width, button_height),
                                  text="Select Saved Game",
                                  callback=self.load_game,
                                  fontsize=46)
    
    # FIXME add propoer functionality for SQL
    def load_game(self):
        # read a user inputted file
        self.start.player = None #placeholder, data should come from the database

    def run(self):
        self.screen.fill(BLACK)

        title_surface = self.title_font.render("Load a Saved Game", True, WHITE)
        title_rect = title_surface.get_rect(center = (WINDOW_WIDTH // 2, self.title_y))
        self.screen.blit(title_surface, title_rect)

        # drawing the button on the screen
        self.load_button.draw(self.screen)
        self.back_button.draw(self.screen)

        # event handling logic
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            self.load_button.handle_event(event)
            self.back_button.handle_event(event)

# this is the in game menu that opens when you click the help button
# includes save and close button for now
# FIXME save button is pulling all the data from start (game logic) and saving to json currently
# FIXME need to change functionality/format for SQL (just placed here to see if it works)
class InGameMenu():
    def __init__(self, screen, font, start, gameStateManager):
        self.screen = screen
        self.font = font
        self.gameStateManager = gameStateManager
        self.start = start
        self.overlay_color = GRAY
        self.title_font = py.font.Font(None, 130)

        button_width = 300
        button_height = 90
        spacing = 50  # space between buttons
        center_x = WINDOW_WIDTH // 2 - button_width // 2
        title_y = WINDOW_HEIGHT // 5
        start_y = WINDOW_HEIGHT // 2 - button_height - spacing // 2
        load_y = start_y + button_height + spacing

        self.title_y = title_y

        self.close_button = Button(dimensions=(center_x, load_y, button_width, button_height),
                                  text = "Close",
                                  callback = lambda new_state = "Start Game" : self.gameStateManager.set_current_state(new_state),
                                  fontsize=46)
        self.save_button = Button(dimensions=(center_x, start_y, button_width, button_height),
                                  text = "Save Game",
                                  callback = self.save_game,
                                  fontsize=46)
    
    # FIXME - (needs to be sql, was just testing functionality with this)
    def save_game(self):
        try:
            ## FIXME need to make sure everything (metrics, etc) are ALL being saved
            data = {
                "player": {
                    "x": self.start.player_x,
                    "y": self.start.player_y,
                },
                "player_velocity": self.start.player_velocity,
                "tasks": getattr(self.start.tasks),
                "budget": getattr(self.start.budget),
                "admins": len(self.start.admins),
                "students": len(self.start.students)
            }

            save_path = os.path.join(os.path.expanduser("~"), "Desktop", "save_game.json")
            with open(save_path, "w") as f:
                json.dump(data, f, indent=4) ## FIXME change to db.execute or something (for sql compatability)

            print(f"Game saved successfully to {save_path}")

        except Exception as e:
            print("Error saving game:", e)
    
    def run(self):
        # draw overlay
        self.screen.fill(BLACK)

        title_surface = self.title_font.render("Menu", True, WHITE)
        title_rect = title_surface.get_rect(center = (WINDOW_WIDTH // 2, self.title_y))
        self.screen.blit(title_surface, title_rect)

        # draw buttons
        self.save_button.draw(self.screen)
        self.close_button.draw(self.screen)

        # event handling logic
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            self.save_button.handle_event(event)
            self.close_button.handle_event(event)

# manages state switching logic
class GameStateManager:
    def __init__(self, current_state):
        self.current_state = current_state

    def get_current_state(self):
        return self.current_state
    
    def set_current_state(self, new_state):
        self.current_state = new_state

if __name__ == '__main__':

    game = Game()
    game.run()