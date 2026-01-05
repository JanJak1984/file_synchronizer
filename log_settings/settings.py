""" Модуль настроек логера """

import logging.config
import os

path_logs = 'logs'
os.makedirs(path_logs, exist_ok=True)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standart": {
            "format": "%(asctime)s [%(levelname)s]: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standart",
            "level": "DEBUG",
        },
        "rotating_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standart",
            "filename": f"{path_logs}/logs.log",
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 3,  # хранить до 3 старых файлов
            "encoding": "utf-8",
            "level": "DEBUG",
        },
    },
    "root": {
        "handlers": ["console", "rotating_file"],
        "level": "DEBUG",
    },
}

logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger(__name__)
