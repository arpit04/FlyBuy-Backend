"""
Database configuration and initialization
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from src.models import Base


db_user = "postgres"
db_password = "ramanujan"
db_name = "flybuy"
db_host = "127.0.0.1"
db_port = 5432

uri_string = f"postgres://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = create_engine(uri_string)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Base.query = db_session.query_property()


def init_db():

    import src.models

    Base.metadata.create_all(bind=engine)
