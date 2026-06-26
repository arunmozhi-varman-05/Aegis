from abc import ABC, abstractmethod

class BasePredictor(ABC):
    """Abstract base class for future Machine Learning models."""
    @abstractmethod
    def predict_risk(self, features: dict) -> float:
        pass

class BaseContentAnalyzer(ABC):
    """Abstract base class for future Page Content Analysis."""
    @abstractmethod
    def analyze_content(self, html: str) -> dict:
        pass

class BaseReputationAPI(ABC):
    """Abstract base class for future external Blacklist APIs (e.g. Safe Browsing)."""
    @abstractmethod
    def check_reputation(self, url: str) -> dict:
        pass
