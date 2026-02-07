import logging

from logging.handlers import RotatingFileHandler

from src.utilities.current_path_provider import set_project_path

project_path = set_project_path()


def get_logger() -> logging.Logger | None:
    log_path = project_path.joinpath("logs")
    log_path.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("ChronaLogger")
    logger.setLevel(logging.WARNING)
    if not logger.hasHandlers():
        handler = RotatingFileHandler(log_path.joinpath("chrona.log"), maxBytes=5 * 1024 * 1024, backupCount=5)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s - %(funcName)s - %(lineno)d",
            datefmt="%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger