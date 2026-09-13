import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path


# ============================================================
# PROJECT ROOT
# ============================================================

ROOT_DIR = Path(__file__).resolve().parents[2]


# ============================================================
# LOG CONFIGURATION
# ============================================================

LOG_DIR = ROOT_DIR / "logs"

LOG_FILE = (
    datetime.now().strftime(
        "%m_%d_%Y_%H_%M_%S"
    )
    + ".log"
)

LOG_FILE_PATH = LOG_DIR / LOG_FILE

MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB

BACKUP_COUNT = 3


# ============================================================
# CREATE LOG DIRECTORY
# ============================================================

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# LOGGER CONFIGURATION
# ============================================================

def configure_logger():

    logger = logging.getLogger("AI-Banking-Agent")

    logger.setLevel(
        logging.DEBUG
    )

    logger.propagate = False


    # Prevent duplicate handlers
    if logger.handlers:
        return logger


    # ========================================================
    # FORMAT
    # ========================================================

    formatter = logging.Formatter(
        "[%(asctime)s] "
        "%(name)s - "
        "%(levelname)s - "
        "%(message)s"
    )


    # ========================================================
    # FILE HANDLER
    # ========================================================

    file_handler = RotatingFileHandler(
        filename=LOG_FILE_PATH,
        maxBytes=MAX_LOG_SIZE,
        backupCount=BACKUP_COUNT,
        encoding="utf-8"
    )

    file_handler.setLevel(
        logging.DEBUG
    )

    file_handler.setFormatter(
        formatter
    )


    # ========================================================
    # CONSOLE HANDLER
    # ========================================================

    console_handler = logging.StreamHandler()

    console_handler.setLevel(
        logging.INFO
    )

    console_handler.setFormatter(
        formatter
    )


    # ========================================================
    # REGISTER HANDLERS
    # ========================================================

    logger.addHandler(
        file_handler
    )

    logger.addHandler(
        console_handler
    )


    return logger


# ============================================================
# GLOBAL LOGGER
# ============================================================

logger = configure_logger()
