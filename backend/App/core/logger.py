import logging
import os
from typing import Any

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("crypto_exchange")
if not logger.handlers:
    logger.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)

    file_handler = logging.FileHandler(os.path.join(LOG_DIR, "app.log"))
    file_handler.setLevel(logging.INFO)

    fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    stream_handler.setFormatter(fmt)
    file_handler.setFormatter(fmt)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)


def log_action(action: str, user_id: int | None = None, details: dict[str, Any] | None = None) -> None:
    logger.info("Action=%s User=%s Details=%s", action, user_id, details)
