# utils/nhat_ky.py
import logging
from utils.cau_hinh import RESET, RED

logging.basicConfig(
    level=logging.INFO,
    format=f"{RED}[%(asctime)s]{RESET} - [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger("Rin")

def log_error(message, detail=None):
    logger.error(message)
    if detail:
        logger.error(detail)

def log_info(message, detail=None):
    logger.info(message)
    if detail:
        logger.info(detail)

def log_debug(message, detail=None):
    logger.debug(message)
    if detail:
        logger.debug(detail)