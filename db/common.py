from contextlib import contextmanager

from sqlalchemy.exc import SQLAlchemyError

from db.models import db


@contextmanager
def db_session():
    session = db.session()
    try:
        yield session
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()