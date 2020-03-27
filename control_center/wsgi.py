from app import create_app
from app.db import (
    engine,
    db_session,
    Base
  )

db_session.bind = engine
Base.metadata.bind = engine 

debug = True

app = create_app(db_session=db_session, debug=debug)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=debug)