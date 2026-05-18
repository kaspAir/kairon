from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

Base = declarative_base()
engine = None
SessionLocal = scoped_session(sessionmaker(autoflush=False, autocommit=False, expire_on_commit=False))


def import_models():
    import app.domains.decision.models  # noqa: F401
    import app.domains.scenario.models  # noqa: F401
    import app.domains.assessment.models  # noqa: F401
    import app.domains.governance.models  # noqa: F401
    import app.domains.observation.models  # noqa: F401
    import app.domains.context.models  # noqa: F401


def init_engine(database_url: str, echo: bool = False):
    global engine
    connect_args = {}
    if database_url.startswith("sqlite"):
        connect_args["check_same_thread"] = False
    engine = create_engine(database_url, echo=echo, pool_pre_ping=True, future=True, connect_args=connect_args)
    SessionLocal.configure(bind=engine)
    import_models()
    return engine


@contextmanager
def session_scope():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
