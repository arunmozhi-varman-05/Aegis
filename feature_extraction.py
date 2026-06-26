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

IP_PATTERN = re.compile(r'^(?:\d{1,3}\.){3}\d{1,3}$')


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
# ==============================
def extract_features(url):
    try:
        url_lower = url.lower()

        # Make sure urlparse can find a netloc even if scheme is missing
        parse_target = url if "://" in url else f"http://{url}"
        host = urlparse(parse_target).netloc.split(":")[0]

        extracted = tldextract.extract(url)
        root_domain = extracted.domain.lower()

        features = {
            "url_length": len(url),
            "num_dots": url.count('.'),
            "https": int(url_lower.startswith("https")),
            "has_at": int('@' in url),
            "hyphen_count": url.count('-'),
            "has_ip": int(bool(IP_PATTERN.match(host))),
            "phishing_keyword_count": sum(1 for kw in PHISHING_KEYWORDS if kw in url_lower),
            # Flag brand impersonation: brand name appears in the URL
            # but isn't actually the registered root domain (e.g. paypal-secure.com)
            "brand_keyword": int(any(
                brand in url_lower and brand != root_domain
                for brand in BRAND_KEYWORDS
            )),
            "url_entropy": round(calculate_entropy(url), 4)
        }

        return features

    except Exception as e:
        return {
            "url_length": 0,
            "num_dots": 0,
            "https": 0,
            "has_at": 0,
            "hyphen_count": 0,
            "has_ip": 0,
            "phishing_keyword_count": 0,
            "brand_keyword": 0,
            "url_entropy": 0
        }
