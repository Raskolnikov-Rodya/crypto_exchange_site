from loguru import logger
import sys

logger.remove()

# Remove default logger
logger.remove()

# Configure logging
logger.add(
    sys.stdout, 
    format="{time} {level} {message}", 
    level="INFO"
)

logger.add(
    "logs/app.log", 
    rotation="1 day",  # Creates a new log file every day
    level="INFO"
)

def log_action(action: str, user_id: int = None, details: dict = None):
    """Logs important actions for tracking."""
    logger.info(f"Action: {action}, User: {user_id}, Details: {details}")