import logging
from datetime import datetime
from pathlib import Path

def setup_logger(name="bronze_pipeline"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if logger.handlers:
        return logger
    log_dir = Path(__file__).resolve().parent.parent.parent / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"ingestion_{datetime.now().strftime('%Y-%m-%d')}.log"
    fmt = logging.Formatter("[%(asctime)s] %(levelname)-5s | %(message)s", "%Y-%m-%d %H:%M:%S")
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(fmt)
    file = logging.FileHandler(log_file, encoding="utf-8")
    file.setLevel(logging.DEBUG)
    file.setFormatter(fmt)
    logger.addHandler(console)
    logger.addHandler(file)
    return logger
