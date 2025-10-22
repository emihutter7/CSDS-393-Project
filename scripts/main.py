## imports
import numpy as np
import sys
import pygame
from menu import MenuManager, Menu 

pygame.init()

## define constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
STEEL_BLUE = (70, 130, 180)  # Steel Blue

WINDOW_HEIGHT = 700
WINDOW_WIDTH = 1200
WINDOW_SIZE = (1200, 700) # set an arbitrary value, fix later
WINDOW_TITLE = "Kaler Simulator"

pygame.display.set_caption(WINDOW_TITLE)

WINDOW = pygame.display.set_mode(WINDOW_SIZE)
SYS_FONT = pygame.font.SysFont(None, 24)
current_state = 'MENU'
running = True

''' To test the menu things, can change based on other UI elements for the demo'''
def set_state_to_simulating():
    global current_state
    current_state = 'SIMULATING'
    print("Action: Simulation Started!")

def show_start_menu():
    global menu_manager
    
    # Define the final button actions for the menu
    def confirm_start():
        set_state_to_simulating()
        
    def cancel_action():
        print("Action: Start cancelled by user.")

    start_menu = Menu(
        menu_manager=menu_manager,
        title="Confirm Simulation Start",
        text="Starting the simulation will clear any current progress and launch the environment. Do you wish to proceed?",
        user_options=[
            ("PROCEED", confirm_start),
            ("CANCEL", cancel_action)
        ],
        user_closable=True # Allows the user to close via the 'X' button
    )
    # Activate the menu
    menu_manager.open_menu(start_menu)
    
def show_settings_menu():
    global menu_manager
    
    def apply_settings():
        print("placeholder")
        
    settings_menu = Menu(
        menu_manager=menu_manager,
        title="Building Menu",
        text="Adjust visual and simulation options",
        user_options=[
            ("APPLY", apply_settings),
            ("CLOSE", lambda: print("Settings closed.")) 
        ],
        button_dimensions={
        "width": 500,
        "height": 200,
        "spacing": 20,
        "bottom_offset": 20
        },
        user_closable=True
    )
    menu_manager.open_menu(settings_menu)

# set up the main menu
main_menu_data = [
    ("START SIMULATION", show_start_menu),
    ("SETTINGS", show_settings_menu),
]

menu_manager = MenuManager(main_menu_data)

def main():
    global current_state, running
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # menu-manager handles the main buttons and the active popup 
            if current_state == 'MENU':
                menu_manager.handle_event(event)
            
            # can change later
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and current_state == 'SIMULATING':
                    current_state = 'MENU'
                    print("Transitioning back to MENU state.")
        
        WINDOW.fill(GRAY)

        # left panels
        pygame.draw.rect(WINDOW, STEEL_BLUE, (0, 0, WINDOW_WIDTH // 6, 100))
        pygame.draw.rect(WINDOW, BLACK, (0, 0, WINDOW_WIDTH // 6, 100), width=3)
        WINDOW.blit(SYS_FONT.render("Budget", True, BLACK), (10, 10))

        pygame.draw.rect(WINDOW, STEEL_BLUE, (0, 100, WINDOW_WIDTH // 6, 500))
        pygame.draw.rect(WINDOW, BLACK, (0, 100, WINDOW_WIDTH // 6, 500), width=3)
        WINDOW.blit(SYS_FONT.render("Tasks", True, BLACK), (10, 110))

        pygame.draw.rect(WINDOW, STEEL_BLUE, (0, 600, WINDOW_WIDTH // 6, 200))
        pygame.draw.rect(WINDOW, BLACK, (0, 600, WINDOW_WIDTH // 6, 200), width=3)
        WINDOW.blit(SYS_FONT.render("Semester", True, BLACK), (10, 610))

        # right panels
        pygame.draw.rect(WINDOW, STEEL_BLUE, (1000, 0, WINDOW_WIDTH - WINDOW_WIDTH // 6, 700))
        pygame.draw.rect(WINDOW, BLACK, (1000, 0, WINDOW_WIDTH - WINDOW_WIDTH // 6, 700), width=3)
        WINDOW.blit(SYS_FONT.render("Metrics", True, BLACK), (1010, 10))

        if current_state == 'MENU':

            menu_manager.draw(WINDOW)
            
        elif current_state == 'SIMULATING':
            # Simulation drawing logic will go here
            font_sim = pygame.font.Font(None, 24)
            sim_text = font_sim.render("SIMULATION ACTIVE (Press SPACE to return)", True, BLACK)
            sim_rect = sim_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            WINDOW.blit(sim_text, sim_rect)


        pygame.display.update()

    pygame.quit()
    sys.exit() # will not close in ipynb because it is an interactive environment, just displays the error

if __name__ == "__main__":
    main()