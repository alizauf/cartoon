from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', pre_meta,
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


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['username'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['username'].create()
