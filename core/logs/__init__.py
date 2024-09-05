import logging, os, sys
from logging.handlers import TimedRotatingFileHandler

log_dir_path = "log"

if not os.path.exists(log_dir_path):
    os.makedirs(log_dir_path)

log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
log_file = os.path.join(log_dir_path, "backend.log")

file_handler = TimedRotatingFileHandler(
    log_file, when="midnight", interval=1, backupCount=7, encoding="utf-8"
)
file_handler.setFormatter(log_formatter)


error_file_handler = TimedRotatingFileHandler(
    log_file, when="midnight", interval=1, backupCount=7, encoding="utf-8"
)
error_file_handler.setLevel(logging.ERROR)
error_file_handler.setFormatter(log_formatter)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(log_formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.addHandler(error_file_handler)


def LOG_ERROR(text, e=None):
    if not e == None:
        logger.error(f"{text} {e}")
    else:
        logger.error(f"{text} ")


def LOG_INFO(text, e=None):
    if not e == None:
        logger.info(f"{text} {e}")
    else:
        logger.info(f"{text} ")