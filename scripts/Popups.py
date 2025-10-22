from MetricsClass import Metrics

# applies metric changes
class AdjustMetricsTask:

    def __init__(self, budget=450000000, prestige=51, sHappiness=75, aHappiness=60, security=50, academics=80):
        self.budget = budget
        self.prestige = prestige
        self.sHappiness = sHappiness
        self.aHappiness = aHappiness
        self.security = security
        self.academics = academics

    def run(self, m):
        m.budget += self.budget
        m.prestige += self.prestige
        m.sHappiness += self.sHappiness
        m.aHappiness += self.aHappiness
        m.security += self.security
        m.academics += self.academics


# a single choice in a popup event
class PopupChoice:

    def __init__(self, text, effects):
        self.text = text
        self.effects = effects

# popup event class
class PopupEvent:

    def __init__(self, title, description, event_type, choices):
        self.title = title
        self.description = description
        self.event_type = event_type  # minor or major event
        self.choices = choices

    # apply choice selected
    def trigger_choice(self, index, metrics):
        choice = self.choices[index]
        print("Event:", self.title)
        print("Choice selected:", choice.text)
        print("Applying effects:", choice.effects)

        # pass values to AdjustMetricsTask
        task = AdjustMetricsTask(**choice.effects)
        task.run(metrics)

        print("Metrics updated successfully.")



minor_events = [

    PopupEvent(
        "Snowstorm Hits Campus",
        "A major snowstorm is forecasted this week. Classes are at a risk of being cancelled.",
        "minor",
        [
            PopupChoice("Fund extra plowing crews", {"budget": -2000000, "sHappiness": +10, "aHappiness": +10, "security": +5}),
            PopupChoice("Maintain current funding", {"sHappiness": -5, "aHappiness": -10, +"security": -5}),
            PopupChoice("Cut maintenance budget", {"budget": +1000000, "sHappiness": -6, "security": -5})
        ]
    ),

    PopupEvent(
        "Dining Hall Maintenance Request",
        "The dining hall needs new equipment and updated ventilation.",
        "minor",
        [
            PopupChoice("Approve full renovation", {"budget": -3000000, "sHappiness": +10, "prestige": +5}),
            PopupChoice("Approve partial repairs", {"budget": -1000000, "sHappiness": +5}),
            PopupChoice("Deny request", {"sHappiness": -10, "prestige": -5})
        ]
    ),

    PopupEvent(
        "Faculty Research Proposal",
        "Professors propose a new research investment.",
        "minor",
        [
            PopupChoice("Fund research center", {"budget": -4000000, "academics": +10, "aHappiness": +10, "prestige": +10}),
            PopupChoice("Delay decision", {"aHappiness": -5, "academics": -5}),
            PopupChoice("Reject proposal", {"aHappiness": -10, "academics": -10, "prestige": -10})
        ]
    ),

    PopupEvent(
        "Dorm Overcrowding",
        "Too many admitted students has caused dorm shortages across campus.",
        "minor",
        [
            PopupChoice("Add temporary housing", {"budget": -2000000, "sHappiness": +10}),
            PopupChoice("Do nothing", {"sHappiness": -10}),
            PopupChoice("Raise housing costs", {"budget": +2000000, "sHappiness": -10})
        ]
    ),
]

major_events = [

    PopupEvent(
        "Annual Board Meeting",
        "The Board of Trustees has asked you what to emphasize in this year’s performance review.",
        "major",
        [
            PopupChoice("Highlight student success", {"prestige": +10, "academics": +10, "sHappiness": +10, "aHappiness": +5, "budget": -1000000}),
            PopupChoice("Focus on cost-saving", {"budget": +5000000, "sHappiness": -5, "aHappiness": -5}),
            PopupChoice("Propose expansion plan", {"prestige": +10, "academics": +10, "budget": -6000000})
        ]
    ),

    PopupEvent(
        "Campus Safety Review",
        "A state inspection team is visiting to evaluate campus security and emergency readiness.",
        "major",
        [
            PopupChoice("Invest heavily in upgrades", {"budget": -4000000, "security": +10, "prestige": +5, "sHappiness": +5}),
            PopupChoice("Provide minimal upgrades", {"budget": -1000000, "security": +5}),
            PopupChoice("Ignore recommendations", {"security": -5, "prestige": -5, "sHappiness": -5})
        ]
    ),
]


if __name__ == "__main__":
    m = Metrics()

    print("Initial metrics:")
    print("Budget:", m.budget, "| Prestige:", m.prestige, "| Student Happiness:", m.sHappiness, "| Security:", m.security, "| Academics:", m.academics, "| Profesor Happiness:", m.aHappiness)

    # run first popup
    event = minor_events[0]
    event.trigger_choice(0, m)

    print("After event:")
    print("Budget:", m.budget, "| Prestige:", m.prestige, "| Student Happiness:", m.sHappiness, "| Security:", m.security, "| Academics:", m.academics, "| Profesor Happiness:", m.aHappiness)