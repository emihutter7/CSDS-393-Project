import pytest
from scripts.MetricsClass import Metrics
from scripts.Popups import PopupEvent, PopupChoice, minor_events, major_events, AdjustMetricsTask

@pytest.fixture
def m():
    return Metrics()

# test AdjustMetricsTask
def test_adjust_metrics_task_adds_correctly(m):
    task = AdjustMetricsTask(budget=-2_000_000, sHappiness=+5, security=+3)
    starting_budget = m.budget
    starting_shappy = m.sHappiness
    starting_security = m.security

    task.run(m)

    assert m.budget == starting_budget - 2_000_000
    assert m.sHappiness == starting_shappy + 5
    assert m.security == starting_security + 3


# PopupEvent and PopupChoice init test
def test_popupchoice_and_event_creation():
    choice1 = PopupChoice("Do something", {"budget": -100000})
    event = PopupEvent("Test Event", "Description", "minor", [choice1])

    assert event.title == "Test Event"
    assert event.description == "Description"
    assert event.event_type == "minor"
    assert len(event.choices) == 1
    assert event.choices[0].text == "Do something"


# test trigger_choice actually applies changes
def test_trigger_choice_applies_effects(m):
    choice1 = PopupChoice("Test choice", {"budget": -1_000_000, "sHappiness": +3})
    event = PopupEvent("Test Event", "Demo event", "minor", [choice1])

    start_budget = m.budget
    start_shappy = m.sHappiness

    event.trigger_choice(0, m)

    assert m.budget == start_budget - 1000000
    assert m.sHappiness == start_shappy + 3


# test snowstorm choice one
def test_snowstorm_choice_one(m):
    event = minor_events[0]
    start_budget = m.budget
    start_shappy = m.sHappiness
    start_ahappy = m.aHappiness
    start_security = m.security

    event.trigger_choice(0, m)
    assert m.budget == start_budget - 2_000_000
    assert m.sHappiness == start_shappy + 10
    assert m.aHappiness == start_ahappy + 10
    assert m.security == start_security + 5

# test snowstorm choice three
def test_snowstorm_choice_three(m):
    event = minor_events[0]
    start_budget = m.budget
    start_shappy = m.sHappiness
    start_security = m.security

    event.trigger_choice(2, m)
    assert m.budget == start_budget + 1_000_000
    assert m.sHappiness == start_shappy - 6
    assert m.security == start_security - 5

# test dining choice one
def test_dining_choice_one(m):
    event = minor_events[1]
    start_budget = m.budget
    start_shappy = m.sHappiness
    start_prestige = m.prestige

    event.trigger_choice(0, m)
    assert m.budget == start_budget - 3_000_000
    assert m.sHappiness == start_shappy + 10
    assert m.prestige == start_prestige + 5

# test dining choice three
def test_dining_choice_three(m):
    event = minor_events[1]
    start_shappy = m.sHappiness
    start_prestige = m.prestige

    event.trigger_choice(2, m)
    assert m.sHappiness == start_shappy - 10
    assert m.prestige == start_prestige - 5

# test faculty choice one
def test_faculty_choice_one(m):
    event = minor_events[2]
    start_budget = m.budget
    start_academics = m.academics
    start_ahappy = m.aHappiness
    start_prestige = m.prestige

    event.trigger_choice(0, m)
    assert m.budget == start_budget - 4_000_000
    assert m.academics == start_academics + 10
    assert m.aHappiness == start_ahappy + 10
    assert m.prestige == start_prestige + 10

# test faculty choice three
def test_faculty_choice_three(m):
    event = minor_events[2]
    start_academics = m.academics
    start_ahappy = m.aHappiness
    start_prestige = m.prestige

    event.trigger_choice(2, m)
    assert m.aHappiness == start_ahappy - 10
    assert m.academics == start_academics - 10
    assert m.prestige == start_prestige - 10

# test dorm choice one
def test_dorm_choice_one(m):
    event = minor_events[3]
    start_budget = m.budget
    start_shappy = m.sHappiness

    event.trigger_choice(0, m)
    assert m.budget == start_budget - 2_000_000
    assert m.sHappiness == start_shappy + 10

# test dorm choice three
def test_dorm_choice_three(m):
    event = minor_events[3]
    start_budget = m.budget
    start_shappy = m.sHappiness

    event.trigger_choice(2, m)
    assert m.budget == start_budget + 2_000_000
    assert m.sHappiness == start_shappy - 10

# test board choice one
def test_board_choice_one(m):
    event = major_events[0]
    start_budget = m.budget
    start_prestige = m.prestige
    start_academics = m.academics
    start_shappy = m.sHappiness
    start_ahappy = m.aHappiness

    event.trigger_choice(0, m)
    assert m.budget == start_budget - 1_000_000
    assert m.prestige == start_prestige + 10
    assert m.academics == start_academics + 10
    assert m.sHappiness == start_shappy + 10
    assert m.aHappiness == start_ahappy + 5

# test board choice two
def test_board_choice_two(m):
    event = major_events[0]
    start_budget = m.budget
    start_shappy = m.sHappiness
    start_ahappy = m.aHappiness

    event.trigger_choice(1, m)
    assert m.budget == start_budget + 5_000_000
    assert m.sHappiness == start_shappy - 5
    assert m.aHappiness == start_ahappy - 5

# test safety choice one
def test_safety_choice_one(m):
    event = major_events[1]
    start_budget = m.budget
    start_security = m.security
    start_prestige = m.prestige
    start_shappy = m.sHappiness

    event.trigger_choice(0, m)
    assert m.budget == start_budget - 4_000_000
    assert m.security == start_security + 10
    assert m.prestige == start_prestige + 5
    assert m.sHappiness == start_shappy + 5

# test safety choice two
def test_safety_choice_three(m):
    event = major_events[1]
    start_security = m.security
    start_prestige = m.prestige
    start_shappy = m.sHappiness

    event.trigger_choice(2, m)
    assert m.security == start_security - 5
    assert m.prestige == start_prestige - 5
    assert m.sHappiness == start_shappy - 5
