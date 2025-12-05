# First import all necessary libraries and initialize inheritance
import sys
import pygame as py
import random
import os
from .config import *
from .Button import Button
from .agentsClass import Admin, Student, Player
from .MetricsClass import Metrics
from .Popups import PopupEvent, minor_events, major_events
from .menu import Menu, MenuManager
from .GameState import GameState
from .db import db_init

# This class contains the main loop set up. It creates the screen, clock, and state manager
class Game:
    def __init__(self):
        py.init()
        self.screen = py.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) #py.RESIZABLE - if we want to make it full screen, we have to resize everything
        self.clock = py.time.Clock()

        db_init()

        self.current_state = "Auth"
        self.font = py.font.SysFont(None, 24)
        self.gameStateManager = GameStateManager(self.current_state)
        self.gameState = GameState()
        self.auth = LoginRegisterScreen(self.screen, self.font, self.gameStateManager)


        self.start = StartGame(self.screen, self.font, self.gameStateManager, self.gameState)
        self.load = LoadGame(self.screen, self.font, self.start, self.gameStateManager)
        self.main_opt = MainGameMenu(self.screen, self.font, self.gameStateManager)
        self.in_game_opt = InGameMenu(self.screen, self.font, self.start, self.gameStateManager)

        self.states = {
            "Auth": self.auth,
            "Main Menu" : self.main_opt,
            "Start Game" : self.start,
            "Load Game" : self.load,
            "In-Game Menu" : self.in_game_opt
        }

    # The main lopp that calls run methods from the current state
    def run(self):
        while True:

            self.screen.fill(BLACK)

            self.states[self.gameStateManager.get_current_state()].run() 
            
            py.display.update()
            self.clock.tick(FPS)

# This class generates the initial login/register screen for users to access the game
class LoginRegisterScreen:
    def __init__(self, screen, font, gameStateManager):
        self.screen = screen
        self.font = font
        self.gameStateManager = gameStateManager

        self.username = ""
        self.password = ""
        self.active_field = None
        self.message = ""

        cx = WINDOW_WIDTH // 2 - 200
        self.login_button = Button(
            (cx, 350, 400, 60), "Login",
            callback=self.login_user, fontsize=40
        )
        self.register_button = Button(
            (cx, 430, 400, 60), "Register",
            callback=self.register_user, fontsize=40
        )

    # Allows user to login if they have an existing account
    def login_user(self):
        from .db import authenticate_user, get_user_id
        if authenticate_user(self.username, self.password):
            self.gameStateManager.player_username = self.username
            self.gameStateManager.player_id = get_user_id(self.username)
            self.gameStateManager.set_current_state("Main Menu")
        else:
            self.message = "Invalid username or password"

    # Allows user to create an account, only if it does not already exist
    def register_user(self):
        from .db import create_user
        try:
            create_user(self.username, self.password)
            self.message = "Account created — login now."
        except:
            self.message = "Username already exists."

    # Creates the textboxes for user to input login/registration information
    def draw_textbox(self, x, y, w, h, text, active):
        color = (255,255,255) if active else (180,180,180)
        py.draw.rect(self.screen, color, (x,y,w,h))
        rendered = self.font.render(text, True, (0,0,0))
        self.screen.blit(rendered, (x+5, y+5))

    # Executes the functionality of the login/register screen 
    def run(self):
        self.screen.fill((20,20,20))

        textbox_width = 400
        textbox_height = 40
        top_left_x = WINDOW_WIDTH // 2 - 200
        start_y = 200  # y for username

        self.draw_textbox(top_left_x, start_y, textbox_width, textbox_height, self.username, self.active_field=="user")
        self.draw_textbox(top_left_x, start_y + 60, textbox_width, textbox_height, "*"*len(self.password), self.active_field=="pass")

        msg = self.font.render(self.message, True, (255,120,120))
        self.screen.blit(msg, (top_left_x, 300))

        self.login_button.draw(self.screen)
        self.register_button.draw(self.screen)

        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit(); sys.exit()

            # Focus fields
            if event.type == py.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if 300 <= mx <= 750:
                    if 180 <= my <= 225:
                        self.active_field = "user"
                    elif 240 <= my <= 285:
                        self.active_field = "pass"
                    else:
                        self.active_field = None

            # Typing
            if event.type == py.KEYDOWN and self.active_field:
                if event.key == py.K_BACKSPACE:
                    if self.active_field == "user":
                        self.username = self.username[:-1]
                    else:
                        self.password = self.password[:-1]
                else:
                    if self.active_field == "user":
                        self.username += event.unicode
                    else:
                        self.password += event.unicode

            self.login_button.handle_event(event)
            self.register_button.handle_event(event)

