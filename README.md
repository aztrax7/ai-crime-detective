# AI Crime Detective 🕵️

**It's basically like if Sherlock Holmes met `scikit-learn` 🔥**

AI Crime Detective is a Python-based, text adventure game where you investigate randomly generated crimes, question suspects, collect evidence, and try to catch the culprit before running out of investigation points.

**Plot twist:** you've got an AI assistant helping you crack the case.

But it's not some all-knowing detective, btw. It can only work with the evidence you've uncovered, and its predictions aren't always right. So yeah, you'll still need to use your brain.

## How I built it

I built the game using **Python, object-oriented programming (OOP), and machine learning.**

The cases are procedurally generated, so every investigation is different. The game randomly picks a crime, victim, location, 4–5 suspects, and one actual culprit.

For the AI side, I trained a **Random Forest classifier** using scikit-learn on 1,000 synthetically generated suspect records. It looks at seven features:

- Fingerprint and DNA evidence
- Motive strength
- Witness identification
- Suspicious behavior
- False alibis
- Digital evidence

The model uses the information you've discovered to estimate how suspicious each suspect is. Basically, the more useful evidence you find, the better informed its predictions can be.

**Tech stack:** Python · scikit-learn · pandas · joblib · JSON

## What can you actually do?

- **Solve different cases:** Randomly generated crimes, suspects, and evidence. No two investigations have to play out the same way.
- **Search crime scenes:** Discover physical clues, digital records, and witness statements.
- **Interrogate suspects:** Ask questions, investigate motives, and check their alibis.
- **Consult the AI:** Get a ranking of suspects based on their estimated guilt probabilities.
- **Manage your resources:** You only get 18 investigation points. You can't just spam every action and hope for the best.
- **Earn detective ranks:** Solve cases, collect points, and climb from Rookie to Master Detective.

Oh, and innocent suspects can have incriminating evidence too. Wouldn't be much of a detective game otherwise.

## Installation

You'll need Python installed.

Clone the repository and install the dependencies:

```bash
git clone https://github.com/aztrax7/ai-crime-detective.git
cd ai-crime-detective
pip install scikit-learn pandas joblib
```

Then launch the game:

```bash
python main.py
```

The repository includes a trained model. If the model file is missing, the program automatically trains one.

## How to play

Enter your detective name, read the case briefing, and start investigating.

| Command | What it does | Points |
|---|---|---|
| `search` | Search the crime scene | 3 |
| `evidence` | View discovered evidence | Free |
| `analyze <number>` | Examine a clue | 1 |
| `suspects` | List all suspects | Free |
| `profile <name>` | View a suspect's profile | Free |
| `interview <name>` | Question a suspect | 2 |
| `ai` | Run AI guilt predictions | 2 |
| `accuse <name>` | Make your final accusation | Ends case |
| `help` | Display commands | Free |
| `quit` | Leave the game | Free |

**Your starting budget: 18 investigation points.**

You'll earn **500 points** for correctly identifying the culprit, plus bonuses for analyzing relevant evidence (+50 per clue) and using the AI (+100).

Wrong accusation? **-300 points.** Yeah, that one's gonna hurt.

## A little more about the AI

The model uses a `RandomForestClassifier` with 200 decision trees, trained using an 80/20 train-test split.

The training dataset is synthetic, meaning I generated simulated examples rather than using real criminal records. Each example contains seven evidence features and a label indicating whether the simulated suspect is guilty.

During gameplay, the AI uses the features you've uncovered to estimate guilt probabilities and rank suspects.

**Small disclaimer:** This isn't a real-world crime prediction tool. It's a fictional investigation game designed to explore how machine learning can assist with decision-making.

The current version also treats undiscovered features as zero, which can affect prediction accuracy. That's something I'd like to improve.

## Project structure

```text
ai-crime-detective/
├── main.py          # Runs the game
├── game/            # Game logic, cases, suspects, evidence
├── ai/              # ML training and prediction system
├── data/            # JSON templates for generating cases
└── README.md
```

## What's next?

A few upgrades I've got in mind:

- A proper GUI, because the terminal can only do so much.
- An interactive evidence board linking suspects and clues.
- More realistic interviews, potentially using an LLM.
- Better model evaluation and explainable AI predictions.
- Multiplayer detective mode, because why not?

## Why I made this

I wanted to build something that combined **game development, Python, and machine learning** without making another generic prediction app.

And honestly, the idea of building a detective game where an AI helps you solve crimes sounded pretty cool.

It's not perfect, and there are definitely things I want to improve. But it was a fun way to experiment with procedural generation, OOP, and getting an ML model to actually do something inside a playable game.

**Now go solve some crimes.**
