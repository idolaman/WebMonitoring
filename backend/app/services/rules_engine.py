import re
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Union, Type
from ..models import RequestData, Rule, UrlRegexRule
from ..logging_config import get_logger

logger = get_logger(__name__)

class RuleHandler(ABC):
    """Abstract base class for rule handlers."""
    
    @staticmethod
    @abstractmethod
    def execute(request_data: RequestData, rule: Rule) -> Optional[Dict[str, str]]:
        """Execute a rule against request data."""
        pass

class UrlRegexHandler(RuleHandler):
    """Static handler for URL regex rules."""
    
    @staticmethod
    def execute(request_data: RequestData, rule: Rule) -> Optional[Dict[str, str]]:
        """Execute URL regex rule against request URL."""
        if not isinstance(rule, UrlRegexRule):
            raise ValueError(f"UrlRegexHandler expects UrlRegexRule, got {type(rule)}")
        
        if re.search(rule.pattern, request_data.url, re.IGNORECASE):
            logger.info(f"Rule '{rule.name}' matched URL: {request_data.url}")
            return {
                "name": rule.name,
                "type": rule.type,
                "severity": rule.severity,
                "pattern": rule.pattern,
                "matched_url": request_data.url
            }
        return None

RULE_TYPE_REGISTRY: Dict[str, Type[Rule]] = {
    "url-regex": UrlRegexRule,
}

def create_rule_from_dict(rule_data: Dict) -> Rule:
    """Factory function to create appropriate rule type from dictionary."""
    rule_type = rule_data.get("type")
    
    rule_class = RULE_TYPE_REGISTRY.get(rule_type, Rule)
    
    return rule_class(**rule_data)

class RulesEngine:
    """Engine for executing monitoring rules."""
    
    def __init__(self):
        self.handlers = {
            "url-regex": UrlRegexHandler
        }
    
    def execute_rules(self, request_data: RequestData, rules: List[Rule]) -> List[Dict[str, str]]:
        """Execute all rules against request data."""
        logger.info(f"Executing {len(rules)} rules against request: {request_data.url}")
        alerts = []
        
        for rule in rules:
            handler_class = self.handlers.get(rule.type)
            if handler_class is None:
                logger.warning(f"No handler found for rule type '{rule.type}', skipping rule '{rule.name}'")
                continue
            
            alert = handler_class.execute(request_data, rule)
            if alert:
                alerts.append(alert)
        
        logger.info(f"Rules execution completed: {len(alerts)} alerts generated")
        return alerts 