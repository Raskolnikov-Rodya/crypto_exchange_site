from slowapi import Limiter
from slowapi.util import get_remote_address

# Allow max 5 requests per minute per user
limiter = Limiter(key_func=get_remote_address, default_limits=["5 per minute"])
