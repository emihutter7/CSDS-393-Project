""" import os
import pytest
import pygame as py
import scripts.game as game


# ------------------------------------------------------
#  Automatic pygame initialization for all tests
# ------------------------------------------------------
@pytest.fixture(autouse=True)
def init_pygame():
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    py.init()
    yield
    py.quit()


# ------------------------------------------------------
#  Test check_input correctly updates player_input
# ------------------------------------------------------
def test_check_input_updates_dict():
    original = game.player_input.copy()

    game.check_input(py.K_LEFT, True)
    assert game.player_input["left"] is True

    game.check_input(py.K_LEFT, False)
    assert game.player_input["left"] is False

    # restore
    game.player_input.update(original)


# ------------------------------------------------------
#  Test check_selection() selecting from button_list
# ------------------------------------------------------
def test_check_selection(monkeypatch):
    # Create fake buttons
    btn1 = py.Rect(10, 10, 50, 50)
    btn2 = py.Rect(100, 100, 50, 50)

    game.button_list[:] = [btn1, btn2]

    # Monkeypatch the print to avoid actual console output
    clicked = []
    monkeypatch.setattr("builtins.print", lambda msg: clicked.append(msg))

    game.check_selection((20, 20))     # hits btn1
    assert "Clicked" in clicked[0]


# ------------------------------------------------------
#  Agent movement reverses direction at endpoints
# ------------------------------------------------------
def test_agent_reverse_direction():
    agent = game.Agent(x=0, y=0, color=(0, 0, 0), speed=5, path_end=(10, 0))

    # Move forward until reversal
    for _ in range(3):
        agent.move_along_path()
    assert agent.direction == -1  # reversed

    # Now move backward until reversal
    for _ in range(3):
        agent.move_along_path()
    assert agent.direction == 1  # reversed again


# ------------------------------------------------------
#  Student.draw and Admin.draw should call pygame draw functions
# ------------------------------------------------------
def test_student_draw(monkeypatch):
    calls = []
    monkeypatch.setattr(py.draw, "polygon", lambda *args, **kwargs: calls.append(args))

    stu = game.Student(50, 50, (0, 255, 0), speed=1, path_end=(100, 50))
    surf = py.Surface((200, 200))

    stu.draw(surf)
    assert calls  # polygon was called


def test_admin_draw(monkeypatch):
    calls = []
    monkeypatch.setattr(py.draw, "circle", lambda *args, **kwargs: calls.append(args))

    adm = game.Admin(50, 50, (0, 0, 0), speed=1, path_end=(100, 50))
    surf = py.Surface((200, 200))

    adm.draw(surf)
    assert calls  # circle was called


# ------------------------------------------------------
#  Player.draw should call pygame.draw.rect
# ------------------------------------------------------
def test_player_draw(monkeypatch):
    calls = []
    monkeypatch.setattr(py.draw, "rect", lambda *args, **kwargs: calls.append(args))

    p = game.Player(10, 20)
    surf = py.Surface((100, 100))

    p.draw(surf)
    assert calls


# ------------------------------------------------------
#  Test that main loop exits properly when QUIT event appears
# ------------------------------------------------------
def test_main_exits_on_quit(monkeypatch):
    # Monkeypatch event.get() to return QUIT immediately
    monkeypatch.setattr(py.event, "get", lambda: [py.event.Event(py.QUIT, {})])

    # Prevent pygame.quit() and sys.exit() from killing pytest
    monkeypatch.setattr(py, "quit", lambda: None)
    monkeypatch.setattr(game.sys, "exit", lambda: (_ for _ in ()).throw(SystemExit))

    # main() should raise SystemExit immediately
    with pytest.raises(SystemExit):
        game.main()
 """