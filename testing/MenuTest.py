import pytest
import pygame
from scripts.menu import Menu, MenuManager
from scripts.Button import Button

# fixture to test each case in the mock pygame environment
@pytest.fixture(autouse=True)
def init_pygame():
    pygame.init()
    yield
    pygame.quit()

# test to make sure the button creation works for inside the menu panel
def test_menu_button_creation(mocker):

    mock_callback = mocker.MagicMock()
    mock_manager = mocker.MagicMock()

    user_options = [("Option1", mock_callback), ("Option2", mock_callback)]
    menu = Menu(menu_manager=mock_manager, title="Title", text="Some text", user_options=user_options)

    assert len(menu.buttons) == 2
    for button in menu.buttons:
        assert isinstance(button, Button)

# test that the menu properly delegates the event handling
def test_menu_event_handle(mocker):

    mock_callback = mocker.MagicMock()
    mock_manager = mocker.MagicMock()
    user_options = [("Test", mock_callback)]
    menu = Menu(menu_manager=mock_manager, title="Title", text="Test text", user_options=user_options)

    mock_button = mocker.MagicMock(spec=Button)
    menu.buttons = [mock_button]

    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (0, 0)})
    menu.handle_event(event)

    mock_button.handle_event.assert_called_once_with(event)

# make sure that the main menu creates buttons correctly
def test_manager_button_creation(mocker):

    mock_callback = mocker.MagicMock()
    data = [("Play", mock_callback), ("Exit", mock_callback)]
    manager = MenuManager(main_data=data)

    assert len(manager.main_buttons) == 2
    for b in manager.main_buttons:
        assert isinstance(b, Button)

# test to make sure menus open and close correctly
def test_open_and_close():

    manager = MenuManager(main_data=[])
    menu = "dummy"
    manager.open_menu(menu)
    assert manager.active_menu == menu

    manager.close_menu()
    assert manager.active_menu is None

# make sure text wraps correctly in the menu
def test_menu_wrap_text(mocker):

    mock_surface = mocker.MagicMock()
    mocker.patch("pygame.font.Font", return_value=mocker.MagicMock(size=lambda text: (len(text)*10, 20), render=mocker.MagicMock()))
    
    menu = Menu(menu_manager=mocker.MagicMock(), title="Title",
                text="This is a very long text that should wrap correctly",
                user_options=[])
    menu._wrap_text(mock_surface, menu.text, menu.text_font, x=0, y=0, max_width=50)

# test to make sure explicit button positions and sizes are able to be declared
def test_button_positions():

    callback = lambda: None # dummy
    data = [("Btn", callback, (10, 20, 100, 50))]
    manager = MenuManager(main_data=data)

    btn = manager.main_buttons[0]
    assert btn.rect.x == 10
    assert btn.rect.y == 20
    assert btn.rect.width == 100
    assert btn.rect.height == 50

# test that when a menu is active, the main screen is not clickable until the menu is addressed
def test_active_menu(mocker):

    manager = MenuManager(main_data=[("Btn", lambda: None)])
    active_menu = mocker.MagicMock()
    manager.open_menu(active_menu)

    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button":1, "pos": (0,0)})
    manager.handle_event(event)
    active_menu.handle_event.assert_called_once_with(event)