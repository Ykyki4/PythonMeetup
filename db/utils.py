from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from models import User


engine = create_engine('sqlite:///db.sqlite3', echo=True)
session = Session(engine)


def get_user(telegram_id):
	try:
		stmt = select(User).where(User.telegram_id==telegram_id)
		user = session.scalars(stmt).one()
	except NoResultFound:
		return None
	return user


def create_user(first_name, last_name, telegram_id):
	user = User(
		first_name=first_name,
        last_name=last_name,
        telegram_id=telegram_id,
    )

	session.add_all([user])
	session.commit()

	return user
