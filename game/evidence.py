"""Evidence objects: what the player actually finds and reads."""

import random


class Evidence:
    def __init__(self, name, category, description, associated_suspect, reliability, importance):
        self.name = name
        self.category = category            # "Physical", "Digital", "Testimony"
        self.description = description
        self.associated_suspect = associated_suspect   # Suspect object or None
        self.reliability = reliability      # 0-100
        self.importance = importance        # 1-5
        self.discovered = False

    def card(self):
        who = self.associated_suspect.name if self.associated_suspect else "Unclear"
        return (
            f"[{self.category}] {self.name}\n"
            f"  {self.description}\n"
            f"  Linked to: {who} | Reliability: {self.reliability}% | Importance: {self.importance}/5"
        )


def build_evidence_pool(templates, suspects, victim_name):
    """Create a pool of Evidence objects, some pointing at the real culprit,
    some pointing at innocent suspects (red herrings), some neutral scene evidence."""
    pool = []
    categories = ["physical", "digital", "testimony"]

    for suspect in suspects:
        feats = suspect.feature_vector()

        if feats["fingerprint"] or feats["dna_match"]:
            desc = random.choice(templates["physical"]).format(suspect=suspect.name)
            pool.append(Evidence(
                name=f"Physical trace ({suspect.name})",
                category="Physical",
                description=desc,
                associated_suspect=suspect,
                reliability=random.randint(60, 95),
                importance=4 if suspect.is_culprit else random.randint(1, 3),
            ))

        if feats["digital_evidence"]:
            desc = random.choice(templates["digital"]).format(suspect=suspect.name)
            pool.append(Evidence(
                name=f"Digital record ({suspect.name})",
                category="Digital",
                description=desc,
                associated_suspect=suspect,
                reliability=random.randint(50, 90),
                importance=3 if suspect.is_culprit else random.randint(1, 3),
            ))

        if feats["witness_identification"] or feats["suspicious_behavior"]:
            desc = random.choice(templates["testimony"]).format(suspect=suspect.name)
            pool.append(Evidence(
                name=f"Witness account ({suspect.name})",
                category="Testimony",
                description=desc,
                associated_suspect=suspect,
                reliability=random.randint(35, 80),
                importance=3 if suspect.is_culprit else random.randint(1, 2),
            ))

    # A couple of generic scene-evidence items with no clear owner (atmosphere / red herrings).
    generic = [
        f"The scene near the {victim_name.split()[-1]} case shows signs of a struggle.",
        "A torn piece of fabric was found but doesn't clearly match anyone yet.",
        "An unidentified set of keys was recovered at the scene.",
    ]
    for desc in random.sample(generic, k=min(2, len(generic))):
        pool.append(Evidence(
            name="Unidentified scene evidence",
            category=random.choice(["Physical", "Testimony"]),
            description=desc,
            associated_suspect=None,
            reliability=random.randint(20, 50),
            importance=1,
        ))

    random.shuffle(pool)
    return pool
