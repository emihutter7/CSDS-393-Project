import pytest
from scripts.GameLoop import Game, GameStateManager, StartGame, MainGameMenu, InGameMenu

# mock objects because we need to run in a headless env
class MockSurface:
    def fill(self, *args, **kwargs):
        pass
    def blit(self, *args, **kwargs):
        pass
    def get_rect(self, *args, **kwargs):
        pass

class MockFont:
    def render(self, *args, **kwargs):
        return MockSurface()
    def get_linesize(self):
        return 10

class MockClock:
    def tick(self, fps):
        pass

# create the mock env
@pytest.fixture(autouse=True)
def mock_pygame(monkeypatch):
    import pygame
    monkeypatch.setattr(pygame, "init", lambda: None)
    monkeypatch.setattr(pygame, "font", type("FontModule", (), {"Font": lambda *a, **k: MockFont(), "SysFont": lambda *a, **k: MockFont()})())
    monkeypatch.setattr(pygame, "display", type("DisplayModule", (), {"set_mode": lambda *a, **k: MockSurface(), "update": lambda: None})())
    monkeypatch.setattr(pygame, "Surface", lambda *a, **k: MockSurface())
    monkeypatch.setattr(pygame, "draw", type("DrawModule", (), {"rect": lambda *a, **k: None})())
    monkeypatch.setattr(pygame, "event", type("EventModule", (), {"get": lambda: []})())
    monkeypatch.setattr(pygame, "QUIT", "QUIT")
    monkeypatch.setattr(pygame, "KEYDOWN", "KEYDOWN")
    monkeypatch.setattr(pygame, "KEYUP", "KEYUP")
    monkeypatch.setattr(pygame, "K_LEFT", "K_LEFT")
    monkeypatch.setattr(pygame, "K_RIGHT", "K_RIGHT")
    monkeypatch.setattr(pygame, "K_UP", "K_UP")
    monkeypatch.setattr(pygame, "K_DOWN", "K_DOWN")
    monkeypatch.setattr(pygame, "RESIZABLE", 0)

# make sure game states change as expected
def test_game_state_changes():
    game = Game()
    
    # initial state should be Main Menu
    assert game.gameStateManager.get_current_state() == "Main Menu"

    game.gameStateManager.set_current_state("Start Game")
    assert game.gameStateManager.get_current_state() == "Start Game"

    game.gameStateManager.set_current_state("In-Game Menu")
    assert game.gameStateManager.get_current_state() == "In-Game Menu"

    game.gameStateManager.set_current_state("Main Menu")
    assert game.gameStateManager.get_current_state() == "Main Menu"

# make sure callbacks trigger the right state changes
def test_trigger_state_change():
    game = Game()
    
    main_menu = game.states["Main Menu"]
    start_game = game.states["Start Game"]
    in_game = game.states["In-Game Menu"]
    
    main_menu.load_button.callback()
    assert game.gameStateManager.get_current_state() == "Load Game"
    
    main_menu.start_button.callback()
    assert game.gameStateManager.get_current_state() == "Start Game"

    start_game.help_button.callback()
    assert game.gameStateManager.get_current_state() == "In-Game Menu"

    in_game.close_button.callback()
    assert game.gameStateManager.get_current_state() == "Start Game"

# test whether the game is saving
def test_in_game_save():
    game = Game()
    in_game = game.states["In-Game Menu"]
    start_game = game.states["Start Game"]

    # some dummy values
    start_game.player_x = 10
    start_game.player_y = 20
    start_game.player_velocity = [1, 2]
    start_game.tasks = ["Task1"]
    start_game.budget = 5000
    start_game.admins = ["admin1", "admin2"]
    start_game.students = ["student1", "student2", "student3"]

    # save game (should not raise)
    in_game.save_game()

# test next semester updating
def test_next_sem():
    start_game = StartGame(screen=None, font=MockFont(), gameStateManager=GameStateManager("Start Game"))
    
    initial_sem = start_game.semester
    start_game.tasks = []  # no pending tasks
    start_game.next_sem()
    assert start_game.semester == initial_sem + 1

    start_game.semester = 8
    start_game.next_sem()
    # semester should not be more than 8
    assert start_game.semester == 8

# test that main menu works correctly
def test_main_game_menu():
    gsm = GameStateManager("Main Menu")
    screen = None  # pygame is mocked
    font = None
    main_menu = MainGameMenu(screen, font, gsm)

    main_menu.load_button.callback()
    assert gsm.get_current_state() == "Load Game"

    # reset state
    gsm.set_current_state("Main Menu")

    # click start state
    main_menu.start_button.callback()
    assert gsm.get_current_state() == "Start Game"

# test the in-game menu buttons
def test_in_game_menu():
    gsm = GameStateManager("Start Game")
    screen = None
    font = None
    start_game = StartGame(screen, font, gsm)
    in_game_menu = InGameMenu(screen, font, start_game, gsm)

    # save game button should run without error
    start_game.player_x = 100
    start_game.player_y = 200
    start_game.player_velocity = [1, 1]
    start_game.tasks = []
    start_game.budget = 5000
    start_game.admins = ["admin1"]
    start_game.students = ["student1", "student2"]

    in_game_menu.save_button.callback()  # runs save_game()
    
    # close button should return to Start Game state
    gsm.set_current_state("In-Game Menu")
    in_game_menu.close_button.callback()
    assert gsm.get_current_state() == "Start Game"