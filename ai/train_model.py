"""
Generates a synthetic dataset of past 'solved cases' and trains a
RandomForestClassifier to predict probability of guilt from evidence features.

Run directly to (re)generate dataset.csv and model.pkl:
    python ai/train_model.py
"""

import os
import random

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

AI_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(AI_DIR, "dataset.csv")
MODEL_PATH = os.path.join(AI_DIR, "model.pkl")

FEATURES = [
    "fingerprint",
    "dna_match",
    "motive_strength",
    "witness_identification",
    "suspicious_behavior",
    "false_alibi",
    "digital_evidence",
]


def _generate_row():
    """Simulates one suspect from one historical case, using the same
    generative logic as the live game (Suspect.feature_vector), so the
    model's learned boundary matches what it will see in play."""
    guilty = 1 if random.random() < 0.35 else 0  # ~35% of suspects in history were guilty

    def roll(p_guilty, p_innocent):
        p = p_guilty if guilty else p_innocent
        return 1 if random.random() < p else 0

    fingerprint = roll(0.75, 0.15)
    dna_match = 1 if (fingerprint and random.random() < 0.5) else 0
    motive_strength = random.choices([0, 1, 2], weights=[0.10, 0.30, 0.60] if guilty else [0.60, 0.30, 0.10])[0]
    witness_identification = roll(0.55, 0.15)
    suspicious_behavior = roll(0.70, 0.20)
    false_alibi = roll(0.70, 0.20)
    digital_evidence = roll(0.55, 0.15)

    return {
        "fingerprint": fingerprint,
        "dna_match": dna_match,
        "motive_strength": motive_strength,
        "witness_identification": witness_identification,
        "suspicious_behavior": suspicious_behavior,
        "false_alibi": false_alibi,
        "digital_evidence": digital_evidence,
        "guilty": guilty,
    }


def generate_dataset(n_rows=1000, seed=None):
    if seed is not None:
        random.seed(seed)
    rows = [_generate_row() for _ in range(n_rows)]
    return pd.DataFrame(rows)


def train_and_save(n_rows=1000, seed=42):
    df = generate_dataset(n_rows=n_rows, seed=seed)
    df.to_csv(DATASET_PATH, index=False)

    X = df[FEATURES]
    y = df["guilty"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=seed)

    model = RandomForestClassifier(n_estimators=200, max_depth=6, random_state=seed)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    joblib.dump(model, MODEL_PATH)
    return acc


if __name__ == "__main__":
    accuracy = train_and_save()
    print(f"Model trained. Test accuracy: {accuracy:.2%}")
    print(f"Saved dataset -> {DATASET_PATH}")
    print(f"Saved model   -> {MODEL_PATH}")
