import os
from os import devnull
import sys
from contextlib import contextmanager,redirect_stderr,redirect_stdout
import logging
import traceback

# Logging utils
def set_config(config, override_path):

    ENABLE_LOG_FILE = config['LOGGING']['ENABLE_LOG_FILE']
    print(f"ENABLE_LOG_FILE: {ENABLE_LOG_FILE}")

    LOG_FILE_PATH = None
    if override_path:
        LOG_FILE_PATH = override_path
    else:
        LOG_FILE_PATH = config['LOGGING']['LOG_FILE_PATH']
    print(f"LOG_FILE_PATH: {LOG_FILE_PATH}")

    LOGGING_LEVEL = config['LOGGING']['LOGGING_LEVEL']
    print(f"LOGGING_LEVEL: {LOGGING_LEVEL}")

    LOG_OVERWRITE = config['LOGGING']['LOG_OVERWRITE']
    print(f"LOG_OVERWRITE: {LOG_OVERWRITE}") 

    # This sets the root logger to write to stdout (console).
    # Your script/app needs to call this somewhere at least once.
    # Configure logging


    logging.basicConfig(handlers=[logging.FileHandler(LOG_FILE_PATH), logging.StreamHandler()], format='%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d %(message)s', level=LOGGING_LEVEL)

    # By default the root logger is set to WARNING and all loggers you define
    # inherit that value. Here we set the root logger to NOTSET. This logging
    # level is automatically inherited by all existing and new sub-loggers
    # that do not set a less verbose level.
    logging.root.setLevel(LOGGING_LEVEL)


@contextmanager
def suppress_stdout_stderr():
    """A context manager that redirects stdout and stderr to devnull"""
    with open(devnull, 'w') as fnull:
        with redirect_stderr(fnull) as err, redirect_stdout(fnull) as out:
            yield (err, out)


# Disable logging
def disable_logging():  
    # Disable logging  
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': True,
    })


# Restore logging
def enable_logging():
    # Re-enable logging
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
    })



