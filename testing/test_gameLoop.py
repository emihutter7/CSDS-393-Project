import json
import os
from types import SimpleNamespace

import pytest
import pygame as py

import scripts.GameLoop as gl
from scripts.Popups import PopupEvent, PopupChoice


@pytest.fixture(autouse=True)
def init_pygame():
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    py.init()
    yield
    py.quit()


@pytest.fixture
def start_game(monkeypatch):
    # deterministic task selection so tests do not depend on randomness
    monkeypatch.setattr(gl.random, "sample", lambda population, k: list(population[:k]))
    screen = py.Surface((gl.WINDOW_WIDTH, gl.WINDOW_HEIGHT))
    font = py.font.Font(None, 24)
    manager = gl.GameStateManager("Start Game")
    return gl.StartGame(screen, font, manager)


def test_game_run_proc(monkeypatch):
    events = [py.event.Event(py.USEREVENT, {})]
    monkeypatch.setattr(py.event, "get", lambda: events)

    # stop the infinite loop after a single frame
    def stop_after_one():
        raise SystemExit

    monkeypatch.setattr(py.display, "update", stop_after_one)

    game = gl.Game()
    with pytest.raises(SystemExit):
        game.run()


def test_building_opens(start_game):
    start_game.show_building_menu("Nord")
    assert start_game.menu_manager.active_menu is not None
    assert start_game.menu_manager.active_menu.title == "Nord Menu"


def test_update_directions(start_game):
    start_game.check_input(py.K_LEFT, True)
    start_game.check_input(py.K_RIGHT, True)
    start_game.check_input(py.K_UP, True)
    start_game.check_input(py.K_DOWN, True)

    assert start_game.player_input == {
        "left": True,
        "right": True,
        "up": True,
        "down": True,
        "select": False,
    }


def test__start_handle_event(monkeypatch, start_game):
    events = [
        py.event.Event(py.KEYDOWN, {"key": py.K_LEFT}),
        py.event.Event(py.KEYUP, {"key": py.K_LEFT}),
        py.event.Event(py.MOUSEMOTION, {"pos": (30, 160)}),
    ]
    monkeypatch.setattr(py.event, "get", lambda: events)

    # ensure popup handling branch runs
    choice_tracker = []

    class DummyChoice:
        def handle_event(self, event):
            choice_tracker.append(event.type)

    start_game.active_popup = PopupEvent("Popup", "desc", "minor", [])
    start_game.choice_buttons = [DummyChoice()]

    start_game.run()
    assert not start_game.player_input["left"]
    assert choice_tracker


def test_start_quit_event(monkeypatch, start_game):
    events = [py.event.Event(py.QUIT, {})]
    monkeypatch.setattr(py.event, "get", lambda: events)
    monkeypatch.setattr(py, "quit", lambda: None)

    exit_called = []

    def fake_exit():
        exit_called.append(True)
        raise SystemExit

    monkeypatch.setattr(gl.sys, "exit", fake_exit)

    with pytest.raises(SystemExit):
        start_game.run()
    assert exit_called


def test_generate_tasks(start_game):
    start_game.semester = 2
    start_game.tasks = []
    start_game.generate_tasks()
    assert len(start_game.tasks) == 2  # one minor + one major event


def test_popup(start_game):
    event = PopupEvent(
        "Test Popup",
        "desc",
        "minor",
        [PopupChoice("Resolve", {"budget": 0})],
    )

    start_game.tasks = [SimpleNamespace(text=event.title)]
    start_game.open_popup(event)
    start_game.draw_popup()
    start_game.choose_option(0)

    assert start_game.active_popup is None
    assert not start_game.tasks


def test_load_handle_event(monkeypatch):
    screen = py.Surface((gl.WINDOW_WIDTH, gl.WINDOW_HEIGHT))
    font = py.font.Font(None, 24)
    start = SimpleNamespace(player="value")
    gsm = gl.GameStateManager("Load Game")
    loader = gl.LoadGame(screen, font, start, gsm)

    loader.load_game()
    assert start.player is None

    events = [py.event.Event(py.USEREVENT, {})]
    monkeypatch.setattr(py.event, "get", lambda: events)
    loader.run()


