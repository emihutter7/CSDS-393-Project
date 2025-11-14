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

# test dining hall choice one
def test_dining_hall_choice_one(m):
    event = minor_events[1]
    start_budget = m.budget
    start_shappy = m.sHappiness
    start_prestige = m.prestige

    event.trigger_choice(0, m)
    assert m.budget == start_budget - 3_000_000
    assert m.sHappiness == start_shappy + 10
    assert m.prestige == start_prestige + 5

# test faculty research choice one
def test_faculty_research_choice_one(m):
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

# test dorm overcrowding choice one
def test_dorm_overcrowding_choice_one(m):
    event = minor_events[3]
    start_budget = m.budget
    start_shappy = m.sHappiness

    event.trigger_choice(0, m)
    assert m.budget == start_budget - 2_000_000
    assert m.sHappiness == start_shappy + 10

# test power outage choice one
def test_power_outage_choice_one(m):
    event = minor_events[4]
    start_budget = m.budget
    start_academics = m.academics
    start_ahappy = m.aHappiness

    event.trigger_choice(0, m)
    assert m.budget == start_budget - 2_500_000
    assert m.academics == start_academics + 10
    assert m.aHappiness == start_ahappy + 5

# test festival choice one
def test_festival_choice_one(m):
    event = minor_events[5]
    start_budget = m.budget
    start_shappy = m.sHappiness
    start_prestige = m.prestige

    event.trigger_choice(0, m)
    assert m.budget == start_budget - 1_500_000
    assert m.sHappiness == start_shappy + 15
    assert m.prestige == start_prestige + 5

# test network glitch choice one
def test_network_glitch_choice_one(m):
    event = minor_events[6]
    start_budget = m.budget
    start_academics = m.academics
    start_ahappy = m.aHappiness

    event.trigger_choice(0, m)
    assert m.budget == start_budget - 2_000_000
    assert m.academics == start_academics + 10
    assert m.aHappiness == start_ahappy + 5

# test parking shortage choice one
def test_parking_shortage_choice_one(m):
    event = minor_events[7]
    start_budget = m.budget
    start_shappy = m.sHappiness
    start_ahappy = m.aHappiness

    event.trigger_choice(0, m)
    assert m.budget == start_budget - 3_000_000
    assert m.sHappiness == start_shappy + 10
    assert m.aHappiness == start_ahappy + 10

# test library hours choice one
def test_library_hours_choice_one(m):
    event = minor_events[8]
    start_budget = m.budget
    start_academics = m.academics
    start_shappy = m.sHappiness

    event.trigger_choice(0, m)
    assert m.budget == start_budget - 1_000_000
    assert m.academics == start_academics + 10
    assert m.sHappiness == start_shappy + 5

# test broken gym choice one
def test_broken_gym_choice_one(m):
    event = minor_events[9]
    start_budget = m.budget
    start_shappy = m.sHappiness

    event.trigger_choice(0, m)
    assert m.budget == start_budget - 1_500_000
    assert m.sHappiness == start_shappy + 10

# test cafeteria complaints choice one
def test_cafeteria_complaints_choice_one(m):
    event = minor_events[10]
    start_budget = m.budget
    start_shappy = m.sHappiness

    event.trigger_choice(0, m)
    assert m.budget == start_budget - 1_000_000
    assert m.sHappiness == start_shappy + 15

# test drone usage choice one
def test_drone_usage_choice_one(m):
    event = minor_events[11]
    start_security = m.security
    start_shappy = m.sHappiness

    event.trigger_choice(0, m)
    assert m.security == start_security + 10
    assert m.sHappiness == start_shappy - 5

# test data breach choice one
def test_data_breach_choice_one(m):
    event = minor_events[12]
    start_budget = m.budget
    start_security = m.security
    start_prestige = m.prestige

    event.trigger_choice(0, m)
    assert m.budget == start_budget - 1_500_000
    assert m.security == start_security + 10
    assert m.prestige == start_prestige + 5

# test student protest choice one
def test_student_protest_choice_one(m):
    event = minor_events[13]
    start_budget = m.budget
    start_shappy = m.sHappiness
    start_prestige = m.prestige

    event.trigger_choice(0, m)
    assert m.budget == start_budget - 1_000_000
    assert m.sHappiness == start_shappy + 10
    assert m.prestige == start_prestige + 5

# test mural project choice one
def test_mural_project_choice_one(m):
    event = minor_events[14]
    start_budget = m.budget
    start_prestige = m.prestige
    start_shappy = m.sHappiness

    event.trigger_choice(0, m)
    assert m.budget == start_budget - 1_000_000
    assert m.prestige == start_prestige + 10
    assert m.sHappiness == start_shappy + 5

# test hvac malfunction choice one
def test_hvac_malfunction_choice_one(m):
    event = minor_events[15]
    start_budget = m.budget
    start_ahappy = m.aHappiness
    start_academics = m.academics

    event.trigger_choice(0, m)
    assert m.budget == start_budget - 3_000_000
    assert m.aHappiness == start_ahappy + 10
    assert m.academics == start_academics + 5

# test visiting scholar choice one
def test_visiting_scholar_choice_one(m):
    event = minor_events[16]
    start_budget = m.budget
    start_prestige = m.prestige
    start_academics = m.academics

    event.trigger_choice(0, m)
    assert m.budget == start_budget - 2_500_000
    assert m.prestige == start_prestige + 10
    assert m.academics == start_academics + 10

