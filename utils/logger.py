import logging

def get_logger(name):
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        file_formatter = logging.Formatter('%(asctime)s~%(levelname)s~%(message)s~module:%(module)s~function:%(module)s')
        console_formatter = logging.Formatter('%(levelname)s -- %(message)s')
        
        file_handler = logging.FileHandler("logfile.log")
        file_handler.setLevel(logging.WARNING)
        file_handler.setFormatter(file_formatter)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(console_formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        logger.setLevel(logging.DEBUG)
    
    return logger