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
def show_nrv_menu():
    global menu_manager
    
    # Define the final button actions for the menu
    def confirm_upgrade():
        print("placeholder handler")

    def cancel_action():
        print("Action: Start cancelled by user.")

    nrv_menu = Menu(
        menu_manager=menu_manager,
        title="North Residential Village Dorms",
        text="You can upgrade the building from 1 to 2. Do you wish to proceed?",
        user_options=[
            ("PROCEED", confirm_upgrade),
            ("CANCEL", cancel_action)
        ],
        user_closable=True
    )
    menu_manager.open_menu(nrv_menu)
    
def show_ksl_menu():
    global menu_manager
    
    def ksl_actions():
        print("placeholder_callback")
        
    ksl_menu = Menu(
        menu_manager=menu_manager,
        title="Building Menu",
        text="Adjust visual and simulation options",
        user_options=[
            ("APPLY", ksl_actions),
            ("CLOSE", lambda: print("Settings closed.")) 
        ],
        user_closable=True
    )
    menu_manager.open_menu(ksl_menu)

# set up the main menu
main_menu_data = [
    ("NRV Dorms", show_nrv_menu, (500, 400, 200, 200)),
    ("KSL", show_ksl_menu, (500, 10, 400, 200)), 
]

menu_manager = MenuManager(main_data=main_menu_data)

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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: #and current_state == 'SIMULATING'
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
            
        pygame.display.update()

    pygame.quit()
    sys.exit() # will not close in ipynb because it is an interactive environment, just displays the error

if __name__ == "__main__":
    main()