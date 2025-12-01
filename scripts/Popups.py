from scripts.MetricsClass import Metrics

# applies metric changes
class AdjustMetricsTask:

    def __init__(self, budget=0, prestige=0, sHappiness=0, aHappiness=0, security=0, academics=0):
        # Defaults to zero so only provided metrics change
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
            PopupChoice("Fund extra plowing crews", {'budget': -20000000, 'sHappiness': 4, 'aHappiness': 4, 'security': 2}),
            PopupChoice("Maintain current funding", {'sHappiness': -2, 'aHappiness': -4, 'security': -2}),
            PopupChoice("Cut maintenance budget", {'budget': 10000000, 'sHappiness': -3, 'security': -2})
        ]
    ),

    PopupEvent(
        "Dining Hall Maintenance Request",
        "The dining hall needs new equipment and updated ventilation.",
        "minor",
        [
            PopupChoice("Approve full renovation", {'budget': -30000000, 'sHappiness': 4, 'prestige': 2}),
            PopupChoice("Approve partial repairs", {'budget': -10000000, 'sHappiness': 2}),
            PopupChoice("Deny request", {'sHappiness': -4, 'prestige': -2})
        ]
    ),

    PopupEvent(
        "Faculty Research Proposal",
        "Professors propose a new research investment.",
        "minor",
        [
            PopupChoice("Fund research center", {'budget': -40000000, 'academics': 4, 'aHappiness': 4, 'prestige': 4}),
            PopupChoice("Delay decision", {'aHappiness': -2, 'academics': -2}),
            PopupChoice("Reject proposal", {'aHappiness': -4, 'academics': -4, 'prestige': -4})
        ]
    ),

    PopupEvent(
        "Dorm Overcrowding",
        "Too many admitted students has caused dorm shortages across campus.",
        "minor",
        [
            PopupChoice("Add temporary housing", {'budget': -20000000, 'sHappiness': 4}),
            PopupChoice("Do nothing", {'sHappiness': -4}),
            PopupChoice("Raise housing costs", {'budget': 20000000, 'sHappiness': -4})
        ]
    ),

    PopupEvent(
        "Power Outage in Labs",
        "A power surge has damaged some lab equipment, delaying experiments.",
        "minor",
        [
            PopupChoice("Replace damaged equipment", {'budget': -25000000, 'academics': 4, 'aHappiness': 2}),
            PopupChoice("Repair only essentials", {'budget': -10000000, 'academics': 2}),
            PopupChoice("Ignore issue", {'academics': -4, 'aHappiness': -4})
        ]
    ),

    PopupEvent(
        "Campus Festival Planning",
        "Students propose funding for an annual spring festival.",
        "minor",
        [
            PopupChoice("Fully fund the event", {'budget': -15000000, 'sHappiness': 5, 'prestige': 2}),
            PopupChoice("Approve small budget", {'budget': -5000000, 'sHappiness': 2}),
            PopupChoice("Decline proposal", {'sHappiness': -4})
        ]
    ),

    PopupEvent(
        "IT Network Glitch",
        "The university network experiences frequent outages affecting classes.",
        "minor",
        [
            PopupChoice("Upgrade servers", {'budget': -20000000, 'academics': 4, 'aHappiness': 2}),
            PopupChoice("Temporary fixes", {'budget': -5000000, 'academics': 2}),
            PopupChoice("Ignore complaints", {'academics': -4, 'aHappiness': -4})
        ]
    ),

    PopupEvent(
        "Parking Shortage",
        "Faculty and students complain about lack of parking near classrooms.",
        "minor",
        [
            PopupChoice("Construct new parking lot", {'budget': -30000000, 'sHappiness': 4, 'aHappiness': 4}),
            PopupChoice("Offer shuttle service", {'budget': -10000000, 'sHappiness': 2}),
            PopupChoice("Raise parking fees", {'budget': 15000000, 'sHappiness': -4, 'aHappiness': -2})
        ]
    ),

    PopupEvent(
        "Library Hours Debate",
        "Students demand extended library hours for exam season.",
        "minor",
        [
            PopupChoice("Hire more staff and extend hours", {'budget': -10000000, 'academics': 4, 'sHappiness': 2}),
            PopupChoice("Extend hours without more staff", {'budget': -5000000, 'academics': 2, 'aHappiness': -2}),
            PopupChoice("Keep current schedule", {'academics': -2, 'sHappiness': -4})
        ]
    ),

    PopupEvent(
        "Broken Gym Equipment",
        "Athletic facilities report multiple broken machines and safety issues.",
        "minor",
        [
            PopupChoice("Purchase new equipment", {'budget': -15000000, 'sHappiness': 4}),
            PopupChoice("Repair current machines", {'budget': -5000000, 'sHappiness': 2}),
            PopupChoice("Ignore for now", {'sHappiness': -4, 'security': -2})
        ]
    ),

    PopupEvent(
        "Cafeteria Food Quality Complaints",
        "Students express dissatisfaction with cafeteria meals.",
        "minor",
        [
            PopupChoice("Hire new vendor", {'budget': -10000000, 'sHappiness': 5}),
            PopupChoice("Adjust menus slightly", {'budget': -3000000, 'sHappiness': 2}),
            PopupChoice("Defend current provider", {'sHappiness': -4})
        ]
    ),

    PopupEvent(
        "Unauthorized Drone Usage",
        "Students flying drones near administrative buildings pose privacy risks.",
        "minor",
        [
            PopupChoice("Enforce drone regulations", {'security': 4, 'sHappiness': -2}),
            PopupChoice("Create drone club with safety training", {'budget': -5000000, 'security': 2, 'sHappiness': 2}),
            PopupChoice("Ignore incidents", {'security': -4})
        ]
    ),

    PopupEvent(
        "Data Breach Attempt",
        "The IT team detects a suspicious data access attempt.",
        "minor",
        [
            PopupChoice("Upgrade cybersecurity", {'budget': -15000000, 'security': 4, 'prestige': 2}),
            PopupChoice("Investigate quietly", {'budget': -5000000, 'security': 2}),
            PopupChoice("Do nothing", {'security': -5, 'prestige': -4})
        ]
    ),

    PopupEvent(
        "Student Protest",
        "Students organize a demonstration over tuition increases.",
        "minor",
        [
            PopupChoice("Negotiate with leaders", {'sHappiness': 4, 'prestige': 2, 'budget': -10000000}),
            PopupChoice("Hold firm on pricing", {'budget': 20000000, 'sHappiness': -4}),
            PopupChoice("Call campus security", {'security': 4, 'sHappiness': -5, 'prestige': -2})
        ]
    ),

    PopupEvent(
        "Campus Mural Project",
        "An art professor proposes a large mural celebrating campus diversity.",
        "minor",
        [
            PopupChoice("Approve funding", {'budget': -10000000, 'prestige': 4, 'sHappiness': 2}),
            PopupChoice("Provide partial support", {'budget': -5000000, 'prestige': 2}),
            PopupChoice("Reject project", {'prestige': -2, 'sHappiness': -2})
        ]
    ),

    PopupEvent(
        "HVAC Malfunction",
        "Aging air systems fail in several academic buildings.",
        "minor",
        [
            PopupChoice("Replace entire system", {'budget': -30000000, 'aHappiness': 4, 'academics': 2}),
            PopupChoice("Repair core areas", {'budget': -10000000, 'aHappiness': 2}),
            PopupChoice("Ignore problem", {'aHappiness': -4, 'academics': -2})
        ]
    ),

    PopupEvent(
        "Visiting Scholar Opportunity",
        "A renowned professor is interested in visiting your university.",
        "minor",
        [
            PopupChoice("Offer generous package", {'budget': -25000000, 'prestige': 4, 'academics': 4}),
            PopupChoice("Offer modest package", {'budget': -10000000, 'prestige': 2, 'academics': 2}),
            PopupChoice("Decline offer", {'prestige': -2, 'academics': -2})
        ]
    ),

    PopupEvent(
        "Campus Wi-Fi Upgrade",
        "Students demand faster and more reliable Wi-Fi.",
        "minor",
        [
            PopupChoice("Invest in campus-wide upgrade", {'budget': -20000000, 'sHappiness': 4, 'aHappiness': 2}),
            PopupChoice("Upgrade key buildings", {'budget': -10000000, 'sHappiness': 2}),
            PopupChoice("Keep current system", {'sHappiness': -4})
        ]
    ),

    PopupEvent(
        "Athletic Team Success",
        "The basketball team advances to the national semifinals!",
        "minor",
        [
            PopupChoice("Host celebration event", {'budget': -10000000, 'prestige': 4, 'sHappiness': 4}),
            PopupChoice("Send congratulations only", {'prestige': 2}),
            PopupChoice("Ignore publicity", {'prestige': -2, 'sHappiness': -2})
        ]
    ),

    PopupEvent(
        "Fire Drill Failures",
        "A surprise inspection finds that fire drills weren’t properly conducted.",
        "minor",
        [
            PopupChoice("Revamp safety program", {'budget': -10000000, 'security': 4, 'prestige': 2}),
            PopupChoice("Reprimand staff quietly", {'security': 2}),
            PopupChoice("Ignore report", {'security': -4, 'prestige': -2})
        ]
    ),

    PopupEvent(
        "Cultural Exchange Week",
        "Students propose an event to celebrate international diversity.",
        "minor",
        [
            PopupChoice("Fund fully", {'budget': -15000000, 'sHappiness': 4, 'prestige': 2}),
            PopupChoice("Approve partial funding", {'budget': -5000000, 'sHappiness': 2}),
            PopupChoice("Decline proposal", {'sHappiness': -4})
        ]
    ),

    PopupEvent(
        "Lost Endowment File",
        "An important investment document is misplaced by staff.",
        "minor",
        [
            PopupChoice("Launch full investigation", {'budget': -10000000, 'security': 4}),
            PopupChoice("Quietly reissue paperwork", {'budget': -5000000}),
            PopupChoice("Ignore issue", {'prestige': -2, 'security': -4})
        ]
    ),

    PopupEvent(
        "New Cafeteria Opening",
        "A nearby franchise offers to open on campus with a profit-sharing deal.",
        "minor",
        [
            PopupChoice("Approve partnership", {'budget': 30000000, 'sHappiness': 4}),
            PopupChoice("Negotiate tougher terms", {'budget': 15000000, 'sHappiness': 2}),
            PopupChoice("Reject deal", {'sHappiness': -2})
        ]
    ),

    PopupEvent(
        "Art Exhibit Donation",
        "An alumnus offers a major art donation if given naming rights.",
        "minor",
        [
            PopupChoice("Accept donation", {'prestige': 4, 'budget': 20000000}),
            PopupChoice("Negotiate naming terms", {'prestige': 2, 'budget': 10000000}),
            PopupChoice("Decline offer", {'prestige': -2})
        ]
    ),

    PopupEvent(
        "Dorm Fire Alarm Pranks",
        "Frequent false alarms are frustrating residents.",
        "minor",
        [
            PopupChoice("Install new detection system", {'budget': -10000000, 'security': 4, 'sHappiness': 2}),
            PopupChoice("Issue warnings", {'security': 2}),
            PopupChoice("Ignore behavior", {'security': -4, 'sHappiness': -2})
        ]
    ),
]

