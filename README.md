# AI Crime Detective

A Python-based detective game where you solve randomly generated crimes with a little help from machine learning.

The idea is pretty simple: you're a detective, there's been a crime, and you've got a handful of suspects. Your job is to investigate the scene, collect evidence, question suspects, and figure out who's guilty before you run out of investigation points.

The twist? You have an AI assistant that can analyze the evidence you've collected and predict which suspects are most likely guilty. But it doesn't magically know the answer. The more you investigate, the more information it has to work with.

## How I built it

I built this project using **Python, object-oriented programming (OOP), and machine learning.**

The game itself uses procedural generation, meaning every new case has different suspects, victims, locations, and evidence. Behind the scenes, there's a Random Forest classifier trained using scikit-learn on 1,000 synthetically generated suspect records.

Each suspect has seven evidence-related features, including fingerprints, DNA matches, motives, witness identification, suspicious behavior, false alibis, and digital evidence. The model uses whichever features you've uncovered to estimate guilt probabilities.

**Tech stack:** Python, scikit-learn, pandas, joblib, JSON

## Features

- **Randomly generated cases:** Different crimes, locations, victims, and 4–5 suspects each time.
- **Evidence collection:** Search crime scenes and examine physical, digital, and witness evidence.
- **Suspect interviews:** Question suspects, check alibis, and look for suspicious behavior.
- **AI predictions:** Use a trained Random Forest model to rank suspects based on discovered evidence.
- **Limited investigation points:** Every major action costs points, so you can't just investigate everything.
- **Scoring and ranks:** Earn points for solving cases and work your way from Rookie to Master Detective.

## Getting started

Make sure you have Python installed, then clone the repository:

```bash
git clone https://github.com/aztrax7/ai-crime-detective.git
cd ai-crime-detective
pip install scikit-learn pandas joblib
python main.py
```

The project includes a saved ML model. If it's missing, the game automatically generates a synthetic dataset and trains a new model.

You can also retrain it manually:

```bash
python ai/train_model.py
```

## How to play

Once you start the game, enter your detective name and you'll receive your first case.

| Command | What it does | Cost |
|---|---|---|
| `search` | Search for evidence | 3 |
| `evidence` | View discovered clues | Free |
| `analyze <number>` | Examine a clue | 1 |
| `suspects` | View the suspect list | Free |
| `profile <name>` | Check a suspect's profile | Free |
| `interview <name>` | Question a suspect | 2 |
| `ai` | Get AI guilt predictions | 2 |
| `accuse <name>` | Make your final accusation | Ends case |
| `help` | Show available commands | Free |
| `quit` | Exit the game | Free |

You start with **18 investigation points**. Use them wisely.

A correct accusation earns 500 points, with bonuses for analyzing evidence linked to the culprit and using the AI. A wrong accusation costs you 300 points.

## Project structure

```text
ai-crime-detective/
├── main.py           # Main game loop
├── game/             # Cases, suspects, evidence, gameplay
├── ai/               # Model training, predictions, dataset
├── data/             # JSON templates for generating cases
└── README.md
```

## About the AI

I used a **RandomForestClassifier** with 200 decision trees, trained on synthetic data with an 80/20 train-test split.

The model learns patterns between evidence features and whether a simulated suspect is guilty. It then uses those patterns to make predictions during gameplay.

One thing worth mentioning: this isn't an actual crime prediction system. The dataset is entirely simulated, and the model is designed for the game's fictional investigations.

Also, features you haven't uncovered yet currently default to zero. That's one of the limitations I want to improve.

## What's next?

A few things I'd like to add in future versions:

- A proper GUI instead of the terminal interface.
- A visual evidence board connecting suspects and clues.
- More interactive suspect interviews, possibly using an LLM.
- Better ML evaluation and explanations for AI predictions.
- Multiplayer investigations.

## Final note

This project was my attempt at combining two things I find interesting: building interactive software and understanding how machine learning can support decision-making.

It's still a work in progress, but building the game helped me explore how different parts of a Python application can work together, from generating cases to training and using an ML model.
