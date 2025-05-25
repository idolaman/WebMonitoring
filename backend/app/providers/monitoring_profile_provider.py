import json
from pathlib import Path
from ..logging_config import get_logger

logger = get_logger(__name__)

class MonitoringProfileProvider:
    """Provider for monitoring profile data loaded from JSON file."""
    
    def __init__(self, profile_file: str = "monitoring_profile.json"):
        self.profile_file = Path(profile_file)
    
    def load_profile(self):
        """Load monitoring profile from JSON file."""
        try:
            if not self.profile_file.exists():
                logger.warning(f"Profile file {self.profile_file} not found, using default configuration")
                return {
                    "domains": [],
                    "rules": []
                }
            
            with open(self.profile_file, 'r') as f:
                profile = json.load(f)
                logger.info(f"Successfully loaded monitoring profile from {self.profile_file}")
                return profile
        except Exception as e:
            logger.error(f"Error loading profile file {self.profile_file}: {e}, using default configuration")
            return {
                "domains": [],
                "rules": []
            } 