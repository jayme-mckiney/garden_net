from app import create_app
from db import (
    engine,
    db_session,
    Base
  )

db_session.bind = engine
Base.metadata.bind = engine 

app = create_app(db_session)

if __name__ == "__main__":
    app.run(host='0.0.0.0')