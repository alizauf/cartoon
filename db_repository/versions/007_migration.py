from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
users = Table('users', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('username', VARCHAR(length=64)),
    Column('social_id', VARCHAR(length=64)),
    Column('nickname', VARCHAR(length=64)),
    Column('first_name', VARCHAR(length=64)),
    Column('last_name', VARCHAR(length=100)),
    Column('email', VARCHAR(length=120)),
    Column('bio', VARCHAR(length=140)),
    Column('last_seen', DATETIME),
    Column('date_joined', DATETIME),
    Column('something_funny', VARCHAR(length=300)),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String(length=64)),
    Column('social_id', String(length=64)),
    Column('nickname', String(length=64)),
    Column('first_name', String(length=64)),
    Column('last_name', String(length=100)),
    Column('email', String(length=120)),
    Column('bio', String(length=140)),
    Column('last_seen', DateTime),
    Column('date_joined', DateTime),
    Column('something_funny', String(length=300)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['users'].drop()
    post_meta.tables['user'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['users'].create()
    post_meta.tables['user'].drop()
