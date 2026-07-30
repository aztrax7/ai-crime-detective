import random

from ai.predictor import GuiltPredictor

COST_SEARCH = 3
COST_ANALYZE = 1
COST_INTERVIEW = 2
COST_AI_ANALYSIS = 2

INTERVIEW_QUESTIONS = [
    "Where were you at the time of the crime?",
    "Did you have any conflict with the victim?",
    "Do you know anyone who might want to harm the victim?",
    "Can anyone confirm your whereabouts?",
]


class GameSession:
    def __init__(self, case, detective):
        self.case = case
        self.detective = detective
        self.predictor = GuiltPredictor()

        # Track what's been revealed to the player.
        self.discovered_evidence = []          # Evidence objects, "found" but maybe not yet analyzed
        self.analyzed_evidence = []             # Evidence objects fully read
        self.known_features = {s.name: {} for s in self.case.suspects}
        self.ai_analysis_run = False
        self.finished = False
        self.result = None  # "won" / "lost"

    # ---------- Actions ----------

    def search_scene(self):
        if not self.detective.can_afford(COST_SEARCH):
            return "Not enough investigation points left to search."
        undiscovered = [e for e in self.case.evidence_pool if e not in self.discovered_evidence]
        if not undiscovered:
            return "There is nothing new to find at the scene. Try analyzing what you already have, or interview a suspect."

        self.detective.spend(COST_SEARCH)
        batch = random.sample(undiscovered, k=min(2, len(undiscovered)))
        lines = ["You search the scene and turn up new leads:"]
        for e in batch:
            self.discovered_evidence.append(e)
            e.discovered = True
            lines.append(f"  - [{e.category}] {e.name}  (use 'analyze' to examine it)")
        return "\n".join(lines)

    def list_discovered(self):
        if not self.discovered_evidence:
            return "No evidence discovered yet. Try searching the scene first."
        lines = ["Discovered evidence:"]
        for i, e in enumerate(self.discovered_evidence, 1):
            tag = "(analyzed)" if e in self.analyzed_evidence else "(not yet analyzed)"
            lines.append(f"  {i}. [{e.category}] {e.name} {tag}")
        return "\n".join(lines)

    def analyze_evidence(self, index):
        if not self.detective.can_afford(COST_ANALYZE):
            return "Not enough investigation points left to analyze evidence."
        if index < 1 or index > len(self.discovered_evidence):
            return "Invalid evidence number. Use 'evidence' to list what you've found."

        e = self.discovered_evidence[index - 1]
        self.detective.spend(COST_ANALYZE)
        if e not in self.analyzed_evidence:
            self.analyzed_evidence.append(e)
            self._absorb_evidence_into_features(e)
        return "You analyze the evidence closely:\n" + e.card()

    def _absorb_evidence_into_features(self, e):
        if e.associated_suspect is None:
            return
        suspect = e.associated_suspect
        feats = suspect.feature_vector()
        kf = self.known_features[suspect.name]
        if e.category == "Physical":
            kf["fingerprint"] = feats["fingerprint"]
            kf["dna_match"] = feats["dna_match"]
        elif e.category == "Digital":
            kf["digital_evidence"] = feats["digital_evidence"]
        elif e.category == "Testimony":
            kf["witness_identification"] = feats["witness_identification"]
            kf["suspicious_behavior"] = feats["suspicious_behavior"]

    def interview(self, suspect_name):
        if not self.detective.can_afford(COST_INTERVIEW):
            return "Not enough investigation points left to interview anyone."
        suspect = self.case.get_suspect(suspect_name)
        if suspect is None:
            return f"No suspect matching '{suspect_name}'. Use 'suspects' to see the list."

        self.detective.spend(COST_INTERVIEW)
        suspect.interviewed = True
        feats = suspect.feature_vector()
        kf = self.known_features[suspect.name]
        kf["motive_strength"] = feats["motive_strength"]
        kf["false_alibi"] = feats["false_alibi"]

        question = random.choice(INTERVIEW_QUESTIONS)
        lines = [
            f"You question {suspect.name}.",
            f"  Q: {question}",
            f'  A: "{suspect.alibi_statement}"',
        ]
        if feats["false_alibi"] or feats["suspicious_behavior"]:
            if suspect.fear > 60 or suspect.honesty < 40:
                lines.append("  (They seem visibly nervous, avoiding eye contact.)")
            else:
                lines.append("  (Something about their story feels slightly off.)")
        else:
            lines.append("  (They answer calmly and directly.)")
        return "\n".join(lines)

    def check_database(self):
        lines = ["Suspect database:"]
        for s in self.case.suspects:
            flags = []
            if s.interviewed:
                flags.append("interviewed")
            n_ev = sum(1 for e in self.analyzed_evidence if e.associated_suspect is s)
            if n_ev:
                flags.append(f"{n_ev} evidence analyzed")
            flag_str = f" [{', '.join(flags)}]" if flags else ""
            lines.append(f"  - {s.summary_line()}{flag_str}")
        return "\n".join(lines)

    def suspect_profile(self, suspect_name):
        suspect = self.case.get_suspect(suspect_name)
        if suspect is None:
            return f"No suspect matching '{suspect_name}'."
        return (
            f"{suspect.summary_line()}\n"
            f"{suspect.profile_block()}\n"
            + ("Alibi given: \"" + suspect.alibi_statement + "\"" if suspect.interviewed else "Not yet interviewed.")
        )

    def run_ai_analysis(self):
        if not self.detective.can_afford(COST_AI_ANALYSIS):
            return "Not enough investigation points left to run an AI analysis."
        self.detective.spend(COST_AI_ANALYSIS)
        self.ai_analysis_run = True

        ranked = self.predictor.rank_suspects(self.known_features)
        lines = ["AI GUILT PREDICTION (based on evidence uncovered so far):"]
        for name, prob in ranked:
            bar = "#" * int(prob * 20)
            lines.append(f"  {name:<20} {prob*100:5.1f}%  {bar}")
        lines.append("(Note: probabilities reflect only what you've uncovered. Investigate further to sharpen them.)")
        return "\n".join(lines)

    def accuse(self, suspect_name):
        suspect = self.case.get_suspect(suspect_name)
        if suspect is None:
            return f"No suspect matching '{suspect_name}'.", False

        self.finished = True
        self.case.solved = True
        correct = suspect.is_culprit

        if correct:
            self.result = "won"
            base = 500
            key_evidence_bonus = 50 * sum(
                1 for e in self.analyzed_evidence if e.associated_suspect is suspect
            )
            ai_bonus = 100 if self.ai_analysis_run else 0
            total = base + key_evidence_bonus + ai_bonus
            self.detective.add_score(total)
            self.detective.cases_solved += 1
            msg = (
                f"You accuse {suspect.name}... and you're RIGHT!\n"
                f"{suspect.name} was the true culprit.\n"
                f"Score breakdown: +{base} correct culprit, +{key_evidence_bonus} key evidence, "
                f"+{ai_bonus} AI analysis used.\n"
                f"Total points earned: {total}"
            )
        else:
            self.result = "lost"
            self.detective.add_score(-300)
            msg = (
                f"You accuse {suspect.name}... but you're WRONG.\n"
                f"The real culprit was {self.case.culprit.name}.\n"
                f"Score penalty: -300"
            )

        self.detective.cases_played += 1
        return msg, correct
