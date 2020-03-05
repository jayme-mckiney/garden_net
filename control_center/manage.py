from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

class ProbeConfig(db.Model):
  __tablename__ = 'probe_configs'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), unique = True)
    active = db.Column(db.Boolean)
    description = db.Column(db.String(128))
    url = db.Column(db.String(128))
    data_columns = db.Column(db.Array(db.String(20)))
    name_mappings = db.Column(db.Array(db.String(20)), nullable = True)


class DataEntry(db.model):
    __tablename__ = 'data_entries'
    observation_datetime = db.Column(db.DateTime)
    source = db.Column(db.String(50))
    data = db.Column(db.JSON())
    __table_args__ = (
        PrimaryKeyConstraint(
            observation_datetime,
            source),
        {})


if __name__ == '__main__':
    manager.run()