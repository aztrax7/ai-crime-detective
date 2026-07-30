import json
import os
import random

from game.suspect import Suspect
from game.evidence import build_evidence_pool

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database")


def _load_json(name):
    with open(os.path.join(DB_DIR, name), "r") as f:
        return json.load(f)


class Case:
    def __init__(self, case_id=None, num_suspects=None):
        suspects_db = _load_json("suspects.json")
        crimes_db = _load_json("crimes.json")
        evidence_db = _load_json("evidence.json")

        self.case_id = case_id or random.randint(1000, 9999)
        self.victim = random.choice(crimes_db["victim_names"])
        self.location = random.choice(crimes_db["locations"])
        self.crime = random.choice(crimes_db["crime_types"])

        n = num_suspects or random.randint(4, 5)
        culprit_index = random.randint(0, n - 1)

        names_used = set()
        self.suspects = []
        for i in range(n):
            while True:
                name = f"{random.choice(suspects_db['first_names'])} {random.choice(suspects_db['last_names'])}"
                if name not in names_used and name != self.victim:
                    names_used.add(name)
                    break
            suspect = Suspect(
                name=name,
                age=random.randint(22, 65),
                occupation=random.choice(suspects_db["occupations"]),
                relationship=random.choice(suspects_db["relationships"]),
                is_culprit=(i == culprit_index),
            )
            self.suspects.append(suspect)

        self.culprit = self.suspects[culprit_index]

        # Alibi statements: honest if not lying, evasive/contradictory if false_alibi.
        alibi_true_pool = [
            "I was at home with my partner all evening.",
            "I was at a work event with several colleagues who can confirm.",
            "I was running errands across town, I have receipts.",
            "I was at the gym, the front desk can verify my check-in time.",
        ]
        alibi_false_pool = [
            "I... was home alone, no one can really confirm that.",
            "I was around, but I don't remember exactly where.",
            "I was out for a walk by myself, nowhere in particular.",
            "I was with someone, but I'd rather not say who.",
        ]
        for s in self.suspects:
            feats = s.feature_vector()
            s.alibi_statement = random.choice(alibi_false_pool if feats["false_alibi"] else alibi_true_pool)

        self.evidence_pool = build_evidence_pool(evidence_db, self.suspects, self.victim)
        self.solved = False

    def briefing(self):
        return (
            f"CASE #{self.case_id}\n"
            f"{'-'*40}\n"
            f"Crime:     {self.crime['type']}\n"
            f"Victim:    {self.victim} ({self.crime['victim_state']})\n"
            f"Location:  {self.location}\n"
            f"Suspects:  {len(self.suspects)}\n"
            f"{'-'*40}\n"
            f"The victim was {self.crime['verb']} at the {self.location}. "
            f"You have {len(self.suspects)} suspects and a limited amount of time "
            f"to gather evidence before you must name the culprit."
        )

    def get_suspect(self, name):
        name = name.strip().lower()
        # Exact match takes priority.
        for s in self.suspects:
            if s.name.lower() == name:
                return s
        # Fall back to a unique prefix match (e.g. "carlos" -> "Carlos Smith").
        matches = [s for s in self.suspects if s.name.lower().startswith(name)]
        if len(matches) == 1:
            return matches[0]
        return None
