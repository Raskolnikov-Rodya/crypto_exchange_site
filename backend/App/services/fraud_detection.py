from app.core.logger import log_action

def detect_suspicious_activity(user_id: int, transaction_type: str, amount: float):
    """Detect unusual trading or withdrawal behavior."""
    if amount > 100000:  # Example: Flag transactions over $100K
        log_action("Suspicious Transaction Detected", user_id, {"type": transaction_type, "amount": amount})
        return True
    return False
