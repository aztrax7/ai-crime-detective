"""Suspect model: identity, psychological profile, and the hidden evidence
feature vector that the ML predictor will eventually see (piece by piece,
as the player uncovers it)."""

import random


class Suspect:
    def __init__(self, name, age, occupation, relationship, is_culprit):
        self.name = name
        self.age = age
        self.occupation = occupation
        self.relationship = relationship
        self.is_culprit = is_culprit

        # Psychological profile (0-100). Flavor + influences interview tone.
        self.honesty = random.randint(10, 90)
        self.aggression = random.randint(10, 90)
        self.intelligence = random.randint(10, 90)
        self.greed = random.randint(10, 90)
        self.fear = random.randint(10, 90)

        # Hidden ground-truth evidence features (what the ML model consumes).
        # Culprits are *more likely* to have incriminating features, but it's
        # probabilistic -- innocent suspects can look suspicious too.
        self.fingerprint = self._roll(0.75, 0.15)
        self.motive_strength = self._roll_motive()
        self.witness_identification = self._roll(0.55, 0.15)
        self.suspicious_behavior = self._roll(0.70, 0.20)
        self.false_alibi = self._roll(0.70, 0.20)
        self.digital_evidence = self._roll(0.55, 0.15)

        # What the player has actually uncovered so far (starts empty).
        self.revealed_evidence = []       # list of Evidence objects
        self.interviewed = False
        self.alibi_statement = None

    def _roll(self, p_if_culprit, p_if_innocent):
        p = p_if_culprit if self.is_culprit else p_if_innocent
        return 1 if random.random() < p else 0

    def _roll_motive(self):
        # 0 = none, 1 = weak, 2 = strong
        if self.is_culprit:
            weights = [0.10, 0.30, 0.60]
        else:
            weights = [0.60, 0.30, 0.10]
        return random.choices([0, 1, 2], weights=weights, k=1)[0]

    def feature_vector(self):
        """Full ground-truth feature vector (used internally / for the
        'omniscient' case generator, not shown directly to the player)."""
        return {
            "fingerprint": self.fingerprint,
            "dna_match": 1 if (self.fingerprint and random.random() < 0.5) else 0,
            "motive_strength": self.motive_strength,
            "witness_identification": self.witness_identification,
            "suspicious_behavior": self.suspicious_behavior,
            "false_alibi": self.false_alibi,
            "digital_evidence": self.digital_evidence,
        }

    def summary_line(self):
        return f"{self.name} ({self.age}) - {self.occupation} | {self.relationship}"

    def profile_block(self):
        return (
            f"Honesty:      {self.honesty}%\n"
            f"Aggression:   {self.aggression}%\n"
            f"Intelligence: {self.intelligence}%\n"
            f"Greed:        {self.greed}%\n"
            f"Fear:         {self.fear}%"
        )
