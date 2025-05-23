import logging

def setup_logger(name, level):
    """
        level: DEBUG, INFO, WARNING, ERROR, CRITICAL
        logging.Logger: configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level))
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger