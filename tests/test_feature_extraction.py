import pytest
import sys
import os

# Add parent directory to path so we can import feature_extraction
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from feature_extraction import extract_features

def test_extract_features_safe_url():
    url = "https://www.google.com"
    features = extract_features(url)
    
    assert features["https"] == 1
    assert features["has_at"] == 0
    assert features["has_ip"] == 0
    assert features["phishing_keyword_count"] == 0
    assert features["brand_keyword"] == 0
    # google.com has 2 dots (www.google.com)
    assert features["num_dots"] == 2

def test_extract_features_phishing_url():
    url = "http://192.168.1.1/login@secure-update-paypal.com"
    features = extract_features(url)
    
    assert features["https"] == 0
    assert features["has_at"] == 1
    assert features["has_ip"] == 1
    # secure, update, login
    assert features["phishing_keyword_count"] >= 3
    # paypal
    assert features["brand_keyword"] >= 1
    assert features["hyphen_count"] >= 2

def test_extract_features_entropy():
    url_normal = "https://example.com"
    url_random = "https://example.com/a8b9c0d1e2f3g4h5i6j7k8l9m0n"
    
    features_normal = extract_features(url_normal)
    features_random = extract_features(url_random)
    
    assert features_random["url_entropy"] > features_normal["url_entropy"]
