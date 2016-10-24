#!flask/bin/python
import os
from config import BASEDIR, SQLALCHEMY_DATABASE_URI
from app import manager, db
from flask_migrate import MigrateCommand


@manager.command
def create_db():
    """Initialize a database"""
    if not os.path.exists(os.path.join(BASEDIR, 'app.db')):
        db.create_all()
        print('Database initialized at %s' % SQLALCHEMY_DATABASE_URI)
        return
    print('Database has been already initialized')


manager.add_command('db', MigrateCommand)
manager.run()
