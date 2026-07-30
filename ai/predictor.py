import os
import pandas as pd
import joblib

from ai.train_model import train_and_save, FEATURES, MODEL_PATH


class GuiltPredictor:
    def __init__(self):
        if not os.path.exists(MODEL_PATH):
            train_and_save()
        self.model = joblib.load(MODEL_PATH)

    def predict_proba(self, feature_dict):
        """feature_dict must contain all keys in FEATURES.
        Returns probability (0-1) of guilt."""
        row = pd.DataFrame([{k: feature_dict.get(k, 0) for k in FEATURES}])
        proba = self.model.predict_proba(row)[0]
        classes = list(self.model.classes_)
        guilty_idx = classes.index(1) if 1 in classes else -1
        return float(proba[guilty_idx])

    def rank_suspects(self, suspects_known_features):
        """suspects_known_features: dict {suspect_name: feature_dict}
        (feature_dict should only include *revealed* features; missing
        ones default to 0, i.e. 'unknown counts as no evidence yet').
        Returns list of (name, probability) sorted descending."""
        results = []
        for name, feats in suspects_known_features.items():
            results.append((name, self.predict_proba(feats)))
        results.sort(key=lambda x: x[1], reverse=True)
        return results
