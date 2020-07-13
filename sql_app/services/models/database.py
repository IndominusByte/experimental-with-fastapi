import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIR_DB = "sqlite:///" + os.path.join(BASE_DIR,'../','app.db')

engine = create_engine(DIR_DB, echo=True)
session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
Base = declarative_base()
Base.query = session.query_property()
