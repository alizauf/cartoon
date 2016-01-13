from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String(length=64)),
    Column('password', String(length=100)),
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
    post_meta.tables['user'].columns['first_name'].create()
    post_meta.tables['user'].columns['last_name'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['first_name'].drop()
    post_meta.tables['user'].columns['last_name'].drop()
