from scripts.MetricsClass import Metrics

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
            PopupChoice("Maintain current funding", {"sHappiness": -5, "aHappiness": -10, "security": -5}),
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

    PopupEvent(
        "Power Outage in Labs",
        "A power surge has damaged some lab equipment, delaying experiments.",
        "minor",
        [
            PopupChoice("Replace damaged equipment", {"budget": -2500000, "academics": +10, "aHappiness": +5}),
            PopupChoice("Repair only essentials", {"budget": -1000000, "academics": +5}),
            PopupChoice("Ignore issue", {"academics": -10, "aHappiness": -10})
        ]
    ),

    PopupEvent(
        "Campus Festival Planning",
        "Students propose funding for an annual spring festival.",
        "minor",
        [
            PopupChoice("Fully fund the event", {"budget": -1500000, "sHappiness": +15, "prestige": +5}),
            PopupChoice("Approve small budget", {"budget": -500000, "sHappiness": +5}),
            PopupChoice("Decline proposal", {"sHappiness": -10})
        ]
    ),

    PopupEvent(
        "IT Network Glitch",
        "The university network experiences frequent outages affecting classes.",
        "minor",
        [
            PopupChoice("Upgrade servers", {"budget": -2000000, "academics": +10, "aHappiness": +5}),
            PopupChoice("Temporary fixes", {"budget": -500000, "academics": +5}),
            PopupChoice("Ignore complaints", {"academics": -10, "aHappiness": -10})
        ]
    ),

    PopupEvent(
        "Parking Shortage",
        "Faculty and students complain about lack of parking near classrooms.",
        "minor",
        [
            PopupChoice("Construct new parking lot", {"budget": -3000000, "sHappiness": +10, "aHappiness": +10}),
            PopupChoice("Offer shuttle service", {"budget": -1000000, "sHappiness": +5}),
            PopupChoice("Raise parking fees", {"budget": +1500000, "sHappiness": -10, "aHappiness": -5})
        ]
    ),

    PopupEvent(
        "Library Hours Debate",
        "Students demand extended library hours for exam season.",
        "minor",
        [
            PopupChoice("Hire more staff and extend hours", {"budget": -1000000, "academics": +10, "sHappiness": +5}),
            PopupChoice("Extend hours without more staff", {"budget": -500000, "academics": +5, "aHappiness": -5}),
            PopupChoice("Keep current schedule", {"academics": -5, "sHappiness": -10})
        ]
    ),

    PopupEvent(
        "Broken Gym Equipment",
        "Athletic facilities report multiple broken machines and safety issues.",
        "minor",
        [
            PopupChoice("Purchase new equipment", {"budget": -1500000, "sHappiness": +10}),
            PopupChoice("Repair current machines", {"budget": -500000, "sHappiness": +5}),
            PopupChoice("Ignore for now", {"sHappiness": -10, "security": -5})
        ]
    ),

    PopupEvent(
        "Cafeteria Food Quality Complaints",
        "Students express dissatisfaction with cafeteria meals.",
        "minor",
        [
            PopupChoice("Hire new vendor", {"budget": -1000000, "sHappiness": +15}),
            PopupChoice("Adjust menus slightly", {"budget": -300000, "sHappiness": +5}),
            PopupChoice("Defend current provider", {"sHappiness": -10})
        ]
    ),

    PopupEvent(
        "Unauthorized Drone Usage",
        "Students flying drones near administrative buildings pose privacy risks.",
        "minor",
        [
            PopupChoice("Enforce drone regulations", {"security": +10, "sHappiness": -5}),
            PopupChoice("Create drone club with safety training", {"budget": -500000, "security": +5, "sHappiness": +5}),
            PopupChoice("Ignore incidents", {"security": -10})
        ]
    ),

    PopupEvent(
        "Data Breach Attempt",
        "The IT team detects a suspicious data access attempt.",
        "minor",
        [
            PopupChoice("Upgrade cybersecurity", {"budget": -1500000, "security": +10, "prestige": +5}),
            PopupChoice("Investigate quietly", {"budget": -500000, "security": +5}),
            PopupChoice("Do nothing", {"security": -15, "prestige": -10})
        ]
    ),

    PopupEvent(
        "Student Protest",
        "Students organize a demonstration over tuition increases.",
        "minor",
        [
            PopupChoice("Negotiate with leaders", {"sHappiness": +10, "prestige": +5, "budget": -1000000}),
            PopupChoice("Hold firm on pricing", {"budget": +2000000, "sHappiness": -10}),
            PopupChoice("Call campus security", {"security": +10, "sHappiness": -15, "prestige": -5})
        ]
    ),

    PopupEvent(
        "Campus Mural Project",
        "An art professor proposes a large mural celebrating campus diversity.",
        "minor",
        [
            PopupChoice("Approve funding", {"budget": -1000000, "prestige": +10, "sHappiness": +5}),
            PopupChoice("Provide partial support", {"budget": -500000, "prestige": +5}),
            PopupChoice("Reject project", {"prestige": -5, "sHappiness": -5})
        ]
    ),

    PopupEvent(
        "HVAC Malfunction",
        "Aging air systems fail in several academic buildings.",
        "minor",
        [
            PopupChoice("Replace entire system", {"budget": -3000000, "aHappiness": +10, "academics": +5}),
            PopupChoice("Repair core areas", {"budget": -1000000, "aHappiness": +5}),
            PopupChoice("Ignore problem", {"aHappiness": -10, "academics": -5})
        ]
    ),

    PopupEvent(
        "Visiting Scholar Opportunity",
        "A renowned professor is interested in visiting your university.",
        "minor",
        [
            PopupChoice("Offer generous package", {"budget": -2500000, "prestige": +10, "academics": +10}),
            PopupChoice("Offer modest package", {"budget": -1000000, "prestige": +5, "academics": +5}),
            PopupChoice("Decline offer", {"prestige": -5, "academics": -5})
        ]
    ),

    PopupEvent(
        "Campus Wi-Fi Upgrade",
        "Students demand faster and more reliable Wi-Fi.",
        "minor",
        [
            PopupChoice("Invest in campus-wide upgrade", {"budget": -2000000, "sHappiness": +10, "aHappiness": +5}),
            PopupChoice("Upgrade key buildings", {"budget": -1000000, "sHappiness": +5}),
            PopupChoice("Keep current system", {"sHappiness": -10})
        ]
    ),

    PopupEvent(
        "Athletic Team Success",
        "The basketball team advances to the national semifinals!",
        "minor",
        [
            PopupChoice("Host celebration event", {"budget": -1000000, "prestige": +10, "sHappiness": +10}),
            PopupChoice("Send congratulations only", {"prestige": +5}),
            PopupChoice("Ignore publicity", {"prestige": -5, "sHappiness": -5})
        ]
    ),

    PopupEvent(
        "Fire Drill Failures",
        "A surprise inspection finds that fire drills weren’t properly conducted.",
        "minor",
        [
            PopupChoice("Revamp safety program", {"budget": -1000000, "security": +10, "prestige": +5}),
            PopupChoice("Reprimand staff quietly", {"security": +5}),
            PopupChoice("Ignore report", {"security": -10, "prestige": -5})
        ]
    ),

    PopupEvent(
        "Cultural Exchange Week",
        "Students propose an event to celebrate international diversity.",
        "minor",
        [
            PopupChoice("Fund fully", {"budget": -1500000, "sHappiness": +10, "prestige": +5}),
            PopupChoice("Approve partial funding", {"budget": -500000, "sHappiness": +5}),
            PopupChoice("Decline proposal", {"sHappiness": -10})
        ]
    ),

    PopupEvent(
        "Lost Endowment File",
        "An important investment document is misplaced by staff.",
        "minor",
        [
            PopupChoice("Launch full investigation", {"budget": -1000000, "security": +10}),
            PopupChoice("Quietly reissue paperwork", {"budget": -500000}),
            PopupChoice("Ignore issue", {"prestige": -5, "security": -10})
        ]
    ),

    PopupEvent(
        "New Cafeteria Opening",
        "A nearby franchise offers to open on campus with a profit-sharing deal.",
        "minor",
        [
            PopupChoice("Approve partnership", {"budget": +3000000, "sHappiness": +10}),
            PopupChoice("Negotiate tougher terms", {"budget": +1500000, "sHappiness": +5}),
            PopupChoice("Reject deal", {"sHappiness": -5})
        ]
    ),

    PopupEvent(
        "Art Exhibit Donation",
        "An alumnus offers a major art donation if given naming rights.",
        "minor",
        [
            PopupChoice("Accept donation", {"prestige": +10, "budget": +2000000}),
            PopupChoice("Negotiate naming terms", {"prestige": +5, "budget": +1000000}),
            PopupChoice("Decline offer", {"prestige": -5})
        ]
    ),

    PopupEvent(
        "Dorm Fire Alarm Pranks",
        "Frequent false alarms are frustrating residents.",
        "minor",
        [
            PopupChoice("Install new detection system", {"budget": -1000000, "security": +10, "sHappiness": +5}),
            PopupChoice("Issue warnings", {"security": +5}),
            PopupChoice("Ignore behavior", {"security": -10, "sHappiness": -5})
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

    PopupEvent(
        "Major Donor Gala",
        "A high-profile event for alumni and investors is being organized.",
        "major",
        [
            PopupChoice("Host lavish event", {"budget": -6000000, "prestige": +15, "budget": +8000000}),
            PopupChoice("Host modest reception", {"budget": -2000000, "prestige": +10}),
            PopupChoice("Cancel due to costs", {"prestige": -10})
        ]
    ),

    PopupEvent(
        "New Campus Expansion Plan",
        "Architects present a proposal for a new research complex and dorms.",
        "major",
        [
            PopupChoice("Approve full plan", {"budget": -15000000, "prestige": +15, "academics": +15}),
            PopupChoice("Approve academic wing only", {"budget": -8000000, "academics": +10}),
            PopupChoice("Reject for now", {"prestige": -10, "academics": -5})
        ]
    ),

    PopupEvent(
        "Sports Scandal",
        "Reports surface of misconduct in the athletics department.",
        "major",
        [
            PopupChoice("Launch investigation", {"budget": -2000000, "prestige": -5, "security": +10}),
            PopupChoice("Publicly defend program", {"prestige": -10, "sHappiness": -5}),
            PopupChoice("Cut implicated staff", {"prestige": +5, "aHappiness": -10})
        ]
    ),

    PopupEvent(
        "Cybersecurity Breach",
        "Sensitive student data has been leaked online.",
        "major",
        [
            PopupChoice("Hire outside cybersecurity firm", {"budget": -5000000, "security": +15, "prestige": +5}),
            PopupChoice("Patch internally", {"budget": -2000000, "security": +5}),
            PopupChoice("Downplay incident", {"prestige": -15, "security": -10})
        ]
    ),

    PopupEvent(
        "National Accreditation Review",
        "A federal accreditation team is visiting to evaluate academic quality.",
        "major",
        [
            PopupChoice("Invest in preparation", {"budget": -4000000, "academics": +15, "prestige": +10}),
            PopupChoice("Do minimal work", {"budget": -1000000, "academics": +5}),
            PopupChoice("Take chances", {"academics": -10, "prestige": -10})
        ]
    ),

    PopupEvent(
        "Natural Disaster Damages",
        "Severe flooding has impacted parts of campus.",
        "major",
        [
            PopupChoice("Rebuild with upgrades", {"budget": -10000000, "security": +10, "sHappiness": +10}),
            PopupChoice("Repair essential areas", {"budget": -4000000, "security": +5}),
            PopupChoice("Delay repairs", {"security": -10, "sHappiness": -10})
        ]
    ),

    PopupEvent(
        "Presidential Resignation",
        "The university president suddenly announces retirement.",
        "major",
        [
            PopupChoice("Launch national search", {"budget": -3000000, "prestige": +10, "aHappiness": +10}),
            PopupChoice("Appoint interim from faculty", {"aHappiness": +5, "prestige": +5}),
            PopupChoice("Leave position vacant", {"prestige": -10, "aHappiness": -10})
        ]
    ),

    PopupEvent(
        "Tech Company Partnership",
        "A major corporation offers to collaborate on an innovation lab.",
        "major",
        [
            PopupChoice("Accept full partnership", {"budget": +8000000, "academics": +10, "prestige": +10}),
            PopupChoice("Negotiate limited deal", {"budget": +4000000, "academics": +5}),
            PopupChoice("Decline offer", {"academics": -5, "prestige": -5})
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