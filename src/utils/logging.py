from loguru import logger


def setup_logger():
    logger.add("logs/logs.log", format="{time} {level} {message}", rotation="10:00", compression="zip")
