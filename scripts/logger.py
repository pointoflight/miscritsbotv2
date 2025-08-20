import logging
import os
from datetime import datetime
import pytz

def setup_logger():
    # Create logs directory if it doesn’t exist
    os.makedirs("logs", exist_ok=True)

    # File name with IST timestamp
    ist = pytz.timezone("Asia/Kolkata")
    timestamp = datetime.now(ist).strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = f"logs/run_{timestamp}.log"

    # Logger instance
    logger = logging.getLogger("miscrits_logger")
    logger.setLevel(logging.INFO)

    # --- File handler (detailed with timestamp) ---
    file_handler = logging.FileHandler(log_filename, encoding="utf-8")
    file_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s",
                                       datefmt="%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(file_formatter)

    # --- Console handler (simple, no timestamps) ---
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter("%(message)s")
    console_handler.setFormatter(console_formatter)

    # Attach both handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger