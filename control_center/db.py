from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://username:passwd@localhost/db', echo=True)