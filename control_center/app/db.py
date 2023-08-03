from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from sqlalchemy import Column, Integer
import os

sql_user = os.environ.get('SQL_USER')
sql_pass = os.environ.get('SQL_PASS')
is_testing = os.environ.get('TEST_RUN', False)
sql_host = "localhost"
# check if containerized dev env
if os.getuid() == 999:
    sql_host = 'mydb'

database_name = 'gardennet_test' if is_testing else 'gardennet'

mysql_connection_string = 'mysql+pymysql://{sql_user}:{sql_pass}@{sql_host}/{database_name}'.format(
    sql_user=sql_user, sql_pass=sql_pass, sql_host=sql_host, database_name=database_name)

engine = create_engine(mysql_connection_string, echo=False)
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
    zone = app.models.Zone(name='Main', description='Primary grow zone')
    db_session.add(zone)
    db_session.commit()

def drop_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import app.models
    Base.metadata.drop_all(bind=engine)

def populate_dev_data(interval_mins=2, hours_to_pop=2):
    from app.models import Zone, Probe, ProbeData, DataPoint
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

    start_time = datetime.now() - timedelta(hours=hours_to_pop)
    entries_to_generate = int(hours_to_pop * 60 / interval_mins)


    p1 = Probe(
        name='env_sensor_high',
        zone_id= zone.id,
        active= True,
        description= 'Enviromental sensor placed high in the room',
        url= ''
    )
    db_session.add(p1)\

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
        url= ''
    )
    db_session.add(p3)

    p4 = Probe(
        name= 'ph_monitor',
        zone_id= zone.id,
        active= True,
        description= 'multi probe ph monitor',
        url= ''
    )
    db_session.add(p4)
    db_session.commit()

    pd1_1 = ProbeData(
        name='tempature high',
        probe_id=p1.id,
        description='temperature from high in the room',
        name_in_probe='tempatureF',
    )
    pd1_2 = ProbeData(
        name='humidity high',
        probe_id=p1.id,
        description='humidity from high in the room',
        name_in_probe='humidity',
    )
    db_session.add(pd1_1)
    db_session.add(pd1_2)

    pd2_1 = ProbeData(
        name='tempature low',
        probe_id=p2.id,
        description='temperature from low in the room',
        name_in_probe='tempatureF',

    )
    pd2_2 = ProbeData(
        name='humidity low',
        probe_id=p2.id,
        description='humidity from low in the room',
        name_in_probe='humidity',
    )
    db_session.add(pd2_1)
    db_session.add(pd2_2)

    pd3_1 = ProbeData(
        name='resevoir tempature 1',
        probe_id=p3.id,
        description='temperature from inside the resevoir',
        name_in_probe='probe1',

    )
    pd3_2 = ProbeData(
        name='resevoir tempature 2',
        probe_id=p3.id,
        description='temperature from inside the resevoir',
        name_in_probe='probe2',
    )
    pd3_3 = ProbeData(
        name='resevoir tempature 3',
        probe_id=p3.id,
        description='temperature from inside the resevoir',
        name_in_probe='probe3',

    )
    pd3_4 = ProbeData(
        name='resevoir tempature 4',
        probe_id=p3.id,
        description='temperature from inside the resevoir',
        name_in_probe='probe4',
    )
    db_session.add(pd3_1)
    db_session.add(pd3_2)
    db_session.add(pd3_3)
    db_session.add(pd3_4)
    pd4_1 = ProbeData(
        name='resevoir ph 1',
        probe_id=p4.id,
        description='ph levels from inside the resevoir',
        name_in_probe='probe1',

    )
    pd4_2 = ProbeData(
        name='resevoir ph 2',
        probe_id=p4.id,
        description='ph levels from inside the resevoir',
        name_in_probe='probe2',
    )
    db_session.add(pd4_1)
    db_session.add(pd4_2)
    db_session.commit()

    fake_temp_list = generate_fake_datapoints(singlepoint_variance_max=2, upper_bound=90, lower_bound=60, number_to_generate=entries_to_generate)
    fake_humidity_list = generate_fake_datapoints(singlepoint_variance_max=2, upper_bound=70, lower_bound=30, number_to_generate=entries_to_generate)
    temp_datapoint_list = []
    hum_datapoint_list = []
    for x in range(entries_to_generate):
        temp_datapoint_list.append(DataPoint(observation_datetime = start_time + timedelta(minutes=x), probedata_id = pd1_1.id, data =  fake_temp_list[x]))
        hum_datapoint_list.append(DataPoint(observation_datetime = start_time + timedelta(minutes=x), probedata_id = pd1_2.id, data = fake_humidity_list[x]))
    db_session.add_all(temp_datapoint_list)
    db_session.add_all(hum_datapoint_list)

    fake_temp_list = generate_fake_datapoints(singlepoint_variance_max=2, upper_bound=78, lower_bound=50, number_to_generate=entries_to_generate)
    fake_humidity_list = generate_fake_datapoints(singlepoint_variance_max=2, upper_bound=80, lower_bound=50, number_to_generate=entries_to_generate)
    temp_datapoint_list = []
    hum_datapoint_list = []
    for x in range(entries_to_generate):
        temp_datapoint_list.append(DataPoint(observation_datetime = start_time + timedelta(minutes=x), probedata_id = pd2_1.id, data =  fake_temp_list[x]))
        hum_datapoint_list.append(DataPoint(observation_datetime = start_time + timedelta(minutes=x), probedata_id = pd2_2.id, data = fake_humidity_list[x]))
    db_session.add_all(temp_datapoint_list)
    db_session.add_all(hum_datapoint_list)

    fake_temp_list1 = generate_fake_datapoints(singlepoint_variance_max=1, upper_bound=70, lower_bound=50, number_to_generate=entries_to_generate)
    fake_temp_list2 = generate_fake_datapoints(singlepoint_variance_max=1, upper_bound=69, lower_bound=48, number_to_generate=entries_to_generate)
    fake_temp_list3 = generate_fake_datapoints(singlepoint_variance_max=1, upper_bound=72, lower_bound=53, number_to_generate=entries_to_generate)
    fake_temp_list4 = generate_fake_datapoints(singlepoint_variance_max=1, upper_bound=68, lower_bound=47, number_to_generate=entries_to_generate)
    datapoint_list1 = []
    datapoint_list2 = []
    datapoint_list3 = []
    datapoint_list4 = []
    for x in range(entries_to_generate):
        datapoint_list1.append(DataPoint(observation_datetime = start_time + timedelta(minutes=x), probedata_id = pd3_1.id, data = fake_temp_list1[x]))
        datapoint_list2.append(DataPoint(observation_datetime = start_time + timedelta(minutes=x), probedata_id = pd3_2.id, data = fake_temp_list2[x]))
        datapoint_list3.append(DataPoint(observation_datetime = start_time + timedelta(minutes=x), probedata_id = pd3_3.id, data = fake_temp_list3[x]))
        datapoint_list4.append(DataPoint(observation_datetime = start_time + timedelta(minutes=x), probedata_id = pd3_4.id, data = fake_temp_list4[x]))
    db_session.add_all(datapoint_list1)
    db_session.add_all(datapoint_list2)
    db_session.add_all(datapoint_list3)
    db_session.add_all(datapoint_list4)

    fake_ph_list1 = generate_fake_datapoints(singlepoint_variance_max=.5, upper_bound=11, lower_bound=3, number_to_generate=entries_to_generate)
    fake_ph_list2 = generate_fake_datapoints(singlepoint_variance_max=.5, upper_bound=10, lower_bound=4, number_to_generate=entries_to_generate)
    datapoint_list1 = []
    datapoint_list2 = []
    for x in range(entries_to_generate):
        datapoint_list1.append(DataPoint(observation_datetime = start_time + timedelta(minutes=x), probedata_id = pd4_1.id, data = fake_ph_list1[x]))
        datapoint_list2.append(DataPoint(observation_datetime = start_time + timedelta(minutes=x), probedata_id = pd4_2.id, data = fake_ph_list2[x]))
    db_session.add_all(datapoint_list1)
    db_session.add_all(datapoint_list2)
    db_session.commit()