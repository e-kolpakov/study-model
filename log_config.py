__author__ = 'john'

config = {
    "version" : 1,
    "formatters": {
        "trace": {
            "format": "%(asctime)s [%(levelname) -8s] at %(module)s(%(lineno)d): %(message)s"
        },
        "output":{
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
            "filename": "log/trace.log",
            "maxBytes": 10240,
            "backupCount": 2
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["file", "console"]
    }
}