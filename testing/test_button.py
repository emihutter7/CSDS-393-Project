import pytest
import pygame
from scripts.Button import Button

# fixture to create a mock pygame environment for each test
@pytest.fixture(autouse=True)
def init_pygame():
    pygame.init()
    yield
    pygame.quit()

# test if button draw method works correctly
def test_button_draw(mocker):

    # mock pygame.draw.rect
    mock_draw_rect = mocker.patch("pygame.draw.rect")

    # mock font constructor
    mock_font_instance = mocker.MagicMock()
    mock_font_instance.render = mocker.MagicMock()
    mocker.patch("pygame.font.Font", return_value=mock_font_instance)

    mock_surface = mocker.MagicMock()
    button = Button(dimensions=(0, 0, 100, 50), text="Click", callback=lambda: None)

    # run draw
    button.draw(mock_surface)

    # verify that rectangle is drawn correctly
    assert mock_draw_rect.call_count >= 2
    mock_font_instance.render.assert_called_once()
    mock_surface.blit.assert_called_once()

# test button's event handler for clicking
def test_button_handle_event(mocker):

    mock_callback = mocker.MagicMock()
    button = Button(dimensions=(0, 0, 100, 50), text="Click", callback=mock_callback)

    # simulate mouse click inside button
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (50, 25)})
    result = button.handle_event(event)

    mock_callback.assert_called_once()
    assert result == mock_callback.return_value

# test button's hover detection when mouse is on or not on the button
def test_button_hover_state():

    button = Button(dimensions=(0, 0, 100, 50), text="Hover", callback=lambda: None)

    # mouse over button
    event_in = pygame.event.Event(pygame.MOUSEMOTION, {"pos": (50, 25)})
    button.handle_event(event_in)
    assert button.is_hovered is True

    # mouse outside button
    event_out = pygame.event.Event(pygame.MOUSEMOTION, {"pos": (200, 200)})
    button.handle_event(event_out)
    assert button.is_hovered is False

# test outside click to make sure the button does not activate
def test_outside_click():

    called = False
    def cb(): nonlocal called; called = True
    button = Button((0, 0, 50, 50), "Click", cb)

    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (100, 100)})
    button.handle_event(event)
    assert not called

# test to make sure just a right click does not trigger the button
def test_right_click():

    called = False
    def cb(): nonlocal called; called = True
    button = Button((0, 0, 50, 50), "Click", cb)

    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 3, "pos": (25, 25)})
    button.handle_event(event)
    assert not called