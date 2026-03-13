import re
import math
import tldextract
from urllib.parse import urlparse


# ==============================
# Suspicious keyword lists
# ==============================
PHISHING_KEYWORDS = [
    "login", "verify", "account", "secure", "update",
    "bank", "support", "help", "signin", "password"
]

BRAND_KEYWORDS = [
    "paypal", "amazon", "google", "apple",
    "facebook", "microsoft", "netflix", "bank"
]


# ==============================
# Entropy calculation
# ==============================
def calculate_entropy(text):
    if not text:
        return 0
    probabilities = [text.count(c) / len(text) for c in set(text)]
    entropy = -sum(p * math.log2(p) for p in probabilities)
    return entropy


# ==============================
# Feature Extraction
# =============================
def extract_features(url):
    try:
        features = {
            "url_length": len(url),
            "num_dots": url.count('.'),
            "has_https": int('https' in url),
            "has_at": int('@' in url),
            "has_dash": int('-' in url)
        }

        return features

    except:
        return {
            "url_length": 0,
            "num_dots": 0,
            "has_https": 0,
            "has_at": 0,
            "has_dash": 0
        }