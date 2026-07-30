# Detective AI: The Case Files

A text-based detective game where you investigate a procedurally generated
crime, gather evidence, interview suspects, and use a **trained machine
learning model** (`scikit-learn` RandomForestClassifier) to estimate each
suspect's probability of guilt — based only on the evidence *you've actually
uncovered* in that playthrough.

Built from the accompanying project specification (`Detective AI: The Case
Files` design doc), implementing Phases 1–6: game engine, procedural case
generator, investigation logic, ML dataset + training pipeline, and full
integration of the model into gameplay.

## Quick start

```bash
pip install scikit-learn pandas joblib
python main.py
```

The first time you run the game (or `ai/train_model.py`), it will
auto-generate a synthetic dataset of 1,000 simulated past cases
(`ai/dataset.csv`) and train the guilt-prediction model (`ai/model.pkl`),
typically landing at ~85-90% test accuracy — matching the target range in
the spec.

You can also retrain manually at any time:

```bash
python ai/train_model.py
```

## How to play

Every game generates a brand-new case: a victim, a location, a crime type,
and 4-5 suspects — one of whom is guilty. You have a limited pool of
**investigation points** to spend before you must name a suspect.

Commands:

| Command | Cost | Effect |
|---|---|---|
| `search` | 3 | Search the crime scene, turning up new evidence leads |
| `evidence` | free | List evidence you've discovered so far |
| `analyze <n>` | 1 | Closely examine a discovered evidence item, revealing details |
| `suspects` | free | List all suspects and what you know about them |
| `profile <name>` | free | View a suspect's psychological profile |
| `interview <name>` | 2 | Question a suspect; reveals their alibi and demeanor |
| `ai` | 2 | Run the ML guilt-prediction analysis across all suspects |
| `accuse <name>` | ends game | Name the culprit |

**Key mechanic:** the AI's prediction is only as good as your legwork. Physical
and digital evidence (found via `search` + `analyze`) reveal fingerprint/DNA/
digital-trail features to the model; interviews reveal motive strength and
whether a suspect's alibi holds up. An unexamined suspect looks "innocent" to
the model by default — you have to do the work to unmask them.

### Scoring

- Correct accusation: **+500**, plus **+50** per analyzed evidence item tied
  to the real culprit, plus **+100** if you ran the AI analysis.
- Wrong accusation: **-300**.
- Ranks: Rookie (0+) → Inspector (500+) → Master Detective (1500+).

## Project structure

```
AI_Crime_Detective/
├── main.py                  # CLI entry point / game loop
├── game/
│   ├── detective.py         # Player state: score, rank, investigation points
│   ├── suspect.py           # Suspect profile + hidden ground-truth evidence features
│   ├── evidence.py          # Evidence objects + procedural evidence-pool builder
│   ├── case.py               # Procedural case generator (victim, suspects, evidence, culprit)
│   └── investigation.py     # Game session: search/interview/analyze/AI/accuse actions
├── ai/
│   ├── train_model.py       # Synthetic dataset generation + RandomForest training
│   ├── predictor.py         # Loads the trained model, scores suspects live in-game
│   ├── dataset.csv          # Generated on first run/train
│   └── model.pkl            # Generated on first run/train
├── data/
│   ├── suspects.json        # Name/occupation/relationship pools
│   ├── crimes.json          # Crime types, victims, locations
│   └── evidence.json        # Evidence description templates
└── README.md
```

## How the ML model works

Each suspect has a hidden 7-feature vector: `fingerprint`, `dna_match`,
`motive_strength` (0/1/2), `witness_identification`, `suspicious_behavior`,
`false_alibi`, `digital_evidence`. The real culprit is generated with a
higher (but not certain) chance of having incriminating features — so the
game is solvable through evidence, but never a guaranteed slam dunk.

`ai/train_model.py` generates 1,000 synthetic "historical cases" using the
same probability distributions, trains a `RandomForestClassifier` on them,
and evaluates held-out accuracy. During play, `ai/predictor.py` takes
whatever subset of features you've actually revealed (unrevealed features
default to 0 — "no evidence found yet") and returns a live guilt probability
per suspect.

## Possible extensions (not included in this build)

The original spec also envisioned a few stretch goals you could add on top
of this foundation:

- **Pygame GUI**: a visual detective's office / evidence board instead of
  the terminal interface.
- **NetworkX relationship graph**: a visual graph of evidence-suspect-weapon
  connections (currently represented as text).
- **LLM-powered interviews**: replace the templated suspect responses with
  a real language model for freeform Q&A.
- **Multiplayer mode**: two detectives racing to solve the same case.

## Credits

Built from the "Detective AI: The Case Files" project specification —
an intermediate portfolio project combining procedural generation, OOP game
design, and a real trained ML classifier.
