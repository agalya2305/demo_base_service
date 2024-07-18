import logging

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s"


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