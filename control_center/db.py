from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://gardennetapp:growweedeveryday@localhost/gardennet', echo=True)