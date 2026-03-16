import logging
import sys
from pathlib import Path
from typing import Optional
from .config import settings


class LoggerSetup:
    @staticmethod
    def setup_logger(name: str, level: Optional[str] = None, log_file: Optional[Path] = None) -> logging.Logger:
        """"
            args: name: logger name,
                  level: Debug, Error, Info etc
        """
        logger = logging.getLogger(name)
        log_level = level or settings.log_level
        logger.setLevel(getattr(logging, log_level.upper()))
        if logger.handlers:
            return logger
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        if log_file:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger


logger = LoggerSetup.setup_logger("boilerplate")
