from app.db import (
    engine,
    db_session,
    Base
  )

db_session.bind = engine
Base.metadata.bind = engine 

from app.models import Zone, Probe, DataPoint