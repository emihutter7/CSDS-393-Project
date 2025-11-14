from .db import (
    save_metrics, load_metrics,
    save_buildings, load_buildings,
    save_popups, load_popups
)

class GameState:
    def __init__(self):
        self.score = 0
        self.time_of_year = "Fall"
        self.buildings = {}
        self.popups = []

    def load(self):
        self.score, self.time_of_year = load_metrics()
        self.buildings = load_buildings()
        self.popups = load_popups()
        print("Game state loaded from database.")

    def save(self):
        save_metrics(self.score, self.time_of_year)
        save_buildings(self.buildings)
        save_popups(self.popups)
        print("Game state saved to database.")
