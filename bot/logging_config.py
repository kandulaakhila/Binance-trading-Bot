import logging
import os

def setup_logger():
    """
    Configures the universal logging system for the trading bot.

    This function sets up a root logger that securely captures application events,
    API interactions, and exceptions. It dynamically creates a `logs/` directory 
    if one doesn't exist and attaches two handlers:
      1. FileHandler: Persists all logs to `logs/trading_bot.log` for auditing.
      2. StreamHandler: Outputs logs directly to the user's terminal (console).
      
    Returns:
        logging.Logger: The configured, ready-to-use root logger object.
    """
    
    # Ensure the logs directory exists
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    # Standardized format
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(log_format)

    # File handler: captures everything for auditing
    file_handler = logging.FileHandler(f"{log_dir}/trading_bot.log", mode="a")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Console handler: shows info + warnings/errors in real time
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Root logger setup
    logger = logging.getLogger("binance_bot")
    logger.setLevel(logging.DEBUG)
 # Prevent duplicate handlers
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

# Expose a pre-configured logger instance
logger = setup_logger()
