## imports
import sys
import pygame
from .menu import MenuManager, Menu 
from .agentsClass import Student, Admin, Player
import random

pygame.init()

## define constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
STEEL_BLUE = (70, 130, 180)  # Steel Blue
WINDOW_HEIGHT = 830
WINDOW_WIDTH = 1200
WINDOW_SIZE = (1200, 830) # set an arbitrary value, fix later
WINDOW_TITLE = "Kaler Simulator"
SYS_FONT = pygame.font.SysFont(None, 24)

# setup the original game state
pygame.display.set_caption(WINDOW_TITLE)
WINDOW = pygame.display.set_mode(WINDOW_SIZE)
current_state = 'MENU'
running = True

# To test the menu, can change based on other UI elements

# nrv menu
def show_nrv_menu():
    global menu_manager
    
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

# leutner menu
def show_leut_menu():
    global menu_manager
    
    def leut_actions():
        print("placeholder_callback")
        
    leut_menu = Menu(
        menu_manager=menu_manager,
        title="Building Menu",
        text="Adjust visual and simulation options",
        user_options=[
            ("APPLY", leut_actions),
            ("CLOSE", lambda: print("Settings closed.")) 
        ],
        user_closable=True
    )
    menu_manager.open_menu(leut_menu)

# ksl menu
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

# wyant menu
def show_wyant_menu():
    global menu_manager
    
    def wyant_actions():
        print("placeholder_callback")
        
    wyant_menu = Menu(
        menu_manager=menu_manager,
        title="Building Menu",
        text="Adjust visual and simulation options",
        user_options=[
            ("APPLY", wyant_actions),
            ("CLOSE", lambda: print("Settings closed.")) 
        ],
        user_closable=True
    )
    menu_manager.open_menu(wyant_menu)

# pbl menu
def show_pbl_menu():
    global menu_manager
    
    def pbl_actions():
        print("placeholder_callback")
        
    pbl_menu = Menu(
        menu_manager=menu_manager,
        title="Building Menu",
        text="Adjust visual and simulation options",
        user_options=[
            ("APPLY", pbl_actions),
            ("CLOSE", lambda: print("Settings closed.")) 
        ],
        user_closable=True
    )
    menu_manager.open_menu(pbl_menu)

# tink menu
def show_tink_menu():
    global menu_manager
    
    def tink_actions():
        print("placeholder_callback")
        
    tink_menu = Menu(
        menu_manager=menu_manager,
        title="Building Menu",
        text="Adjust visual and simulation options",
        user_options=[
            ("APPLY", tink_actions),
            ("CLOSE", lambda: print("Settings closed.")) 
        ],
        user_closable=True
    )
    menu_manager.open_menu(tink_menu) 

# thwing menu
def show_thwing_menu():
    global menu_manager
    
    def thwing_actions():
        print("placeholder_callback")
        
    thwing_menu = Menu(
        menu_manager=menu_manager,
        title="Building Menu",
        text="Adjust visual and simulation options",
        user_options=[
            ("APPLY", thwing_actions),
            ("CLOSE", lambda: print("Settings closed.")) 
        ],
        user_closable=True
    )
    menu_manager.open_menu(thwing_menu)

# srv menu
def show_srv_menu():
    global menu_manager
    
    def srv_actions():
        print("placeholder_callback")
        
    srv_menu = Menu(
        menu_manager=menu_manager,
        title="Building Menu",
        text="Adjust visual and simulation options",
        user_options=[
            ("APPLY", srv_actions),
            ("CLOSE", lambda: print("Settings closed.")) 
        ],
        user_closable=True
    )
    menu_manager.open_menu(srv_menu)

# ford menu
def show_ford_menu():
    global menu_manager
    
    def ford_actions():
        print("placeholder_callback")
        
    ford_menu = Menu(
        menu_manager=menu_manager,
        title="Building Menu",
        text="Adjust visual and simulation options",
        user_options=[
            ("APPLY", ford_actions),
            ("CLOSE", lambda: print("Settings closed.")) 
        ],
        user_closable=True
    )
    menu_manager.open_menu(ford_menu)

# frib menu
def show_frib_menu():
    global menu_manager
    
    def frib_actions():
        print("placeholder_callback")
        
    frib_menu = Menu(
        menu_manager=menu_manager,
        title="Building Menu",
        text="Adjust visual and simulation options",
        user_options=[
            ("APPLY", frib_actions),
            ("CLOSE", lambda: print("Settings closed.")) 
        ],
        user_closable=True
    )
    menu_manager.open_menu(frib_menu)

