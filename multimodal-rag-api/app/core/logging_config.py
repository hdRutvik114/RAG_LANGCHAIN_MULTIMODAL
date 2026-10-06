import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


class AppLogger:
    """Configure a single application logger for console and file output."""

    _logger_name = "app"
    _configured = False

    @classmethod
    def configure(cls, log_file: str, level: int = logging.INFO) -> logging.Logger:
        """Set up the app logger once and return it."""
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        logger = logging.getLogger(cls._logger_name)
        logger.setLevel(level)
        logger.propagate = False

        if cls._configured and logger.handlers:
            return logger

        for handler in list(logger.handlers):
            logger.removeHandler(handler)
            handler.close()

        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

        file_handler = RotatingFileHandler(
            str(log_path),
            maxBytes=5 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8",
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        cls._configured = True
        return logger

    @classmethod
    def get_logger(cls) -> logging.Logger:
        return logging.getLogger(cls._logger_name)


def configure_logging(log_file: str, level: int = logging.INFO) -> logging.Logger:
    """Backward-compatible wrapper for the class-based configuration."""
    return AppLogger.configure(log_file, level)


__all__ = ["AppLogger", "configure_logging"]
