from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column, Integer

engine = create_engine('mysql+pymysql://gardennetapp:growweedeveryday@localhost/gardennet', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    Base.metadata.create_all(bind=engine)

def drop_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    Base.metadata.drop_all(bind=engine)