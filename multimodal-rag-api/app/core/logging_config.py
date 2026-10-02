import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def configure_logging(log_file: str, level: int = logging.INFO):
    """Configure root logger to write to a rotating file and console.

    Creates the parent directory for `log_file` if it doesn't exist.
    """
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(level)

    # avoid adding multiple handlers if called more than once
    if any(isinstance(h, RotatingFileHandler) and h.baseFilename == str(log_path) for h in logger.handlers if hasattr(h, "baseFilename")):
        return

    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    fh = RotatingFileHandler(str(log_path), maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8")
    fh.setLevel(level)
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(fmt)
    logger.addHandler(ch)


__all__ = ["configure_logging"]