# veale menu
def show_veale_menu():
    global menu_manager
    
    def veale_actions():
        print("placeholder_callback")
        
    veale_menu = Menu(
        menu_manager=menu_manager,
        title="Veale Menu",
        text="Adjust visual and simulation options",
        user_options=[
            ("APPLY", veale_actions),
            ("CLOSE", lambda: print("Settings closed.")) 
        ],
        user_closable=True
    )
    menu_manager.open_menu(veale_menu)

# glennan menu
def show_glen_menu():
    global menu_manager
    
    def glen_actions():
        print("placeholder_callback")
        
    glen_menu = Menu(
        menu_manager=menu_manager,
        title="Glennan Menu",
        text="Adjust visual and simulation options",
        user_options=[
            ("APPLY", glen_actions),
            ("CLOSE", lambda: print("Settings closed.")) 
        ],
        user_closable=True
    )
    menu_manager.open_menu(glen_menu)

# white menu
def show_white_menu():
    global menu_manager
    
    def white_actions():
        print("placeholder_callback")
        
    white_menu = Menu(
        menu_manager=menu_manager,
        title="White Building Menu",
        text="Adjust visual and simulation options",
        user_options=[
            ("APPLY", white_actions),
            ("CLOSE", lambda: print("Settings closed.")) 
        ],
        user_closable=True
    )
    menu_manager.open_menu(white_menu)

# olin menu
def show_olin_menu():
    global menu_manager
    
    def olin_actions():
        print("placeholder_callback")
        
    olin_menu = Menu(
        menu_manager=menu_manager,
        title="Olin Building Menu",
        text="Adjust visual and simulation options",
        user_options=[
            ("APPLY", olin_actions),
            ("CLOSE", lambda: print("Settings closed.")) 
        ],
        user_closable=True
    )
    menu_manager.open_menu(olin_menu)

# nord menu
def show_nord_menu():
    global menu_manager
    
    def nord_actions():
        print("placeholder_callback")
        
    nord_menu = Menu(
        menu_manager=menu_manager,
        title="Nord Building Menu",
        text="Adjust visual and simulation options",
        user_options=[
            ("APPLY", nord_actions),
            ("CLOSE", lambda: print("Settings closed.")) 
        ],
        user_closable=True
    )
    menu_manager.open_menu(nord_menu)

# sears menu
def show_sears_menu():
    global menu_manager
    
    def sears_actions():
        print("placeholder_callback")
        
    sears_menu = Menu(
        menu_manager=menu_manager,
        title="Sears Building Menu",
        text="Adjust visual and simulation options",
        user_options=[
            ("APPLY", sears_actions),
            ("CLOSE", lambda: print("Settings closed.")) 
        ],
        user_closable=True
    )
    menu_manager.open_menu(sears_menu)

# wickenden menu
def show_wick_menu():
    global menu_manager
    
    def wick_actions():
        print("placeholder_callback")
        
    wick_menu = Menu(
        menu_manager=menu_manager,
        title="Wickenden Building Menu",
        text="Adjust visual and simulation options",
        user_options=[
            ("APPLY", wick_actions),
            ("CLOSE", lambda: print("Settings closed.")) 
        ],
        user_closable=True
    )
    menu_manager.open_menu(wick_menu)

# iseb menu
def show_iseb_menu():
    global menu_manager
    
    def iseb_actions():
        print("placeholder_callback")
        
    iseb_menu = Menu(
        menu_manager=menu_manager,
        title="ISEB Building Menu",
        text="Adjust visual and simulation options",
        user_options=[
            ("APPLY", iseb_actions),
            ("CLOSE", lambda: print("Settings closed.")) 
        ],
        user_closable=True
    )
    menu_manager.open_menu(iseb_menu)

# tomlinson menu
def show_tmlsn_menu():
    global menu_manager
    
    def tm_actions():
        print("placeholder_callback")
        
    tm_menu = Menu(
        menu_manager=menu_manager,
        title="Tomlinson Building Menu",
        text="Adjust visual and simulation options",
        user_options=[
            ("APPLY", tm_actions),
            ("CLOSE", lambda: print("Settings closed.")) 
        ],
        user_closable=True
    )
    menu_manager.open_menu(tm_menu)

# crawford menu
def show_crwfrd_menu():
    global menu_manager
    
    def craw_actions():
        print("placeholder_callback")
        
    craw_menu = Menu(
        menu_manager=menu_manager,
        title="Crawford Building Menu",
        text="Adjust visual and simulation options",
        user_options=[
            ("APPLY", craw_actions),
            ("CLOSE", lambda: print("Settings closed.")) 
        ],
        user_closable=True
    )
    menu_manager.open_menu(craw_menu)

