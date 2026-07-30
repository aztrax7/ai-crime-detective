RANKS = [
    (0, "Rookie"),
    (500, "Inspector"),
    (1500, "Master Detective"),
]


class Detective:
    def __init__(self, name="Detective", starting_points=18):
        self.name = name
        self.score = 0
        self.points = starting_points
        self.max_points = starting_points
        self.cases_solved = 0
        self.cases_played = 0

    def can_afford(self, cost):
        return self.points >= cost

    def spend(self, cost):
        self.points -= cost

    def add_score(self, amount):
        self.score += amount

    def rank(self):
        current = RANKS[0][1]
        for threshold, name in RANKS:
            if self.score >= threshold:
                current = name
        return current

    def status_line(self):
        return f"{self.name} | Score: {self.score} | Rank: {self.rank()} | Investigation points left: {self.points}/{self.max_points}"
