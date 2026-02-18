from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import tldextract
import json
import os

from feature_extraction import extract_features
from explain import explain_prediction

app = Flask(__name__)
CORS(app)

MODEL_PATH = "url_model.pkl"

HIGH_RISK_THRESHOLD = 0.75
SUSPICIOUS_THRESHOLD = 0.45

TRUSTED_DOMAINS = {
    "google.com",
    "amazon.com",
    "amazon.in",
    "github.com",
    "kaggle.com",
    "microsoft.com",
    "steampowered.com"
}


HARD_TRUST_TLDS = {"gov", "gov.in", "edu", "edu.in", "ac.in"}
HARD_TRUST_CAP = 0.25
TRUST_REDUCTION_FACTOR = 0.4

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)


def get_root_domain(url):
    extracted = tldextract.extract(url)
    return f"{extracted.domain}.{extracted.suffix}", extracted.suffix

def smooth_risk(prob):
    # Clamp extreme confidence
    if prob < 0.05:
        return 0.05
    if prob > 0.95:
        return 0.95
    return prob

@app.route("/check_url", methods=["POST"])
def check_url():
    data = request.json
    url = data.get("url")

    # Feature extraction
    features = extract_features(url)
    df = pd.DataFrame([features])
    reasons = explain_prediction(features)

    # Base ML score (smoothed)
    phishing_prob = smooth_risk(model.predict_proba(df)[0][1])

    # Domain & TLD
    root_domain, tld = get_root_domain(url)
    dynamic_trusted = load_trusted_domains()
    trusted = root_domain in TRUSTED_DOMAINS or root_domain in dynamic_trusted


    # Trust-based adjustments
    if trusted:
        phishing_prob *= TRUST_REDUCTION_FACTOR

    if tld in HARD_TRUST_TLDS:
        phishing_prob = min(phishing_prob, HARD_TRUST_CAP)

    # ✅ FINAL DECISION LOGIC (CORRECT)
    if phishing_prob >= HIGH_RISK_THRESHOLD:
       label = "PHISHING"
    elif phishing_prob >= SUSPICIOUS_THRESHOLD:
       label = "SUSPICIOUS"
    elif phishing_prob >= 0.30:
       label = "LIKELY SAFE"
    else:
       label = "LEGITIMATE"


    return jsonify({
        "url": url,
        "domain": root_domain,
        "risk_score": round(phishing_prob * 100, 2),
        "label": label,
        "reasons": reasons
    })

@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.json
    domain = data.get("domain")
    action = data.get("action")
    label = data.get("label")  # extension must send this

    # Only allow marking safe if NOT phishing
    if action == "mark_safe" and domain and label == "SUSPICIOUS":
        save_trusted_domain(domain)
        return jsonify({
            "status": "success",
            "message": f"{domain} added as trusted"
        })

    return jsonify({"status": "ignored"})



TRUST_FILE = "trusted_domains.json"

def load_trusted_domains():
    if not os.path.exists(TRUST_FILE):
        return set()

    try:
        with open(TRUST_FILE, "r") as f:
            data = json.load(f)
        return set(data.get("domains", []))
    except (json.JSONDecodeError, ValueError):
        # corrupted or empty file
        return set()



def save_trusted_domain(domain):
    domains = load_trusted_domains()
    domains.add(domain)
    with open(TRUST_FILE, "w") as f:
        json.dump({"domains": list(domains)}, f, indent=2)



if __name__ == "__main__":
    app.run(debug=True)
