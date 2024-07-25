import logging
import os

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s"

project_directory = os.path.abspath(os.path.dirname(__file__))
AI_MON_DEFAULT_LOGFILE = project_directory + "/../" + "logs/ai_monitoring.log"
AI_MON_LOG_FORMAT = "[%(asctime)s [%(levelname)s] %(filename)s - %(funcName)s():%(lineno)d] %(message)s"


# Configure the logger for the ai monitoring to log to a separate log file - 'logs/ai_monitoring.log'
ai_mon_logger = logging.getLogger('ai_mon')
ai_mon_logger.setLevel(logging.INFO)
ai_mon_handler = logging.FileHandler(AI_MON_DEFAULT_LOGFILE)
ai_mon_handler.setLevel(logging.INFO)
ai_mon_formatter = logging.Formatter(AI_MON_LOG_FORMAT)
ai_mon_handler.setFormatter(ai_mon_formatter)
ai_mon_logger.addHandler(ai_mon_handler)


def init_logging(log_file_path: str, log_level: int = logging.ERROR, verbose: bool = False):
    if not verbose:
        logging.basicConfig(level=log_level, filename=log_file_path, format=LOG_FORMAT)
    else:
        logging.basicConfig(level=log_level, format=LOG_FORMAT,
                            handlers=[logging.FileHandler(log_file_path), logging.StreamHandler()])


def get_std_logger(enable_query_logging=False) -> logging.Logger:
    if enable_query_logging:
        return logging.getLogger('sqlalchemy.engine')
    return logging.getLogger(__name__)


def get_ai_mon_logger(ai_mon_logging=False) -> logging.Logger:
    if ai_mon_logging:
        return logging.getLogger('ai_mon')
    return logging.getLogger(__name__)