def test_load_quit(monkeypatch):
    screen = py.Surface((gl.WINDOW_WIDTH, gl.WINDOW_HEIGHT))
    font = py.font.Font(None, 24)
    start = SimpleNamespace(player="value")
    gsm = gl.GameStateManager("Load Game")
    loader = gl.LoadGame(screen, font, start, gsm)

    events = [py.event.Event(py.QUIT, {})]
    monkeypatch.setattr(py.event, "get", lambda: events)
    monkeypatch.setattr(py, "quit", lambda: None)

    def fake_exit():
        raise SystemExit

    monkeypatch.setattr(gl.sys, "exit", fake_exit)
    with pytest.raises(SystemExit):
        loader.run()


def test_save_game_json(monkeypatch, tmp_path):
    start = SimpleNamespace(
        player_x=1,
        player_y=2,
        player_velocity=[0, 0],
        tasks=["Task"],
        budget=100,
        admins=[object()],
        students=[object(), object()],
    )
    screen = py.Surface((gl.WINDOW_WIDTH, gl.WINDOW_HEIGHT))
    font = py.font.Font(None, 24)
    menu = gl.InGameMenu(screen, font, start, gl.GameStateManager("Start Game"))

    # bypass invalid getattr usage inside save_game
    monkeypatch.setattr(gl, "getattr", lambda value: value, raising=False)
    monkeypatch.setattr(gl.os.path, "expanduser", lambda _: str(tmp_path))
    monkeypatch.setattr(
        gl.os.path,
        "join",
        lambda *parts: str(tmp_path / "save_game.json"),
    )

    menu.save_game()
    saved = json.loads((tmp_path / "save_game.json").read_text())
    assert saved["player"]["x"] == 1
    assert saved["students"] == 2


def test_in_game_handle_event(monkeypatch):
    start = SimpleNamespace(
        player_x=0,
        player_y=0,
        player_velocity=[0, 0],
        tasks=[],
        budget=0,
        admins=[],
        students=[],
    )
    screen = py.Surface((gl.WINDOW_WIDTH, gl.WINDOW_HEIGHT))
    font = py.font.Font(None, 24)
    menu = gl.InGameMenu(screen, font, start, gl.GameStateManager("Start Game"))

    events = [py.event.Event(py.USEREVENT, {})]
    monkeypatch.setattr(py.event, "get", lambda: events)
    menu.run()


def test_in_game_quit(monkeypatch):
    start = SimpleNamespace(
        player_x=0,
        player_y=0,
        player_velocity=[0, 0],
        tasks=[],
        budget=0,
        admins=[],
        students=[],
    )
    screen = py.Surface((gl.WINDOW_WIDTH, gl.WINDOW_HEIGHT))
    font = py.font.Font(None, 24)
    menu = gl.InGameMenu(screen, font, start, gl.GameStateManager("Start Game"))

    events = [py.event.Event(py.QUIT, {})]
    monkeypatch.setattr(py.event, "get", lambda: events)
    monkeypatch.setattr(py, "quit", lambda: None)
    monkeypatch.setattr(gl.sys, "exit", lambda: (_ for _ in ()).throw(SystemExit))

    with pytest.raises(SystemExit):
        menu.run()


def test_module_main(monkeypatch):
    created = []

    class FakeGame:
        def __init__(self):
            created.append(True)

        def run(self):
            raise SystemExit

    monkeypatch.setattr(gl, "Game", FakeGame)
    filler = "\n" * 665 + "game = Game()\ngame.run()\n"
    code = compile(filler, gl.__file__, "exec")

    with pytest.raises(SystemExit):
        exec(code, gl.__dict__)

    assert created