major_events = [

    PopupEvent(
        "Annual Board Meeting",
        "The Board of Trustees has asked you what to emphasize in this year’s performance review.",
        "major",
        [
            PopupChoice("Highlight student success", {'prestige': 4, 'academics': 4, 'sHappiness': 4, 'aHappiness': 2, 'budget': -10000000}),
            PopupChoice("Focus on cost-saving", {'budget': 50000000, 'sHappiness': -2, 'aHappiness': -2}),
            PopupChoice("Propose expansion plan", {'prestige': 4, 'academics': 4, 'budget': -60000000})
        ]
    ),

    PopupEvent(
        "Campus Safety Review",
        "A state inspection team is visiting to evaluate campus security and emergency readiness.",
        "major",
        [
            PopupChoice("Invest heavily in upgrades", {'budget': -40000000, 'security': 4, 'prestige': 2, 'sHappiness': 2}),
            PopupChoice("Provide minimal upgrades", {'budget': -10000000, 'security': 2}),
            PopupChoice("Ignore recommendations", {'security': -2, 'prestige': -2, 'sHappiness': -2})
        ]
    ),

    PopupEvent(
        "Major Donor Gala",
        "A high-profile event for alumni and investors is being organized.",
        "major",
        [
            PopupChoice("Host lavish event", {'budget': -60000000, 'prestige': 5}),
            PopupChoice("Host modest reception", {'budget': -20000000, 'prestige': 4}),
            PopupChoice("Cancel due to costs", {'prestige': -4})
        ]
    ),

    PopupEvent(
        "New Campus Expansion Plan",
        "Architects present a proposal for a new research complex and dorms.",
        "major",
        [
            PopupChoice("Approve full plan", {'budget': -150000000, 'prestige': 5, 'academics': 5}),
            PopupChoice("Approve academic wing only", {'budget': -80000000, 'academics': 4}),
            PopupChoice("Reject for now", {'prestige': -4, 'academics': -2})
        ]
    ),

    PopupEvent(
        "Sports Scandal",
        "Reports surface of misconduct in the athletics department.",
        "major",
        [
            PopupChoice("Launch investigation", {'budget': -20000000, 'prestige': -2, 'security': 4}),
            PopupChoice("Publicly defend program", {'prestige': -4, 'sHappiness': -2}),
            PopupChoice("Cut implicated staff", {'prestige': 2, 'aHappiness': -4})
        ]
    ),

    PopupEvent(
        "Cybersecurity Breach",
        "Sensitive student data has been leaked online.",
        "major",
        [
            PopupChoice("Hire outside cybersecurity firm", {'budget': -50000000, 'security': 5, 'prestige': 2}),
            PopupChoice("Patch internally", {'budget': -20000000, 'security': 2}),
            PopupChoice("Downplay incident", {'prestige': -5, 'security': -4})
        ]
    ),

    PopupEvent(
        "National Accreditation Review",
        "A federal accreditation team is visiting to evaluate academic quality.",
        "major",
        [
            PopupChoice("Invest in preparation", {'budget': -40000000, 'academics': 5, 'prestige': 4}),
            PopupChoice("Do minimal work", {'budget': -10000000, 'academics': 2}),
            PopupChoice("Take chances", {'academics': -4, 'prestige': -4})
        ]
    ),

    PopupEvent(
        "Natural Disaster Damages",
        "Severe flooding has impacted parts of campus.",
        "major",
        [
            PopupChoice("Rebuild with upgrades", {'budget': -100000000, 'security': 4, 'sHappiness': 4}),
            PopupChoice("Repair essential areas", {'budget': -40000000, 'security': 2}),
            PopupChoice("Delay repairs", {'security': -4, 'sHappiness': -4})
        ]
    ),

    PopupEvent(
        "Presidential Resignation",
        "The university president suddenly announces retirement.",
        "major",
        [
            PopupChoice("Launch national search", {'budget': -30000000, 'prestige': 4, 'aHappiness': 4}),
            PopupChoice("Appoint interim from faculty", {'aHappiness': 2, 'prestige': 2}),
            PopupChoice("Leave position vacant", {'prestige': -4, 'aHappiness': -4})
        ]
    ),

    PopupEvent(
        "Tech Company Partnership",
        "A major corporation offers to collaborate on an innovation lab.",
        "major",
        [
            PopupChoice("Accept full partnership", {'budget': 80000000, 'academics': 4, 'prestige': 4}),
            PopupChoice("Negotiate limited deal", {'budget': 40000000, 'academics': 2}),
            PopupChoice("Decline offer", {'academics': -2, 'prestige': -2})
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
