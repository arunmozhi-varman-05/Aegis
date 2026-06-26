from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import tldextract
import json
import os
import whois
import datetime
import requests
import sqlite3
import redis

from feature_extraction import extract_features
from explain import explain_prediction

app = Flask(__name__)
CORS(app)

DB_PATH = "aegis.db"

# ==========================================
# Caching Setup (Redis)
# ==========================================
redis_client = None
try:
    # Use 'redis' for Docker, 'localhost' for local fallback
    redis_host = os.environ.get("REDIS_HOST", "localhost")
    redis_client = redis.Redis(host=redis_host, port=6379, db=0, decode_responses=True, socket_connect_timeout=1)
    redis_client.ping()
    print(f"✅ Redis Cache Connected at {redis_host}")
except Exception:
    print("⚠️ Redis not available. Running without cache.")
    redis_client = None

# ==========================================
# Database Setup (SQLite)
# ==========================================
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trusted_domains (
            domain TEXT PRIMARY KEY
        )
    ''')
    conn.commit()
    conn.close()

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
    "steampowered.com",
    "youtube.com",
    "linkedin.com",
    "wikipedia.org"
}


HARD_TRUST_TLDS = {"gov", "gov.in", "edu", "edu.in", "ac.in"}
HARD_TRUST_CAP = 0.25
TRUST_REDUCTION_FACTOR = 0.4

SAFE_BROWSING_API_KEY = "YOUR_API_KEY_HERE"

def get_domain_age_days(domain):
    try:
        w = whois.whois(domain)
        creation_date = w.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if creation_date:
            age = (datetime.datetime.now() - creation_date).days
            return age
    except Exception:
        pass
    return None

def check_google_safe_browsing(url):
    if SAFE_BROWSING_API_KEY == "YOUR_API_KEY_HERE":
        return False
    
    api_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={SAFE_BROWSING_API_KEY}"
    payload = {
        "client": {"clientId": "aegis", "clientVersion": "1.0.0"},
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }
    try:
        response = requests.post(api_url, json=payload, timeout=3)
        if response.status_code == 200:
            data = response.json()
            if "matches" in data and len(data["matches"]) > 0:
                return True
    except Exception:
        pass
    return False

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

    # Redis Cache Check
    if redis_client:
        try:
            cached_result = redis_client.get(f"url:{url}")
            if cached_result:
                print(f"⚡ CACHE HIT: {url}")
                return jsonify(json.loads(cached_result))
        except Exception:
            pass

    # Feature extraction
    features = extract_features(url)
    df = pd.DataFrame([features])
    
    # Real-time checks
    root_domain, tld = get_root_domain(url)
    domain_age = get_domain_age_days(root_domain)
    is_safe_browsing_flagged = check_google_safe_browsing(url)
    
    reasons = explain_prediction(features, domain_age, is_safe_browsing_flagged)

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
        
    # WHOIS and Safe Browsing adjustments
    if domain_age is not None and domain_age < 30:
        phishing_prob = max(phishing_prob, 0.85)  # Boost risk for new domains
        
    if is_safe_browsing_flagged:
        phishing_prob = 0.99  # Definite phishing if flagged by Google

    # ✅ FINAL DECISION LOGIC (CORRECT)
    if phishing_prob >= HIGH_RISK_THRESHOLD:
       label = "PHISHING"
    elif phishing_prob >= SUSPICIOUS_THRESHOLD:
       label = "SUSPICIOUS"
    elif phishing_prob >= 0.30:
       label = "LIKELY SAFE"
    else:
       label = "LEGITIMATE"

    response_data = {
        "url": url,
        "domain": root_domain,
        "risk_score": round(phishing_prob * 100, 2),
        "label": label,
        "reasons": reasons
    }
    
    # Save to Redis Cache (24 hours = 86400 seconds)
    if redis_client:
        try:
            redis_client.setex(f"url:{url}", 86400, json.dumps(response_data))
        except Exception:
            pass

    return jsonify(response_data)

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



def load_trusted_domains():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT domain FROM trusted_domains")
        domains = {row[0] for row in cursor.fetchall()}
        conn.close()
        return domains
    except Exception:
        return set()

def save_trusted_domain(domain):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO trusted_domains (domain) VALUES (?)", (domain,))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"DB Error: {e}")



if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0")
