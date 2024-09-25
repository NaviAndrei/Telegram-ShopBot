<<<<<<< HEAD
import os
import logging
from logging.handlers import TimedRotatingFileHandler


def setup_logging(log_dir, log_filename):
    # Ensure log directory exists
    os.makedirs(log_dir, exist_ok=True)

    # Create logger
    app_logger = logging.getLogger()
    app_logger.setLevel(logging.DEBUG)

    # Formatter for log messages
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s - '
        '[in %(pathname)s:%(lineno)d] - [Process: %(process)d, Thread: %(thread)d]'
    )

    # Ensure log_dir and log_filename are explicitly typed as strings.
    # If they are not hardcoded strings, you might want to ensure their types at runtime.
    log_dir = str(log_dir)
    log_filename = str(log_filename)

    # Now construct the filename with os.path.join, which should not raise type hinting issues.
    filename = os.path.join(log_dir, log_filename)

    # Handler for logging to file with dynamic file naming
    file_handler = TimedRotatingFileHandler(
        filename=filename,
        when='midnight',
        interval=1,
        backupCount=7
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    app_logger.addHandler(file_handler)

    # Handler for logging to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    app_logger.addHandler(console_handler)

    return app_logger  # Return the logger object
=======
import os
import logging
from logging.handlers import TimedRotatingFileHandler


def setup_logging(log_dir, log_filename):
    # Ensure log directory exists
    os.makedirs(log_dir, exist_ok=True)

    # Create logger
    app_logger = logging.getLogger()
    app_logger.setLevel(logging.DEBUG)

    # Formatter for log messages
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s - '
        '[in %(pathname)s:%(lineno)d] - [Process: %(process)d, Thread: %(thread)d]'
    )

    # Ensure log_dir and log_filename are explicitly typed as strings.
    # If they are not hardcoded strings, you might want to ensure their types at runtime.
    log_dir = str(log_dir)
    log_filename = str(log_filename)

    # Now construct the filename with os.path.join, which should not raise type hinting issues.
    filename = os.path.join(log_dir, log_filename)

    # Handler for logging to file with dynamic file naming
    file_handler = TimedRotatingFileHandler(
        filename=filename,
        when='midnight',
        interval=1,
        backupCount=7
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    app_logger.addHandler(file_handler)

    # Handler for logging to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    app_logger.addHandler(console_handler)

    return app_logger  # Return the logger object
>>>>>>> bd5b9ce1bcd5d4b5aba4265e011c85a738c39520
