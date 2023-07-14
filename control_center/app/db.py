from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column, Integer
import os

sql_user = os.environ.get('SQL_USER')
sql_pass = os.environ.get('SQL_PASS')
sql_host = "localhost"
# check if containerized dev env
if os.getuid() == 999:
    sql_host = 'mydb'

mysql_connection_string = 'mysql+pymysql://{sql_user}:{sql_pass}@{sql_host}/gardennet'.format(
    sql_user=sql_user, sql_pass=sql_pass, sql_host=sql_host)

engine = create_engine(mysql_connection_string, echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import app.models
    Base.metadata.create_all(bind=engine)

def drop_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import app.models
    Base.metadata.drop_all(bind=engine)

def populate_dev_data(interval_mins=2, hours_to_pop=2):
    from app.models import Zone, Probe, DataPoint
    import random
    from datetime import datetime, timedelta

    def generate_fake_datapoints(singlepoint_variance_max, upper_bound, lower_bound, number_to_generate):
        data_points = []
        last_point = (upper_bound + lower_bound) / 2
        data_points.append(last_point)
        for x in range(number_to_generate -1):
            delta = round(random.uniform(0 - singlepoint_variance_max, singlepoint_variance_max), 2)
            if (last_point + delta) < lower_bound or (last_point + delta) > upper_bound:
                new_point = last_point - delta
            else:
                new_point = last_point + delta 
            last_point = new_point
            data_points.append(last_point)
        return data_points

    zone = Zone(name='Main', description='Primary grow zone')
    db_session.add(zone)
    db_session.commit()

    start_time = datetime.now() - timedelta(hours=hours_to_pop)
    entries_to_generate = int(hours_to_pop * 60 / interval_mins)


    p1 = Probe(
        name='env_sensor_high',
        zone_id= zone.id,
        active= True,
        description= 'Enviromental sensor placed high in the room',
        url= ''
    )
    db_session.add(p1)

    p2 = Probe(
        name= 'env_sensor_low',
        zone_id= zone.id,
        active= True,
        description= 'Enviromental sensor placed low in the room',
        url= ''
    )
    db_session.add(p2)

    p3 = Probe(
        name= 'aquatic_temp_probe_cluster',
        zone_id= zone.id,
        active= True,
        description= 'several submersible temp probes',
        url= '',
        name_mapping= {
            'probe1': 'left resevoir1',
            'probe2': 'left resevoir2',
            'probe3': 'right resevoir1',
            'probe4': 'right resevoir2',
        }
    )
    db_session.add(p3)

    p4 = Probe(
        name= 'ph_monitor',
        zone_id= zone.id,
        active= True,
        description= '',
        url= '',
        name_mapping= {
            'probe1': 'left resevoir',
            'probe2': 'right resevoir',
        }
    )
    db_session.add(p4)
    db_session.commit()

    fake_temp_list = generate_fake_datapoints(singlepoint_variance_max=2, upper_bound=90, lower_bound=60, number_to_generate=entries_to_generate)
    fake_humidity_list = generate_fake_datapoints(singlepoint_variance_max=2, upper_bound=70, lower_bound=30, number_to_generate=entries_to_generate)
    datapoint_list = []
    for x in range(entries_to_generate):
        datapoint_list.append(DataPoint(observation_datetime = start_time + timedelta(minutes=x), probe_id = p1.id, data = {'tempatureF': fake_temp_list[x], 'humidity': fake_humidity_list[x]}))
    db_session.add_all(datapoint_list)

    fake_temp_list = generate_fake_datapoints(singlepoint_variance_max=2, upper_bound=78, lower_bound=50, number_to_generate=entries_to_generate)
    fake_humidity_list = generate_fake_datapoints(singlepoint_variance_max=2, upper_bound=80, lower_bound=50, number_to_generate=entries_to_generate)
    datapoint_list = []
    for x in range(entries_to_generate):
        datapoint_list.append(DataPoint(observation_datetime = start_time + timedelta(minutes=x), probe_id = p2.id, data = {'tempatureF': fake_temp_list[x], 'humidity': fake_humidity_list[x]}))
    db_session.add_all(datapoint_list)

    fake_temp_list1 = generate_fake_datapoints(singlepoint_variance_max=1, upper_bound=70, lower_bound=50, number_to_generate=entries_to_generate)
    fake_temp_list2 = generate_fake_datapoints(singlepoint_variance_max=1, upper_bound=69, lower_bound=48, number_to_generate=entries_to_generate)
    fake_temp_list3 = generate_fake_datapoints(singlepoint_variance_max=1, upper_bound=72, lower_bound=53, number_to_generate=entries_to_generate)
    fake_temp_list4 = generate_fake_datapoints(singlepoint_variance_max=1, upper_bound=68, lower_bound=47, number_to_generate=entries_to_generate)
    datapoint_list = []
    for x in range(entries_to_generate):
        datapoint_list.append(DataPoint(observation_datetime = start_time + timedelta(minutes=x),
                                        probe_id = p3.id,
                                        data = {'probe1': fake_temp_list1[x], 'probe2': fake_temp_list2[x], 'probe3': fake_temp_list3[x], 'probe4': fake_temp_list4[x]}))
    db_session.add_all(datapoint_list)

    fake_ph_list1 = generate_fake_datapoints(singlepoint_variance_max=.5, upper_bound=11, lower_bound=3, number_to_generate=entries_to_generate)
    fake_ph_list2 = generate_fake_datapoints(singlepoint_variance_max=.5, upper_bound=10, lower_bound=4, number_to_generate=entries_to_generate)
    datapoint_list = []
    for x in range(entries_to_generate):
        datapoint_list.append(DataPoint(observation_datetime = start_time + timedelta(minutes=x),
                                        probe_id = p4.id,
                                        data = {'probe1': fake_ph_list1[x], 'probe2': fake_ph_list2[x]}))
    db_session.add_all(datapoint_list)
    db_session.commit()