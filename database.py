from sqlalchemy.orm import Session
from sqlalchemy import  create_engine


engine = create_engine('sqlite:///test_db.db')


def db_session():
    conn = Session(engine)
    return conn