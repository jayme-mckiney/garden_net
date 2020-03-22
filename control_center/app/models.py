from db import Base
from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, PrimaryKeyConstraint, Boolean, ARRAY


class Zone(Base):
  __tablename__ = 'zones'
  id = Column(Integer, primary_key = True)
  name = Column(String(50), unique = True)
  description = Column(String(128))
  def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Probe(Base):
  __tablename__ = 'probes'
  id = Column(Integer, primary_key = True)
  name = Column(String(50), unique = True)
  zone_id = Column(Integer, ForeignKey('zones.id'))
  active = Column(Boolean)
  description = Column(String(128))
  url = Column(String(128))
  name_mapping = Column(JSON())
  def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class DataPoint(Base):
  __tablename__ = 'data_points'
  observation_datetime = Column(DateTime)
  probe_id = Column(Integer, ForeignKey('probes.id'))
  data = Column(JSON())
  __table_args__ = (
      PrimaryKeyConstraint(
          observation_datetime,
          probe_id),
      {})
  def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}