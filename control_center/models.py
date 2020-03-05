from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, JSON
Base = declarative_base()

class ProbeConfig(Base):
  __tablename__ = 'probe_configs'
  id = Column(Integer, primary_key = True)
  name = Column(String(50), unique = True)
  zone_id = Column(Interger, ForeignKey('zone.id'))
  active = Column(Boolean)
  description = Column(String(128))
  url = Column(String(128))
  data_columns = Column(Array(String(20)))
  name_mappings = Column(Array(String(20)), nullable = True)


class Zone(Base):
  __tablename__ = 'zones'
  id = Column(Integer, primary_key = True)
  name = Column(String(50), unique = True)
  description = Column(String(128))


class DataEntry(Base):
    __tablename__ = 'data_entries'
    observation_datetime = Column(DateTime)
    source = Column(String(50))
    data = Column(JSON())
    __table_args__ = (
        PrimaryKeyConstraint(
            observation_datetime,
            source),
        {})
