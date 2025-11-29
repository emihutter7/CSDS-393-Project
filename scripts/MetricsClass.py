class Metrics:

    # figures based off of 2026 reports, ~$70,000/year x 6,500 undergrads
    # ranking 51 / 430
    # shappiness 75%
    # ahappiness 60%
    # security = 50%
    # academics = 80%

    def __init__(self):
        self._prestige = 51
        self._budget = 450000000
        self._sHappiness = 75
        self._aHappiness = 60
        self._security = 50
        self._academics = 80

    @property
    def prestige(self):
        return self._prestige

    @prestige.setter
    def prestige(self, value):
        if value < 0:
            raise ValueError("Prestige cannot be negative.")
        self._prestige = value

    @property
    def budget(self):
        return self._budget
    
    @budget.setter
    def budget(self, value):
        if value < 0:
            raise ValueError("Budget cannot be negative.")
        self._budget = value

    @property
    def sHappiness(self):
        return self._sHappiness

    @sHappiness.setter
    def sHappiness(self, value):
        if value < 0:
            raise ValueError("Student Happiness cannot be negative.")
        self._sHappiness = value
    
    @property
    def aHappiness(self):
        return self._aHappiness

    @aHappiness.setter
    def aHappiness(self, value):
        if value < 0:
            raise ValueError("Admin Happiness cannot be negative.")
        self._aHappiness = value
    
    @property
    def security(self):
        return self._security

    @security.setter
    def security(self, value):
        if value < 0:
            raise ValueError("Security cannot be negative.")
        self._security = value

    @property
    def academics(self):
        return self._academics

    @academics.setter
    def academics(self, value):
        if value < 0:
            raise ValueError("Academics cannot be negative.")
        self._academics = value
    
    def calculate_final_score(self):
        # Define weights for each metric
        weights = {
            "budget": 0.25,
            "prestige": 0.25,
            "sHappiness": 0.2,
            "aHappiness": 0.15,
            "security": 0.1,
            "academics": 0.1
        }

        # Compute normalized deltas
        delta_budget     = (self.metrics.budget - self._budget) / self._budget
        delta_prestige   = (self.metrics.prestige - self._prestige) / self._prestige
        delta_sHappiness = (self.metrics.sHappiness - self._sHappiness) / self._sHappiness
        delta_aHappiness = (self.metrics.aHappiness - self._aHappiness) / self._aHappiness
        delta_security   = (self.metrics.security - self._security) / self._security
        delta_academics  = (self.metrics.academics - self._academics) / self._academics

        # Weighted sum of normalized deltas
        score = (
            delta_budget * weights["budget"] +
            delta_prestige * weights["prestige"] +
            delta_sHappiness * weights["sHappiness"] +
            delta_aHappiness * weights["aHappiness"] +
            delta_security * weights["security"] +
            delta_academics * weights["academics"]
        )

        # Optional: scale to a nicer number, e.g., multiply by 100
        score *= 100

        return score

