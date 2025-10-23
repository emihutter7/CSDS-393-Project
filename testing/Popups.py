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


# test spefic event (Snowstorm Hits Campus)
def test_snowstorm_event_choice_one(m):

    event = minor_events[0]

    start_budget = m.budget
    start_shappy = m.sHappiness
    start_ahappy = m.aHappiness
    start_security = m.security

    # trigger first choice
    event.trigger_choice(0, m)

    # Verify that metrics changed exactly as expected
    assert m.budget == start_budget - 2000000
    assert m.sHappiness == start_shappy + 10
    assert m.aHappiness == start_shappy + 10
    assert m.security == start_security + 5