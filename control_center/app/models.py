from app.db import Base
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, PrimaryKeyConstraint, Boolean, ARRAY
from sqlalchemy.orm import relationship


class Zone(Base):
  __tablename__ = 'zones'
  id = Column(Integer, primary_key = True)
  name = Column(String(50), unique = True)
  description = Column(String(128))

  probes = relationship("Probe", back_populates="zone")
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

  zone = relationship('Zone')
  probe_data = relationship("ProbeData", back_populates="probe")
  def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class ProbeData(Base):
  __tablename__ = 'probedatas'
  id = Column(Integer, primary_key = True)
  name = Column(String(50), unique = True)
  probe_id = Column(Integer, ForeignKey('probes.id'))
  name_in_probe = Column(String(50))
  description = Column(String(128))

  probe = relationship('Probe')
  def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class DataPoint(Base):
  __tablename__ = 'data_points'
  observation_datetime = Column(DateTime)
  probedata_id = Column(Integer, ForeignKey('probedatas.id'))
  data = Column(Float)
  __table_args__ = (
      PrimaryKeyConstraint(
          observation_datetime,
          probedata_id),
      {})
  def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Graph(Base):
  __tablename__= 'graphs'
  id = Column(Integer, primary_key = True)
  name = Column(String(50), unique = True)
  description = Column(String(128))

  graph_lines = relationship("GraphLine", back_populates="graph")
  def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class GraphLine(Base):
  __tablename__ = 'graphlines'
  graph_id = Column(Integer, ForeignKey('graphs.id'))
  probedata_id = Column(Integer, ForeignKey('probedatas.id'))

  probe_data = relationship('ProbeData')
  graph = relationship('Graph')
  __table_args__ = (
      PrimaryKeyConstraint(
          graph_id,
          probedata_id),
      {})