from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from main import User


engine = create_engine('sqlite:///db.sqlite3', echo=True)

def create_user(first_name, last_name, telegram_id)
	with Session(engine) as session:

		user = User(
			first_name=first_name,
	        last_name=last_name
	        telegram_id=telegram_id,
	    )

		session.add_all([user])

		session.commit()
