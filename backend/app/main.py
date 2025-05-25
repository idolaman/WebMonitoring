from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from cachetools import cached, TTLCache

from .models import RequestData, RequestResponse
from .providers.monitoring_profile_provider import MonitoringProfileProvider
from .services.alert_service import log_alert
from .services.rules_engine import create_rule_from_dict, RulesEngine
from .logging_config import get_logger, init_logging

# Initialize logging
init_logging()
logger = get_logger(__name__)

# Create profile provider
profile_provider = MonitoringProfileProvider()

# Create a global rules engine instance
rules_engine = RulesEngine()

# Create cached version of load_profile with 1 minute TTL
@cached(cache=TTLCache(maxsize=1, ttl=60))
def load_profile():
    return profile_provider.load_profile()

app = FastAPI(title="Request Monitoring API")

# Log application startup
logger.info("Starting Request Monitoring API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def process_request_async(request_data: RequestData):
    """Process the request in the background."""
    logger.info(f"Processing request: {request_data.method} {request_data.url}")
    
    # Get current monitoring profile
    profile = load_profile()
    
    # Create rule objects from profile data
    rules = [create_rule_from_dict(r) for r in profile["rules"]]
    logger.info(f"Loaded {len(rules)} rules for processing")
    
    # Execute rules against request data
    alerts = rules_engine.execute_rules(request_data, rules)
    
    # If there are alerts, log them
    if alerts:
        logger.info(f"Generated {len(alerts)} alerts for request {request_data.url}")
        log_alert(request_data, alerts)
    else:
        logger.info(f"No alerts generated for request {request_data.url}")

@app.get("/api/v1/config")
async def get_config():
    """Get the monitoring profile including domains to watch."""
    try:
        profile = load_profile()
        return profile["domains"]
    except Exception as e:
        logger.error(f"Error getting config: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/v1/requests", response_model=RequestResponse)
async def ingest_request(request_data: RequestData, background_tasks: BackgroundTasks):
    """Ingest a request for monitoring and analysis."""
    try:
        logger.info(f"Received request for monitoring: {request_data.method} {request_data.url}")
        background_tasks.add_task(process_request_async, request_data)
        
        return RequestResponse(
            status="accepted"
        )
    except Exception as e:
        logger.error(f"Error ingesting request: {e}")
        raise HTTPException(status_code=500, detail="Internal server error") 