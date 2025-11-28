import pytest
from scripts.db import db_init, get_connection, save_metrics, load_metrics, save_buildings, load_buildings, save_popups, load_popups

@pytest.fixture(autouse=True)
def setup_db():
    # Initialize database before each test
    db_init()
    yield
    # Optional: clean up database after each test
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM metrics")
    cur.execute("DELETE FROM buildings")
    cur.execute("DELETE FROM popups")
    conn.commit()
    cur.close()
    conn.close()

def test_metrics_save_load():
    save_metrics(100, "Summer")
    score, season = load_metrics()
    assert score == 100
    assert season == "Summer"

def test_buildings_save_load():
    buildings = {"Farm": 1, "Barracks": 3}
    save_buildings(buildings)
    loaded = load_buildings()
    assert loaded == buildings

def test_popups_save_load():
    popups = [
        {"name": "Tutorial", "is_active": True, "already_completed": False},
        {"name": "Bonus", "is_active": False, "already_completed": True}
    ]
    save_popups(popups)
    loaded = load_popups()
    assert len(loaded) == 2
    
    # Check that all fields match
    for p in popups:
        match = next((l for l in loaded if l["name"] == p["name"]), None)
        assert match is not None
        assert match["is_active"] == p["is_active"]
        assert match["already_completed"] == p["already_completed"]