# test wifi upgrade choice one
def test_wifi_upgrade_choice_one(m):
    event = minor_events[17]
    start_budget = m.budget
    start_shappy = m.sHappiness
    start_ahappy = m.aHappiness

    event.trigger_choice(0, m)
    assert m.budget == start_budget - 2_000_000
    assert m.sHappiness == start_shappy + 10
    assert m.aHappiness == start_ahappy + 5

# test athletic success choice one
def test_athletic_success_choice_one(m):
    event = minor_events[18]
    start_budget = m.budget
    start_prestige = m.prestige
    start_shappy = m.sHappiness

    event.trigger_choice(0, m)
    assert m.budget == start_budget - 1_000_000
    assert m.prestige == start_prestige + 10
    assert m.sHappiness == start_shappy + 10

# test fire drill choice one
def test_fire_drill_choice_one(m):
    event = minor_events[19]
    start_budget = m.budget
    start_security = m.security
    start_prestige = m.prestige

    event.trigger_choice(0, m)
    assert m.budget == start_budget - 1_000_000
    assert m.security == start_security + 10
    assert m.prestige == start_prestige + 5

# test cultural exchange choice one
def test_cultural_exchange_choice_one(m):
    event = minor_events[20]
    start_budget = m.budget
    start_shappy = m.sHappiness
    start_prestige = m.prestige

    event.trigger_choice(0, m)
    assert m.budget == start_budget - 1_500_000
    assert m.sHappiness == start_shappy + 10
    assert m.prestige == start_prestige + 5

# test lost endowment choice one
def test_lost_endowment_choice_one(m):
    event = minor_events[21]
    start_budget = m.budget
    start_security = m.security

    event.trigger_choice(0, m)
    assert m.budget == start_budget - 1_000_000
    assert m.security == start_security + 10

# test new cafeteria choice one
def test_new_cafeteria_choice_one(m):
    event = minor_events[22]
    start_budget = m.budget
    start_shappy = m.sHappiness

    event.trigger_choice(0, m)
    assert m.budget == start_budget + 3_000_000
    assert m.sHappiness == start_shappy + 10

# test art exhibit choice one
def test_art_exhibit_choice_one(m):
    event = minor_events[23]
    start_prestige = m.prestige
    start_budget = m.budget

    event.trigger_choice(0, m)
    assert m.prestige == start_prestige + 10
    assert m.budget == start_budget + 2_000_000

# test dorm fire alarm choice one
def test_dorm_fire_alarm_choice_one(m):
    event = minor_events[24]
    start_budget = m.budget
    start_security = m.security
    start_shappy = m.sHappiness

    event.trigger_choice(0, m)
    assert m.budget == start_budget - 1_000_000
    assert m.security == start_security + 10
    assert m.sHappiness == start_shappy + 5

# test board meeting choice one
def test_board_meeting_choice_one(m):
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

# test campus safety review choice one
def test_campus_safety_review_choice_one(m):
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

# test donor gala choice one
def test_donor_gala_choice_one(m):
    event = major_events[2]
    start_budget = m.budget
    start_prestige = m.prestige

    event.trigger_choice(0, m)
    assert m.budget == start_budget + 2_000_000  # -6M +8M net
    assert m.prestige == start_prestige + 15

# test expansion plan choice one
def test_expansion_plan_choice_one(m):
    event = major_events[3]
    start_budget = m.budget
    start_prestige = m.prestige
    start_academics = m.academics

    event.trigger_choice(0, m)
    assert m.budget == start_budget - 15_000_000
    assert m.prestige == start_prestige + 15
    assert m.academics == start_academics + 15

# test sports scandal choice one
def test_sports_scandal_choice_one(m):
    event = major_events[4]
    start_budget = m.budget
    start_prestige = m.prestige
    start_security = m.security

    event.trigger_choice(0, m)
    assert m.budget == start_budget - 2_000_000
    assert m.prestige == start_prestige - 5
    assert m.security == start_security + 10

# test cybersecurity breach choice one
def test_cybersecurity_breach_choice_one(m):
    event = major_events[5]
    start_budget = m.budget
    start_security = m.security
    start_prestige = m.prestige

    event.trigger_choice(0, m)
    assert m.budget == start_budget - 5_000_000
    assert m.security == start_security + 15
    assert m.prestige == start_prestige + 5

# test accreditation review choice one
def test_accreditation_review_choice_one(m):
    event = major_events[6]
    start_budget = m.budget
    start_academics = m.academics
    start_prestige = m.prestige

    event.trigger_choice(0, m)
    assert m.budget == start_budget - 4_000_000
    assert m.academics == start_academics + 15
    assert m.prestige == start_prestige + 10

# test disaster damages choice one
def test_disaster_damages_choice_one(m):
    event = major_events[7]
    start_budget = m.budget
    start_security = m.security
    start_shappy = m.sHappiness

    event.trigger_choice(0, m)
    assert m.budget == start_budget - 10_000_000
    assert m.security == start_security + 10
    assert m.sHappiness == start_shappy + 10

# test presidential resignation choice one
def test_presidential_resignation_choice_one(m):
    event = major_events[8]
    start_budget = m.budget
    start_prestige = m.prestige
    start_ahappy = m.aHappiness

    event.trigger_choice(0, m)
    assert m.budget == start_budget - 3_000_000
    assert m.prestige == start_prestige + 10
    assert m.aHappiness == start_ahappy + 10

# test tech partnership choice one
def test_tech_partnership_choice_one(m):
    event = major_events[9]
    start_budget = m.budget
    start_academics = m.academics
    start_prestige = m.prestige

    event.trigger_choice(0, m)
    assert m.budget == start_budget + 8_000_000
    assert m.academics == start_academics + 10
    assert m.prestige == start_prestige + 10
