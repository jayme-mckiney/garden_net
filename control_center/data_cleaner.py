from app.db import db_session
from app.models import DataPoint
from sqlalchemy import func
from datetime import datetime, timedelta
import sqlalchemy as sa

def create_temp_table_obj(model, temp_name=None):
  if temp_name == None:
    temp_name = "temp_" + model.__table__.name
  new_columns = []
  for c in model.__table__.columns.values():
    new_columns.append(sa.Column(c.name, c.type))
  temp_table = sa.Table(temp_name, model.metadata,
                        *new_columns,
                        # ...
                        prefixes=['TEMPORARY'],)
  return temp_table

def clean(start_time=datetime.now()-timedelta(days=2), days=1):
  '''
  This function reducs the data gathered over x number of days from a given start point to only the first
  point of data for every probe_data piece over a 10 minute period

  working query for mysql

  CREATE TEMPORARY TABLE rows_to_keep_temp  AS
  WITH sel AS (
    SELECT * FROM data_points
    WHERE  observation_datetime between '2018-10-30' AND '2018-10-31'
  ),
  filter_times AS (
    SELECT min(observation_datetime) AS observation_datetime, probedata_id
    FROM   sel
    GROUP  BY floor(UNIX_TIMESTAMP(observation_datetime) / 600), probedata_id
    ORDER  BY 1
  )
  SELECT filter_times.observation_datetime, sel.probedata_id, data
  FROM  filter_times join sel
  ON sel.observation_datetime = filter_times.observation_datetime
  AND sel.probedata_id = filter_times.probedata_id;

  DELETE FROM data_points
  WHERE observation_datetime between '2018-10-30' AND '2018-10-31';

  INSERT INTO data_points (observation_datetime, probedata_id, data)
  SELECT observation_datetime, probedata_id, data
  FROM rows_to_keep_temp

  The nice things I could have if mariadb's returning functionality was useful

  WITH del AS (
     DELETE FROM "data_points"
     WHERE  observation_datetime <= '2018-10-31+0'
     RETURNING *
     )
  INSERT INTO "data_points"
  SELECT observation_datetime, del_whole.probedata_id, data
    FROM del AS del_whole JOIN(
  SELECT min(observation_datetime) AS timestamp, probedata_id
  FROM   del
  GROUP  BY floor(UNIX_TIMESTAMP(observation_datetime) / 600), probedata_id
  ORDER  BY 1) AS del_selected on (del_selected.timestamp = del_whole.snapshot_timestamp) and (del_selected.probedata_id = del_whole.probedata_id)
  '''

  keepers = create_temp_table_obj(DataPoint, 'temp_keepers')

  time_frame_logic = DataPoint.observation_datetime.between(start_time, start_time + timedelta(days=1))

  select_statement = sa.select(DataPoint).where(time_frame_logic).cte('sel')
  min_ts_statement = sa.select(sa.func.min(select_statement.c.observation_datetime).label('observation_datetime'), select_statement.c.probedata_id
                        ).group_by(sa.func.floor(sa.func.unix_timestamp(select_statement.c.observation_datetime) / 600), select_statement.c.probedata_id).cte('min_ts')

  join_statement = sa.select(select_statement.c.observation_datetime, select_statement.c.probedata_id, select_statement.c.data
                      ).join(min_ts_statement, 
                        sa.and_(select_statement.c.observation_datetime == min_ts_statement.c.observation_datetime,
                                select_statement.c.probedata_id == min_ts_statement.c.probedata_id))


  db_session.execute(sa.text('create temporary table {name} like {base_name}'.format(name=keepers.name, base_name=DataPoint.__table__.name)))
  insert_to_temp = sa.insert(keepers).from_select(DataPoint.__table__.c.values(), join_statement)
  db_session.execute(insert_to_temp)
  db_session.execute(sa.delete(DataPoint).where(time_frame_logic))
  q = sa.insert(DataPoint).from_select(DataPoint.__table__.c.values(), keepers)
  db_session.execute(q)
  r = db_session.execute(sa.text('drop table {name}'.format(name=keepers.name)))
  db_session.commit()
  DataPoint.metadata.remove(keepers)




if (__name__ == '__main__'):
  clean()
