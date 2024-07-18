import logging
from contextlib import contextmanager

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from common.logging_util import get_std_logger
from config_env import ConfigEnv


class DBUtil:
    def __init__(self, db_url=None, enable_query_logging=False):
        if db_url is None:
            db_url = ConfigEnv.DATABASE_URL
        if not db_url:
            raise Exception("DATABASE_URL value is not available in .env file")
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.logger = get_std_logger(enable_query_logging)
        if enable_query_logging:
            # logs the sql queries in console and in log file
            self.logger.setLevel(logging.INFO)

    @contextmanager
    def get_session(self):
        """Provide a transactional scope around a series of operations."""
        session = self.Session()
        try:
            yield session
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Session rollback because of error: {e}")
            raise
        finally:
            session.close()

    def execute_query(self, query):
        """Execute a raw SQL query."""
        with self.engine.connect() as connection:
            try:
                result = connection.execute(text(query))
                return result.fetchall()
            except SQLAlchemyError as e:
                self.logger.error(f"Error executing query: {e}")
                raise


if __name__ == '__main__':
    db_util = DBUtil()
    prospect_list_query = "select name from prospect"
    results = db_util.execute_query(prospect_list_query)
    for result in results:
        print(result[0])
