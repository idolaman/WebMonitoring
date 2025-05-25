import sys
import logging

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

_logging_initialized = False

def init_logging() -> None:
    """Initialize minimal logging with console output."""
    global _logging_initialized
    
    if not _logging_initialized:
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        
        for handler in list(root_logger.handlers):
            root_logger.removeHandler(handler)
        
        console_handler = logging.StreamHandler(stream=sys.stdout)
        formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
        
        _logging_initialized = True

def get_logger(name: str) -> logging.Logger:
    """Get a logger with the specified name."""
    if not _logging_initialized:
        init_logging()
    
    return logging.getLogger(name) 