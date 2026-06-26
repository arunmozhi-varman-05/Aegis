import pickle
import pandas as pd
# pyrefly: ignore [missing-import]
import tldextract
from feature_extraction import extract_features

from backend.predictor import RandomForestPredictor

MODEL_PATH = "url_model.pkl"

predictor = RandomForestPredictor(MODEL_PATH)

urls_to_test = [
    "google.com",
    "paypal-secure-login-123.com",
    "github.com",
    "login.update-apple-security.com"
]

for url in urls_to_test:
    features = extract_features(url)
    phishing_prob = predictor.predict_risk(features)
    print(f"URL: {url} -> Phishing Prob: {phishing_prob:.4f}")