# adelbert menu
def show_adlbrt_menu():
    global menu_manager
    
    def bert_actions():
        print("placeholder_callback")
        
    bert_menu = Menu(
        menu_manager=menu_manager,
        title="Adelbert College Menu",
        text="Adjust visual and simulation options",
        user_options=[
            ("APPLY", bert_actions),
            ("CLOSE", lambda: print("Settings closed.")) 
        ],
        user_closable=True
    )
    menu_manager.open_menu(bert_menu)

# rockefeller
def show_rockflr_menu():
    global menu_manager
    
    def rock_actions():
        print("placeholder_callback")
        
    rock_menu = Menu(
        menu_manager=menu_manager,
        title="Rockefeller Building Menu",
        text="Adjust visual and simulation options",
        user_options=[
            ("APPLY", rock_actions),
            ("CLOSE", lambda: print("Settings closed.")) 
        ],
        user_closable=True
    )
    menu_manager.open_menu(rock_menu)

# strosacker menu
def show_strskr_menu():
    global menu_manager
    
    def stro_actions():
        print("placeholder_callback")
        
    stro_menu = Menu(
        menu_manager=menu_manager,
        title="Strosacker Building Menu",
        text="Adjust visual and simulation options",
        user_options=[
            ("APPLY", stro_actions),
            ("CLOSE", lambda: print("Settings closed.")) 
        ],
        user_closable=True
    )
    menu_manager.open_menu(stro_menu)

# aw smith menu
def show_smith_menu():
    global menu_manager
    
    def smith_actions():
        print("placeholder_callback")
        
    smith_menu = Menu(
        menu_manager=menu_manager,
        title="AW Smith Building Menu",
        text="Adjust visual and simulation options",
        user_options=[
            ("APPLY", smith_actions),
            ("CLOSE", lambda: print("Settings closed.")) 
        ],
        user_closable=True
    )
    menu_manager.open_menu(smith_menu)

# binghm menu
def show_bghm_menu():
    global menu_manager
    
    def bing_actions():
        print("placeholder_callback")
        
    bing_menu = Menu(
        menu_manager=menu_manager,
        title="Bingham Building Menu",
        text="Adjust visual and simulation options",
        user_options=[
            ("APPLY", bing_actions),
            ("CLOSE", lambda: print("Settings closed.")) 
        ],
        user_closable=True
    )
    menu_manager.open_menu(bing_menu)

# schmitt menu
def show_schmitt_menu():
    global menu_manager
    
    def schmitt_actions():
        print("placeholder_callback")
        
    schmitt_menu = Menu(
        menu_manager=menu_manager,
        title="Millis Schmitt Building Menu",
        text="Adjust visual and simulation options",
        user_options=[
            ("APPLY", schmitt_actions),
            ("CLOSE", lambda: print("Settings closed.")) 
        ],
        user_closable=True
    )
    menu_manager.open_menu(schmitt_menu)

# keep track of input for triggering event
def check_input(key, value):
    if key == pygame.K_LEFT:
        player_input["left"] = value or key == pygame.K_a
    elif key == pygame.K_RIGHT:
        player_input["right"] = value or key == pygame.K_d
    elif key == pygame.K_UP:
        player_input["up"] = value or key == pygame.K_w
    elif key == pygame.K_DOWN:
        player_input["down"] = value or key == pygame.K_s

player_x = 0 # initial x position of player
player_y = 0 # initial x position of player
player_input = {"left": False, "right": False, "up": False, "down": False, "select": False}
player_velocity = [0, 0] # [x, y] how much player changes

