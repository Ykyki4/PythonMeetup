from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, Session

engine = create_engine('sqlite:///db.sqlite3', echo=True)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    telegram_id = Column(Integer(), primary_key=True)
    first_name = Column(String(16))
    last_name = Column(String(16))

Base.metadata.create_all(engine)
