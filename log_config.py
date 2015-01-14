__author__ = 'e.kolpakov'

log_config = {
    "version": 1,
    "formatters": {
        "trace": {
            "format": "%(asctime)s [%(levelname) -8s] at %(module) -15s(%(lineno) -4d): %(message)s"
        },
        "output": {
            "format": "%(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "output",
            "level": "INFO",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "utils.make_file_logger.MakeFileHandler",
            "formatter": "trace",
            "filename": "../log/trace.log",
            "maxBytes": 102400,
            "backupCount": 2
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["file", "console"]
    }
}