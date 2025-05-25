import json
from datetime import datetime, timezone
from typing import List, Dict
from ..models import RequestData
from ..config import ALERTS_DIR
from ..logging_config import get_logger

logger = get_logger(__name__)

def log_alert(request_data: RequestData, alerts: List[Dict[str, str]]):
    """Log alerts to a file."""
    alert_data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "request": {
            "url": request_data.url,
            "method": request_data.method,
            "headers": request_data.headers,
            "request_timestamp": request_data.timestamp
        },
        "alerts": alerts
    }
    
    try:
        filename = ALERTS_DIR / f"alerts_{datetime.now(timezone.utc).strftime('%Y%m%d')}.jsonl"
        
        with open(filename, "a") as f:
            f.write(json.dumps(alert_data) + "\n")
        
        logger.info(f"Successfully logged {len(alerts)} alerts to {filename}")
        
    except Exception as e:
        logger.error(f"Failed to log alerts to file: {e}") 