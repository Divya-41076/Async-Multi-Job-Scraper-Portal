import time
import logging
from sqlalchemy.exc import OperationalError, IntegrityError

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
BASE_DELAY = 0.1


def safe_db_write(operation, session):
    """
    Executes a DB operation with retry for deadlocks
    operation: function (lambda) that performs DB actions
    session: SQLAlchemy session
    """

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            operation()
            session.flush()  # force execution
            return True

        except IntegrityError:
            # duplicate or constraint issue → skip
            session.rollback()
            logger.warning("Duplicate or constraint violation — skipping row")
            return False

        except OperationalError as e:
            session.rollback()

            if "deadlock" in str(e).lower():
                logger.warning(f"Deadlock detected (attempt {attempt})")

                if attempt == MAX_RETRIES:
                    logger.error("Max retries reached — giving up")
                    return False

                time.sleep(BASE_DELAY * attempt)  # exponential-ish backoff
                continue

            # unknown DB error → rethrow
            raise

    return False