(''' After login/register, user is presented with screen that allows the option of loading 
an existing game or creating a new game. This class implements that screen.
''')
class MainGameMenu():
    def __init__(self, screen, font, gameStateManager):
        self.screen = screen
        self.gameStateManager = gameStateManager
        self.font = font

        button_width = 300
        button_height = 90
        spacing = 50  
        center_x = WINDOW_WIDTH // 2 - button_width // 2
        title_y = WINDOW_HEIGHT // 5
        start_y = WINDOW_HEIGHT // 2 - button_height - spacing // 2
        load_y = start_y + button_height + spacing

        self.title_font = py.font.Font(None, 130) 
        self.title_y = title_y

        self.load_button = Button(dimensions=(center_x, start_y, button_width, button_height), # dimensions should be x,y,width,height
                                  text = "Load Saved Game",
                                  callback = lambda new_state = "Load Game" : self.gameStateManager.set_current_state(new_state),
                                  fontsize=46)
        
        self.start_button = Button(dimensions=(center_x, load_y, button_width, button_height), # dimensions should be x,y,width,height
                                  text = "Start New Game",
                                  callback = lambda : self.gameStateManager.set_current_state("Start Game"),
                                  fontsize=46)
    # Executes the functionality of the main game menu  
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

(''' This class contains the core game logic that starts the game. It manages the agents, 
menu manager, and next semester button. ''')
class StartGame():
    def __init__(self, screen, font, gameStateManager, game_state):

        # General game logic
        self.menu_manager = MenuManager(main_data=[])
        self.screen = screen
        self.gameStateManager = gameStateManager
        self.font = font
        self.panel_width = WINDOW_WIDTH // 6
        self.game_state = game_state
        # Metrics and popups
        self.budget = 100000
        self.tasks = [] 
        self.semester = (self.game_state.turn + 1) // 2
        self.turn = self.game_state.turn
        self.turn = self.game_state.max_turns
        self.help_button = Button(dimensions=(WINDOW_WIDTH - 125, 20, 120, 40), # dimensions should be x,y,width,height
                                  text="Help",
                                  callback=lambda: self.gameStateManager.set_current_state("In-Game Menu"),
                                  base_color=BUTTON_COLOR,
                                  hover_color=BUTTON_HOVER,
                                  text_color=TEXT_COLOR)
        self.next_turn_button = Button(dimensions=(10, WINDOW_HEIGHT - 150, 180, 60),
                                    text="Next Turn",
                                    callback=self.next_sem,
                                    base_color=BUTTON_COLOR,
                                    hover_color=BUTTON_HOVER,
                                    text_color=TEXT_COLOR)
        
        raw_buildings = [
            ("NRV Dorms", (370, 120, 80, 80), None),
            ("Leut.",   (400, 70, 50, 50),  None),
            ("Wyan.",     (500, 20, 50, 50),  None),

            ("PBL",       (230, 210, 70, 70), None),
            ("Tink UC",   (300, 280, 50, 100), None),
            ("Thwing",    (360, 330, 60, 40), None),
            ("KSL",       (245, 390, 70, 70), None),
            ("SRV Dorms", (900, 600, 70, 70), None),

            ("Allen Ford", (450, 460, 50, 50), None),
            ("Frib.",    (890, 675, 50, 50), None),

            ("Veale",      (810, 750, 70, 70), None),
            ("Glen.",    (730, 770, 50, 50), None),
            ("White",      (675, 770, 50, 50), None),
            ("Olin",       (620, 770, 50, 50), None),

            ("Nord",       (550, 770, 50, 50), None),
            ("Sears",      (495, 770, 50, 50), None),

            ("Wick",       (425, 770, 50, 50), None),
            ("ISEB",       (370, 770, 50, 50), None),
            ("Toml.",  (315, 770, 50, 50), None),

            ("Craw.",   (290, 655, 50, 50), None),
            ("Adel.",   (340, 540, 50, 50), None),

            ("Rock.", (445, 585, 50, 50), None),
            ("Stros.",  (500, 585, 50, 50), None),
            ("AW Smith",    (555, 585, 50, 50), None),

            ("Bing.",     (630, 660, 50, 50), None),
            ("Schm.",     (510, 505, 50, 50), None),
        ]

        self.building_data = []
        for name, dims, img in raw_buildings:
            self.building_data.append([name, None, dims, img])
        
        self.menu_manager.main_setup(self.building_data)

        for entry, button in zip(self.building_data, self.menu_manager.main_buttons):

            # Store original name so text can be updated like "Veale 2"
            button.original_name = entry[0]

            # Set initial level
            button.level = 1
            self.menu_manager.building_levels[button.original_name] = button.level

            # Fix the callback so it knows which button it belongs to
            button.callback = lambda b=button: self.show_building_menu(b)

        # Speeds
        student_speeds = [1.4, 1.7, 2.0, 2.3, 2.6, 3.0]
        admin_speeds   = [0.7, 0.9, 1.1, 1.3, 1.5]

        # Road A (Lower Quad)
        roadA_left  = (336, 735)
        roadA_right = (756, 735)

        # Road B (Upper Quad)
        roadB_left  = (405, 660)
        roadB_right = (600, 660)

        # Student agents
        self.students = [
            # 1. KSL → Glennan (horizontal)
            Student(315, 425, (0,255,0), student_speeds[0], (765, 425)),
            Student(315, 425, (0,255,0), student_speeds[2], (765, 425)),

            # 2. Glennan → Tomlinson (horizontal)
            Student(336, 735, (0,255,0), student_speeds[3], (756, 735)),
            Student(336, 735, (0,255,0), student_speeds[1], (756, 735)),

            # 3. ISEB → Thwing (vertical)
            Student(405, 370, (0,255,0), student_speeds[5], (405, 735)),
            Student(405, 370, (0,255,0), student_speeds[1], (405, 735)),

            # 4. Wyant → KSL (vertical)
            Student(540, 70,  (0,255,0), student_speeds[2], (540, 425)),
            Student(540, 70,  (0,255,0), student_speeds[4], (540, 425)),

            # 5. KSL → Veale (vertical)
            Student(760, 425, (0,255,0), student_speeds[0], (760, 770)),
            Student(760, 425, (0,255,0), student_speeds[3], (760, 770)),

            # 6. Bingham → Crawford (horizontal)
            Student(405, 660, (0,255,0), student_speeds[4], (600, 660)),

            # 7. Leutner (horizontal)
            Student(400, 95,  (0,255,0), student_speeds[1], (540, 95)),

            # 8. SRV Dorms road (horizontal)
            Student(760, 635, (0,255,0), student_speeds[2], (900, 635)),

            # 9. Schmitt road (horizontal)
            Student(405, 530, (0,255,0), student_speeds[5], (535, 530)),

            # 10. Fribley road (horizontal)
            Student(760, 700, (0,255,0), student_speeds[1], (890, 700)),
        ]

        # Admin agents
        self.admins = [
            # 1. KSL → Glennan
            Admin(315, 425, (0,0,0), admin_speeds[1], (765, 425)),

            # 2. Glennan → Tomlinson
            Admin(336, 735, (0,0,0), admin_speeds[0], (756, 735)),

            # 3. ISEB → Thwing
            Admin(405, 370, (0,0,0), admin_speeds[3], (405, 735)),

            # 4. Wyant → KSL
            Admin(540, 70,  (0,0,0), admin_speeds[2], (540, 425)),

            # 5. KSL → Veale
            Admin(760, 425, (0,0,0), admin_speeds[4], (760, 770)),

            # 6. Bingham → Crawford
            Admin(405, 660, (0,0,0), admin_speeds[1], (600, 660)),

            # 7. Leutner
            Admin(400, 95,  (0,0,0), admin_speeds[3], (540, 95)),

            # 8. SRV Dorms
            Admin(760, 635, (0,0,0), admin_speeds[0], (900, 635)),

            # 9. Schmitt
            Admin(405, 530, (0,0,0), admin_speeds[2], (535, 530)),

            # 10. Fribley
            Admin(760, 700, (0,0,0), admin_speeds[4], (890, 700)),
        ]
        self.player = Player(200, 300)
        self.player_velocity = [0, 0]
        self.player_input = {"left": False, "right": False, "up": False, "down": False, "select": False}
        self.player_x = 0
        self.player_y = 0

        # Currently no popup open, will store temporary popup choice buttons
        self.active_popup = None       
        self.popup_context = None  # metadata about the current popup (e.g., task vs year-end)
        self.choice_buttons = []

        # Metrics initializing
        self.metrics = Metrics()
        self.year_start_metrics = self._metrics_snapshot()
        self.generate_tasks()
        
    
    # Locates popups within the game 
    def find_popup_by_name(self, name):
        # Search minor events
        for e in minor_events:
            if e.title == name:
                return e

        # Search major events
        for e in major_events:
            if e.title == name:
                return e

        return None

    # Implements next turn and semester logic
    # Ensures users complete all tasks before turning 
    def next_sem(self):

        # Only allow next turn if no active tasks
        if len(self.tasks) > 0:
            print("Finish all tasks before advancing!")
            return

        # Advance turn via GameState
        game_over = self.game_state.next_turn()
        self.semester = (self.game_state.turn + 1) // 2  

        # Check if game is over
        if game_over:
            self.show_final_score_screen()
            return

        # Year-end (every 4 turns) triggers a major event popup with metrics summary
        if self.game_state.turn % 4 == 0:
            self.show_year_end_popup()

        # Otherwise, generate new tasks
        self.generate_tasks()

    # Function that displays the user final score at the end of the game
    def show_final_score_screen(self):
        print(self.metrics.budget)

        weights = {
            "budget": 0.25,
            "prestige": 0.25,
            "sHappiness": 0.2,
            "aHappiness": 0.15,
            "security": 0.1,
            "academics": 0.1
        }

        # Compute normalized deltas
        delta_budget     = (self.metrics.budget - 450000000) / 450000000
        delta_prestige   = (self.metrics.prestige - 51) / 51
        delta_sHappiness = (self.metrics.sHappiness - 75) / 75
        delta_aHappiness = (self.metrics.aHappiness - 60) / 60
        delta_security   = (self.metrics.security - 50) / 50
        delta_academics  = (self.metrics.academics - 80) / 80

        # Weighted contributions
        contributions = {
            "budget": delta_budget * weights["budget"] * 100,
            "prestige": delta_prestige * weights["prestige"] * 100,
            "sHappiness": delta_sHappiness * weights["sHappiness"] * 100,
            "aHappiness": delta_aHappiness * weights["aHappiness"] * 100,
            "security": delta_security * weights["security"] * 100,
            "academics": delta_academics * weights["academics"] * 100
        }

        # Total final score
        total_score = sum(contributions.values())
        
        text = f"Game Over!   Your final score: {total_score:.2f}"

        # Build a nice text display
        lines = [f"Game Over!  Your final score: {total_score:.2f}\n"]
        for metric, value in contributions.items():
            lines.append(f"{metric}: {value:.2f}")

        menu = Menu(
            menu_manager=self.menu_manager,
            title="Game Over",
            text=text,
            user_options=[("EXIT", lambda: exit())],  # or return to main menu
            user_closable=False
        )

        self.menu_manager.open_menu(menu)


    # Displays a generic building menu
    def show_building_menu(self, building_button):
        b = building_button          # The actual button object
        name = b.original_name       # Original base name (like "Veale")
        lvl = b.level                # Current building level

        # Implements building upgrade logic
        def upgrade():
            if b.level < 3:
                b.level += 1
                b.text = f"{b.original_name} {b.level}"
                self.menu_manager.building_levels[b.original_name] = b.level
                self._apply_building_upgrade_effects()
            # Re-open menu so title updates
            self.menu_manager.close_menu()
            self.show_building_menu(b)

        # Exits building menu
        def close_menu():
            self.menu_manager.close_menu()

        menu = Menu(
            menu_manager=self.menu_manager,
            title=f"{name} Menu — Level {lvl}",
            text=f"{name} is currently Level {lvl}",
            user_options=[
                ("UPGRADE", upgrade),
                ("CLOSE", close_menu)
            ],
            user_closable=True
        )

        self.menu_manager.open_menu(menu)
    
    # Reads user input
    def check_input(self, key, value):
        if key == py.K_LEFT:
            self.player_input["left"] = value or key == py.K_a
        elif key == py.K_RIGHT:
            self.player_input["right"] = value or key == py.K_d
        elif key == py.K_UP:
            self.player_input["up"] = value or key == py.K_w
        elif key == py.K_DOWN:
            self.player_input["down"] = value or key == py.K_s
    
    # Applys metrics
    def apply_loaded_metrics(self, metrics):
        self.metrics.budget = metrics["score"]
        self.semester = 1 

    # Recreaates task on reloaded game
    def recreate_task_buttons(self, popup_dicts):
        self.tasks = []
        y_offset = 40

        for p in popup_dicts:
            popup_obj = self.find_popup_by_name(p["name"])

            if popup_obj is None:
                continue  # skip unknown

            btn = Button(
                dimensions=(20, y_offset, self.panel_width - 40, 50),
                text=popup_obj.title,
                callback=lambda e=popup_obj: self.open_popup(e),
                base_color=BUTTON_COLOR,
                hover_color=BUTTON_HOVER,
                text_color=TEXT_COLOR
            )

            self.tasks.append(btn)
            y_offset += 60

    # Function that saves the game when a player exits 
    def auto_save_on_exit(self):
        from .db import save_game_for_user
        player_id = self.gameStateManager.player_id

        # Collect data
        metrics = { "score": self.metrics.budget, "time_of_year": "Fall" }
        buildings = self.menu_manager.get_building_levels()

        # Convert tasks to popup dicts
        popups = []
        for btn in self.tasks:
            popups.append({
                "name": btn.text,
                "is_active": True,
                "already_completed": False
            })

        save_game_for_user(player_id, metrics, buildings, popups)
        print("Auto-save completed for player", player_id)

    # Playing game loop
    def run(self):

        self.screen.fill(TAN_BG)

        # Tasks panel
        py.draw.rect(self.screen, PANEL_COLOR, (0, 0, self.panel_width, 600))
        py.draw.rect(self.screen, BORDER_COLOR, (0, 0, self.panel_width, 600), width=3)
        self.screen.blit(self.font.render("Tasks", True, TEXT_COLOR), (15, 15))

        # Semester panel
        semester_panel_y = 600
        py.draw.rect(self.screen, PANEL_COLOR, (0, semester_panel_y, self.panel_width, 230))
        py.draw.rect(self.screen, BORDER_COLOR, (0, semester_panel_y, self.panel_width, 230), width=3)
        self.screen.blit(self.font.render(f"Semester: {self.semester}", True, TEXT_COLOR), (15, semester_panel_y + 15))

        # Right-side metrics panel (adjusted so Help button sits above)
        metrics_panel_x = WINDOW_WIDTH - self.panel_width
        py.draw.rect(self.screen, PANEL_COLOR, (metrics_panel_x, 70, self.panel_width, WINDOW_HEIGHT - 70))
        py.draw.rect(self.screen, BORDER_COLOR, (metrics_panel_x, 70, self.panel_width, WINDOW_HEIGHT - 70), width=3)
        self.screen.blit(self.font.render("Metrics", True, TEXT_COLOR), (metrics_panel_x + 15, 80))

        # Draws metrics
        metrics_x = WINDOW_WIDTH - self.panel_width + 15
        y = 110
        for label, value in [
            ("Budget", f"${self.metrics.budget:,}"),
            ("Prestige", self.metrics.prestige),
            ("Stud. Happiness", self.metrics.sHappiness),
            ("Admin Happiness", self.metrics.aHappiness),
            ("Security", self.metrics.security),
            ("Academics", self.metrics.academics)
        ]:
            self.screen.blit(self.font.render(f"{label}: {value}", True, TEXT_COLOR), (metrics_x, y))
            y += 30

        # Event handling logic
        for event in py.event.get():
            if event.type == py.QUIT:
                print("Detected window close — auto-saving game...")
                self.auto_save_on_exit()
                py.quit()
                sys.exit()
            if event.type == py.KEYDOWN:
                self.check_input(event.key, True)
            if event.type == py.KEYUP:
                self.check_input(event.key, False)
            self.menu_manager.handle_event(event)
            self.help_button.handle_event(event)
            self.next_turn_button.handle_event(event)
            for btn in self.tasks:
                btn.handle_event(event)
            # Handle popup choice button clicks when popup open
            if self.active_popup:
                for btn in self.choice_buttons:
                    btn.handle_event(event)
            

 

        road_vertical_wyant_to_ksl     = ((525, 70),  (525, 525))
        road_horizontal_ksl_to_glennan = ((525, 525), (780, 525))
        road_vertical_glennan_to_veale = ((780, 525), (780, 810))
        road_horizontal_veale_to_olin  = ((800, 810), (630, 810))
        ROAD_COLOR = (100, 100, 100)
        ROAD_WIDTH = 10

        # 1. Wyant → KSL
        py.draw.line(self.screen, ROAD_COLOR, (540, 70),  (540, 425), ROAD_WIDTH)

        # 2. KSL → Glennan
        py.draw.line(self.screen, ROAD_COLOR, (315, 425), (765, 425), ROAD_WIDTH)

        # 3. KSL → Veale vertical drop
        py.draw.line(self.screen, ROAD_COLOR, (760, 425), (760, 770), ROAD_WIDTH)

        # 4. Veale → Glennan
        py.draw.line(self.screen, ROAD_COLOR, (810, 760), (756, 760), ROAD_WIDTH)

        # 5. Glennan → Tomlinson   LOWER QUAD
        py.draw.line(self.screen, ROAD_COLOR, (756, 735), (336, 735), ROAD_WIDTH)

        # 6. Nord → Bingham   vertical upwards in quad
        py.draw.line(self.screen, ROAD_COLOR, (600, 735), (600, 656), ROAD_WIDTH)

        # 7. Bingham → Crawford   UPPER QUAD
        py.draw.line(self.screen, ROAD_COLOR, (600, 660), (405, 660), ROAD_WIDTH)

        # 8. ISEB → Thwing   vertical upwards from quad
        py.draw.line(self.screen, ROAD_COLOR, (405, 735), (405, 370), ROAD_WIDTH)

        # Vertical roads down into the bottom quad row (Tomlinson → White)
        py.draw.line(self.screen, ROAD_COLOR, (340, 735), (340, 770), ROAD_WIDTH)   # Tomlinson
        py.draw.line(self.screen, ROAD_COLOR, (395, 735), (395, 770), ROAD_WIDTH)   # ISEB
        py.draw.line(self.screen, ROAD_COLOR, (450, 735), (450, 770), ROAD_WIDTH)   # Wick
        py.draw.line(self.screen, ROAD_COLOR, (520, 735), (520, 770), ROAD_WIDTH)   # Sears
        py.draw.line(self.screen, ROAD_COLOR, (575, 735), (575, 770), ROAD_WIDTH)   # Nord
        py.draw.line(self.screen, ROAD_COLOR, (655, 735), (655, 770), ROAD_WIDTH)   # Olin
        py.draw.line(self.screen, ROAD_COLOR, (700, 735), (700, 770), ROAD_WIDTH)   # White

        # Vertical roads DOWN into the upper quad (Strosacker, Rockefeller, A.W. Smith)
        py.draw.line(self.screen, ROAD_COLOR, (470, 660), (470, 635), ROAD_WIDTH)   # Rockefeller
        py.draw.line(self.screen, ROAD_COLOR, (525, 660), (525, 635), ROAD_WIDTH)   # Strosacker
        py.draw.line(self.screen, ROAD_COLOR, (580, 660), (580, 635), ROAD_WIDTH)   # AW Smith

        # 1. To SRV Dorms (y-mid = 635)
        py.draw.line(self.screen, ROAD_COLOR, (760, 635), (900, 635), ROAD_WIDTH)

        # 2. To Fribley (y-mid = 700)
        py.draw.line(self.screen, ROAD_COLOR, (760, 700), (890, 700), ROAD_WIDTH)

        # Horizontal roads LEFT from x=405
        py.draw.line(self.screen, ROAD_COLOR, (405, 680), (315, 680), ROAD_WIDTH)   # Crawford
        py.draw.line(self.screen, ROAD_COLOR, (405, 565), (365, 565), ROAD_WIDTH)   # Adelbert

        # Horizontal roads RIGHT from x=405
        py.draw.line(self.screen, ROAD_COLOR, (405, 530), (535, 530), ROAD_WIDTH)   # Schmitt
        py.draw.line(self.screen, ROAD_COLOR, (405, 485), (475, 485), ROAD_WIDTH)   # Allen Ford

        # 1. Vertical KSL → PBL
        py.draw.line(self.screen, ROAD_COLOR, (280, 390), (280, 280), ROAD_WIDTH)

        # 2. Horizontal from that same x to Tink UC
        py.draw.line(self.screen, ROAD_COLOR, (280, 330), (300, 330), ROAD_WIDTH)

        # Horizontal roads LEFT from x = 540
        py.draw.line(self.screen, ROAD_COLOR, (540, 95), (400, 95), ROAD_WIDTH)    # Leutner
        py.draw.line(self.screen, ROAD_COLOR, (540, 160), (450, 160), ROAD_WIDTH)  # NRV Dorms

        # Rightward road toward Bingham
        py.draw.line(self.screen, ROAD_COLOR, (600, 685), (630, 685), ROAD_WIDTH)

        # Field 1
        field1_rect = py.Rect(420, 670, 165, 55)   
        py.draw.rect(self.screen, (34,139,34), field1_rect, border_radius=12)
        py.draw.rect(self.screen, (0,0,0), field1_rect, width=3, border_radius=12)

        # Field 2
        field2_rect = py.Rect(625, 450, 110, 185)  
        py.draw.rect(self.screen, (34,139,34), field2_rect, border_radius=12)
        py.draw.rect(self.screen, (0,0,0), field2_rect, width=3, border_radius=12)

        # Outer brick rectangle
        outer_field_rect = py.Rect(580, 20, 230, 140)
        py.draw.rect(self.screen, (178, 34, 34), outer_field_rect)  # brick color
        py.draw.rect(self.screen, (0,0,0), outer_field_rect, width=4)  # black border

        # Inner rounded green field
        inner_field_rect = py.Rect(590, 30, 210, 120)
        py.draw.rect(self.screen, (34,139,34), inner_field_rect, border_radius=18)
        py.draw.rect(self.screen, (255,255,255), inner_field_rect, width=3, border_radius=18)  # white border

        # Vertical white lines inside the mega field
        num_lines = 10
        spacing = inner_field_rect.width / (num_lines + 1)

        for i in range(1, num_lines + 1):
            x = inner_field_rect.x + int(i * spacing)
            py.draw.line(
                self.screen,
                (255, 255, 255),  
                (x, inner_field_rect.y),
                (x, inner_field_rect.y + inner_field_rect.height - 1),
                2  # Line thickness
            )

        # Agents logic
        self.player_velocity[0] = self.player_input['right'] - self.player_input['left'] # velocity in X direction. If right is true then 1 - 0 = 1, if left is tru thenn 0 - 1 = -1
        self.player_velocity[1] = self.player_input['up'] - self.player_input['down'] # velocity in Y direction. If up is true then 1 - 0 = 1, if downn is tru thenn 0 - 1 = -1

        self.player_x += self.player_velocity[0] * 5
        self.player_y += self.player_velocity[1] * 5

        for s in self.students:
            s.move_along_path()
            s.draw(self.screen)

        for a in self.admins:
            a.move_along_path()
            a.draw(self.screen)

        # Draw all other buttons
        self.next_turn_button.draw(self.screen)
        self.help_button.draw(self.screen)
        self.menu_manager.draw(self.screen)

        # Draw task buttons
        for btn in self.tasks:
            btn.draw(self.screen)
        
        if self.active_popup:
            self.draw_popup()

    # Logic that generates popups/tasks to be completed by the user
    def generate_tasks(self):
        # Clear old tasks
        self.tasks.clear()
        tasks_to_add = []
        if self.semester % 2 == 1:   # start of semester
            tasks_to_add = random.sample(minor_events, 2)
        else:                        # end of semester
            tasks_to_add = random.sample(minor_events, 1) + random.sample(major_events, 1)

        y_offset = 40
        for event in tasks_to_add:
            btn = Button(
                dimensions=(20, y_offset, self.panel_width - 40, 50),
                text=event.title,
                callback=lambda e=event: self.open_popup(e),
                base_color=BUTTON_COLOR,
                hover_color=BUTTON_HOVER,
                text_color=TEXT_COLOR
            )
            self.tasks.append(btn)
            y_offset += 60

    # Allows popup to display when player clicks on it
    def open_popup(self, event):
        self.active_popup = event
        self.popup_context = {"type": "task"}

    # Displays final popup event at the end of the academic year (2 semester) for player to respond to
    def show_year_end_popup(self):
        # Pick a major event to present as the year-end choice
        event = random.choice(major_events)
        self.active_popup = event
        self.popup_context = {
            "type": "year_end",
            "year_number": ((self.game_state.turn - 1) // 4) + 1
        }
    
    def _wrap_text(self, surface, text, font, x, y, max_width):
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + (" " if current_line else "") + word

            # Case 1: Fits normally
            if font.size(test_line)[0] <= max_width:
                current_line = test_line

            else:
                # Case 2: Current line exists → push it and start new line
                if current_line:
                    lines.append(current_line)
                    current_line = word
                else:
                    # Case 3: Long single word — force break character-by-character
                    split_word = ""
                    for ch in word:
                        if font.size(split_word + ch)[0] <= max_width:
                            split_word += ch
                        else:
                            lines.append(split_word)
                            split_word = ch
                    current_line = split_word

        if current_line:
            lines.append(current_line)

        # Draw the lines
        for line in lines:
            text_surface = font.render(line, True, TEXT_COLOR)
            surface.blit(text_surface, (x, y))
            y += font.get_linesize()

    
    ('''Render current metrics and delta since year start inside the popup rect.
        Returns the next y position to continue drawing (after the summary block). ''')
    def _render_metric_deltas(self, rect, start_y=None, include_header=False):
        if not self.year_start_metrics:
            return (start_y or rect.y + 160)

        font = py.font.Font(None, 22)
        header_font = py.font.Font(None, 26)
        y = start_y if start_y is not None else (rect.y + 140)

        if include_header:
            header = header_font.render("End of Year Metrics Summary", True, TEXT_COLOR)
            self.screen.blit(header, (rect.x + 20, y))
            y += header_font.get_linesize() + 6
        lines = []
        current = {
            "budget": self.metrics.budget,
            "prestige": self.metrics.prestige,
            "sHappiness": self.metrics.sHappiness,
            "aHappiness": self.metrics.aHappiness,
            "security": self.metrics.security,
            "academics": self.metrics.academics
        }

        for key, label in [
            ("budget", "Budget"),
            ("prestige", "Prestige"),
            ("sHappiness", "Stud. Happiness"),
            ("aHappiness", "Admin Happiness"),
            ("security", "Security"),
            ("academics", "Academics")
        ]:
            start_val = self.year_start_metrics.get(key, 0)
            delta = current[key] - start_val
            if key == "budget":
                current_str = f"${current[key]:,}"
                delta_str = f"{'+' if delta >= 0 else ''}${delta:,}"
            else:
                current_str = str(current[key])
                delta_str = f"{'+' if delta >= 0 else ''}{delta}"
            lines.append(f"{label}: {current_str} ({delta_str})")

        for line in lines:
            text_surface = font.render(line, True, TEXT_COLOR)
            self.screen.blit(text_surface, (rect.x + 20, y))
            y += font.get_linesize() + 2

        return y + 10

    # Displays any popups on screen 
    def draw_popup(self):
        popup = self.active_popup
        if not popup:
            return
        rect = py.Rect(WINDOW_WIDTH//2 - 320, WINDOW_HEIGHT//2 - 250, 640, 500)
        py.draw.rect(self.screen, PANEL_COLOR, rect)
        py.draw.rect(self.screen, BORDER_COLOR, rect, 3)

        # Draw title & description
        title_surf = self.font.render(popup.title, True, TEXT_COLOR)
        desc_surf = self.font.render(popup.description, True, TEXT_COLOR)

        self._wrap_text(surface=self.screen, 
                        text=popup.description, 
                        font=py.font.Font(None, 24), 
                        x=rect.x + 20, 
                        y=rect.y + 60, 
                        max_width=rect.width - 60)

        self.screen.blit(title_surf, (rect.x + 20, rect.y + 20))

        # Set starting y for choices
        self.choice_buttons = []
        y = rect.y + 120

        # Draw choices as buttons
        for i, choice in enumerate(popup.choices):
            btn = Button(
                dimensions=(rect.x + 100, y, 400, 40),
                text=choice.text,
                callback=lambda idx=i: self.choose_option(idx),
                base_color=BUTTON_COLOR,
                hover_color=BUTTON_HOVER,
                text_color=TEXT_COLOR
            )
            btn.draw(self.screen)
            self.choice_buttons.append(btn)
            y += 60

        # For year-end popups, render metric deltas below the choices with a header
        if self.popup_context and self.popup_context.get("type") == "year_end":
            self._render_metric_deltas(rect, start_y=y + 10, include_header=True)

    # Allows user to choose one of the options from the popup task
    def choose_option(self, idx):
        self.active_popup.trigger_choice(idx, self.metrics)
        # Remove this task from task list if it came from tasks
        if self.popup_context and self.popup_context.get("type") == "task":
            self.tasks = [t for t in self.tasks if t.text != self.active_popup.title]

        # After year-end, reset snapshot for the new year
        if self.popup_context and self.popup_context.get("type") == "year_end":
            self.year_start_metrics = self._metrics_snapshot()

        self.active_popup = None
        self.popup_context = None

    (''' Apply immediate metric effects when a building is upgraded.
        Defaults can be adjusted as needed. ''')
    def _apply_building_upgrade_effects(self):
        budget_cost = -2_000_000
        prestige_gain = 2
        academics_gain = 2
        student_hap_gain = 1
        admin_hap_gain = 1
        security_gain = 1

        # Prevent negative budget crashes
        new_budget = max(0, self.metrics.budget + budget_cost)
        self.metrics.budget = new_budget
        self.metrics.prestige += prestige_gain
        self.metrics.academics += academics_gain
        self.metrics.sHappiness += student_hap_gain
        self.metrics.aHappiness += admin_hap_gain
        self.metrics.security += security_gain

    # Contains the current metrics for the game for a specific user 
    def _metrics_snapshot(self):
        return {
            "budget": self.metrics.budget,
            "prestige": self.metrics.prestige,
            "sHappiness": self.metrics.sHappiness,
            "aHappiness": self.metrics.aHappiness,
            "security": self.metrics.security,
            "academics": self.metrics.academics
        }


# This class generates the loading screen. It must prompt user to select a file off of desktop and load
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
    
    # Loads an existing game 
    def load_game(self):
        from .db import load_full_state
        print("LOAD GAME CLICKED")

        player_id = self.gameStateManager.player_id
        state = load_full_state(player_id)

        if not state:
            return

        # Restore semester
        self.start.semester = state["semester"]

        # Restore metrics
        m = state["metrics"]
        self.start.metrics.budget = m["budget"]
        self.start.metrics.prestige = m["prestige"]
        self.start.metrics.sHappiness = m["student_happiness"]
        self.start.metrics.aHappiness = m["admin_happiness"]
        self.start.metrics.security = m["security"]
        self.start.metrics.academics = m["academics"]
        self.start.year_start_metrics = self.start._metrics_snapshot()

        # Restore buildings
        self.start.menu_manager.set_building_levels(state["buildings"])

        # Restore tasks
        self.start.recreate_task_buttons([
            {"name": name, "is_active": True, "already_completed": False}
            for name in state["tasks"]
        ])

        # Switch to the game
        self.gameStateManager.set_current_state("Start Game")
        

    def run(self):
        self.screen.fill(BLACK)

        title_surface = self.title_font.render("Load a Saved Game", True, WHITE)
        title_rect = title_surface.get_rect(center = (WINDOW_WIDTH // 2, self.title_y))
        self.screen.blit(title_surface, title_rect)

        # Drawing the button on the screen
        self.load_button.draw(self.screen)
        self.back_button.draw(self.screen)

        # Event handling logic
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            self.load_button.handle_event(event)
            self.back_button.handle_event(event)

# This class is the in game menu that opens when you click the help button It includes save and close button.
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
    
    # Saves a game when user clicks "Save Game" button
    def save_game(self):
        print("SAVE GAME CLICKED")
        player_id = self.gameStateManager.player_id

        state = {
            "semester": self.start.semester,
            "metrics": {
                "budget": self.start.metrics.budget,
                "prestige": self.start.metrics.prestige,
                "student_happiness": self.start.metrics.sHappiness,
                "admin_happiness": self.start.metrics.aHappiness,
                "security": self.start.metrics.security,
                "academics": self.start.metrics.academics
            },
            "buildings": self.start.menu_manager.get_building_levels(),
            "tasks": [btn.text for btn in self.start.tasks]
        }

        from .db import save_full_state
        save_full_state(player_id, state)
        print("Game saved to database for player", player_id)
       
    
    def get_save_path(self):
        return os.path.join(os.path.expanduser("~"), "Desktop", "save_game.json")

    def run(self):
        # Draw overlay
        self.screen.fill(BLACK)

        title_surface = self.title_font.render("Menu", True, WHITE)
        title_rect = title_surface.get_rect(center = (WINDOW_WIDTH // 2, self.title_y))
        self.screen.blit(title_surface, title_rect)

        # Draw buttons
        self.save_button.draw(self.screen)
        self.close_button.draw(self.screen)

        # Event handling logic
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            self.save_button.handle_event(event)
            self.close_button.handle_event(event)
        return 

# This class manages state switching logic
class GameStateManager:
    def __init__(self, current_state):
        self.current_state = current_state
        self.player_username = None
        self.player_id = None

    def get_current_state(self):
        return self.current_state
    
    def set_current_state(self, new_state):
        self.current_state = new_state

# Main execution block
if __name__ == '__main__':
    game = Game()
    game.run()
