import pytest
import pygame
from unittest import mock
from scripts.agentsClass import Agent, Student, Admin, Player

@pytest.fixture(autouse=True)
def init_pygame():
    pygame.init()
    yield
    pygame.quit()

def test_agent_move():
    agent = Agent(x=0, y=0, color=(255,0,0), speed=5, path_end=(10,0))
    start_direction = agent.direction

    # move forward until it hits the end
    for _ in range(3):
        agent.move_along_path()
    assert agent.x == 10  # reached end
    assert agent.direction == -start_direction  # reversed direction

    # now move back
    for _ in range(3):
        agent.move_along_path()
    assert agent.direction == start_direction  # reversed again

def test_student_draw_polygon(mocker):
    mock_polygon = mocker.patch("pygame.draw.polygon")
    s = Student(x=50, y=50, color=(0,255,0), speed=1, path_end=(100,50))
    mock_window = mock.MagicMock()

    s.draw(mock_window)

    mock_polygon.assert_called_once()
    args, kwargs = mock_polygon.call_args
    assert args[1] == (0, 255, 0)  # color
    assert isinstance(args[2], list)  # points list

def test_admin_draw_circle(mocker):
    mock_circle = mocker.patch("pygame.draw.circle")
    a = Admin(x=100, y=200, color=(0,0,0), speed=1, path_end=(150,200))
    mock_window = mock.MagicMock()

    a.draw(mock_window)

    mock_circle.assert_called_once()
    args, kwargs = mock_circle.call_args
    assert args[1] == (0, 0, 0)

def test_player_draw_rect(mocker):
    mock_rect = mocker.patch("pygame.draw.rect")
    p = Player(x=10, y=20, color=(0,0,255))
    mock_window = mock.MagicMock()

    p.draw(mock_window)

    mock_rect.assert_called_once()
    args, kwargs = mock_rect.call_args
    assert args[1] == (0, 0, 255)
    rect_args = args[2]
    assert isinstance(rect_args, tuple)
    assert len(rect_args) == 4  # x, y, width, height

