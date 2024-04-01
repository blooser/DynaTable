import logging


def get_logger(name: str) -> logging.Logger:
    """
    Creates and returns a logger with the specified name.

    The logger is configured to output logs in a format that includes
    the log level, date and time, logger's name, and the log message.
    By default, logs are output to standard output (console).

    Args:
        name (str): The name of the logger to be used for identification.

    Returns:
        logging.Logger: A configured logger object.

    Example:
        my_logger = get_logger('myLogger')
        my_logger.info('This is a test message')
    """

    logger = logging.getLogger(name)

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(levelname)s %(asctime)s %(name)s: %(message)s")

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger
