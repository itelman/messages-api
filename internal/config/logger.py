import logging


class Logger:
    def __init__(self, infoLog, errorLog):
        self.infoLog = infoLog
        self.errorLog = errorLog


info_log = logging.getLogger("info")
error_log = logging.getLogger("error")

# Configure loggers
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
info_log.setLevel(logging.INFO)
error_log.setLevel(logging.ERROR)

# Configure file logging if needed
file_handler = logging.FileHandler("/tmp/info.log")
file_handler.setLevel(logging.INFO)
info_log.addHandler(file_handler)
error_log.addHandler(file_handler)

loggers = Logger(info_log, error_log)
