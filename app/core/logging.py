import logging
import os
from logging.config import dictConfig

_DEFAULT_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

def configure_logging() -> None:
    dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s %(levelname)s [%(name)s] %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": _DEFAULT_LEVEL,
            }
        },
        "root": {
            "handlers": ["console"],
            "level": _DEFAULT_LEVEL,
        },
    })

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
