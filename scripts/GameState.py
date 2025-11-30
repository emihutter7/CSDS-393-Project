from .db import (
    save_metrics, load_metrics,
    save_buildings, load_buildings,
    save_popups, load_popups
)

class GameState:
    def __init__(self, turn=1, score=0, buildings=None, popups=None):
        self.time_of_year = "Fall"
        self.turn = turn
        self.score = score
        self.buildings = buildings or {}
        self.popups = popups or []         
        self.max_turns = 16

    def load(self):
        self.score, self.time_of_year, self.turn = load_metrics()
        self.buildings = load_buildings()
        self.popups = load_popups()
        print("Game state loaded from database.")

    def save(self):
        save_metrics(self.score, self.time_of_year, self.turn)
        save_buildings(self.buildings)
        save_popups(self.popups)
        print("Game state saved to database.")

    def next_turn(self):
        self.turn += 1
        if self.turn % 2 == 0:
            self.time_of_year = "Fall" if self.time_of_year == "Spring" else "Spring"
        
        print(f"Turn {self.turn} completed. Time of year: {self.time_of_year}")

        # Check if game is over
        if self.turn >= self.max_turns:
            print("Game Over!")
            return True  # signal that game is over
        return False