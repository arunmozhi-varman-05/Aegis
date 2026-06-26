import pickle
import sys
import os

# Ensure the root directory is accessible so we can import feature_extraction
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# (No longer need feature_extraction here since features are passed in)
from backend.interfaces import BasePredictor
import pandas as pd

HIGH_RISK_THRESHOLD = 0.75
SUSPICIOUS_THRESHOLD = 0.45

TRUSTED_DOMAINS = {
    "google.com", "amazon.com", "amazon.in", "github.com",
    "kaggle.com", "microsoft.com", "steampowered.com", "youtube.com",
    "linkedin.com", "wikipedia.org", "chatgpt.com", "openai.com",
    "apple.com", "facebook.com"
}
HARD_TRUST_TLDS = {"gov", "gov.in", "edu", "edu.in", "ac.in"}
HARD_TRUST_CAP = 0.25
TRUST_REDUCTION_FACTOR = 0.4

class RandomForestPredictor(BasePredictor):
    def __init__(self, model_path="url_model.pkl"):
        # Go up one directory to find the model if running from backend/
        root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        full_model_path = os.path.join(root_path, model_path)
        try:
            with open(full_model_path, "rb") as f:
                self.model = pickle.load(f)
        except Exception as e:
            print(f"Failed to load model: {e}")
            self.model = None

    def predict_risk(self, features: dict) -> float:
        """Predicts the phishing probability (0.0 to 1.0)."""
        if not self.model:
            return 0.5 # Default middle-ground if model fails

        df = pd.DataFrame([features])
        probs = self.model.predict_proba(df)[0]
        classes = list(self.model.classes_)
        raw_phish_prob = 0.0
        if '1' in classes:
            raw_phish_prob += probs[classes.index('1')]
        if 'phishing' in classes:
            raw_phish_prob += probs[classes.index('phishing')]
        
        return raw_phish_prob
