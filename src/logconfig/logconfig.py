import logging
import sys

class LogConfig:
    def __init__(self, is_verbose=False, logfile='genetic.log'):
        # configuring log
        if (is_verbose):
            self.log_level=logging.DEBUG
        else:
            self.log_level=logging.INFO

        self.console_log_format = logging.Formatter('[%(asctime)s] [%(levelname)s] - %(message)s')
        self.file_log_format = logging.Formatter('[%(asctime)s] [%(levelname)s] - %(message)s')

        # writing to stdout
        consoleHandler = logging.StreamHandler(sys.stdout)
        consoleHandler.setLevel(self.log_level)
        consoleHandler.setFormatter(self.console_log_format)

        # writing to file
        fileHandler = logging.FileHandler(logfile)
        fileHandler.setLevel(self.log_level)
        fileHandler.setFormatter(self.file_log_format)

        logging.basicConfig(
            level=self.log_level,
            handlers=[consoleHandler, fileHandler])
        
        self.log = logging.getLogger(__name__)

        # Log information about configuration
        self.log.info("Logging system is configured")
        self.log.debug("Logging level: ", self.log_level)