# set up the main menu
main_menu_data = [
    ("NRV Dorms", show_nrv_menu, (370, 120, 80, 80)),
    ("Leutner", show_leut_menu, (400, 70, 50, 50)),
    ("Wyant", show_wyant_menu, (500, 20, 50, 50)),
    ("PBL", show_pbl_menu, (330, 310, 70, 70)),
    ("Tink UC", show_tink_menu, (400, 380, 50, 100)),
    ("Thwing", show_thwing_menu, (460, 430, 60, 40)),
    ("KSL", show_ksl_menu, (345, 490, 70, 70)),
    ("SRV Dorms", show_srv_menu, (900, 600, 70, 70)),
    ("Allen Ford", show_ford_menu, (480, 570, 50, 50)),
    ("Fribley", show_frib_menu, (890, 675, 50, 50)),
    ("Veale", show_veale_menu, (800, 750, 70, 70)),
    ("Glennan", show_glen_menu, (730, 770, 50, 50)),
    ("White", show_white_menu, (680, 770, 50, 50)),
    ("Olin", show_olin_menu, (630, 770, 50, 50)),
    ("Nord", show_nord_menu, (570, 770, 50, 50)),
    ("Sears", show_sears_menu, (520, 770, 50, 50)),
    ("Wick.", show_wick_menu, (460, 770, 50, 50)),
    ("ISEB", show_iseb_menu, (410, 770, 50, 50)),
    ("Tomlinson", show_tmlsn_menu, (360, 770, 50, 50)),
    ("Crawford", show_crwfrd_menu, (340, 700, 50, 50)),
    ("Adelbert", show_adlbrt_menu, (390, 630, 50, 50)),
    ("Rockefeller", show_rockflr_menu, (480, 660, 50, 50)),
    ("Strosacker", show_strskr_menu, (530, 660, 50, 50)),
    ("AW Smith", show_smith_menu, (580, 660, 50, 50)),
    ("Bingham", show_bghm_menu, (650, 700, 50, 50)),
    ("Schmitt", show_schmitt_menu, (540, 600, 50, 50)),
]
menu_manager = MenuManager(main_data=main_menu_data)

# all agents start at x=600 and move vertically between y=200 and y=500
students = [Student(600, random.randint(10, 800), (0, 255, 0), speed=0.05, path_end=(600, 830)) for _ in range(4)]

admins = [Admin(600, random.randint(10, 800), (0, 0, 0), speed=0.05, path_end=(600, 800)) for _ in range(2)]

# main game loop
def main():
    global current_state, running, player_x, player_y, player_input, player_velocity, students, admins
    while running:

        # handle all the events
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
            
            if event.type == pygame.KEYDOWN:
                check_input(event.key, True)
            if event.type == pygame.KEYUP:
                check_input(event.key, False)

        WINDOW.fill(GRAY)

        # create player
        player = Player(200, 300)

        # all agents start at x=600 and move vertically between y=200 and y=500
        students = [Student(600, random.randint(10, 800), (0, 255, 0), speed=0.05, path_end=(600, 830)) for _ in range(4)]

        admins = [Admin(600, random.randint(10, 800), (0, 0, 0), speed=0.01, path_end=(600, 800)) for _ in range(2)]

        player_velocity[0] = player_input['right'] - player_input['left'] # velocity in X direction. If right is true then 1 - 0 = 1, if left is tru thenn 0 - 1 = -1
        player_velocity[1] = player_input['up'] - player_input['down'] # velocity in Y direction. If up is true then 1 - 0 = 1, if downn is tru thenn 0 - 1 = -1

        player_x += player_velocity[0] * 5
        player_y += player_velocity[1] * 5

        # move & draw AI agents
        for s in students:
            s.move_along_path()
            s.draw(WINDOW)

        for a in admins:
            a.move_along_path()
            a.draw(WINDOW)

        # left panels
        pygame.draw.rect(WINDOW, STEEL_BLUE, (0, 0, WINDOW_WIDTH // 6, 100))
        pygame.draw.rect(WINDOW, BLACK, (0, 0, WINDOW_WIDTH // 6, 100), width=3)
        WINDOW.blit(SYS_FONT.render("Budget", True, BLACK), (10, 10))

        pygame.draw.rect(WINDOW, STEEL_BLUE, (0, 100, WINDOW_WIDTH // 6, 500))
        pygame.draw.rect(WINDOW, BLACK, (0, 100, WINDOW_WIDTH // 6, 500), width=3)
        WINDOW.blit(SYS_FONT.render("Tasks", True, BLACK), (10, 110))

        pygame.draw.rect(WINDOW, STEEL_BLUE, (0, 600, WINDOW_WIDTH // 6, 230))
        pygame.draw.rect(WINDOW, BLACK, (0, 600, WINDOW_WIDTH // 6, 230), width=3)
        WINDOW.blit(SYS_FONT.render("Semester", True, BLACK), (10, 610))

        # right panels
        pygame.draw.rect(WINDOW, STEEL_BLUE, (1000, 0, WINDOW_WIDTH - WINDOW_WIDTH // 6, 830))
        pygame.draw.rect(WINDOW, BLACK, (1000, 0, WINDOW_WIDTH - WINDOW_WIDTH // 6, 830), width=3)
        WINDOW.blit(SYS_FONT.render("Metrics", True, BLACK), (1010, 10))

        if current_state == 'MENU':
            menu_manager.draw(WINDOW)
            
        pygame.display.update()

    pygame.quit()
    sys.exit() # will not close in ipynb because it is an interactive environment, just displays the error

if __name__ == "__main__":
    main()