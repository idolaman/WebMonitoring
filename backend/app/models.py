from pydantic import BaseModel
from typing import Dict, List

class RequestData(BaseModel):
    """Model for incoming request data."""
    url: str
    method: str
    headers: Dict[str, str]
    timestamp: str

class RequestResponse(BaseModel):
    """Model for request response."""
    status: str

class Rule(BaseModel):
    """Base model for rule configuration."""
    name: str
    type: str
    severity: str

class UrlRegexRule(Rule):
    """Model for URL regex rule configuration."""
    pattern: str 