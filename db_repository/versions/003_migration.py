from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
caption = Table('caption', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('text', VARCHAR(length=250)),
    Column('user_id', INTEGER),
    Column('contest_id', INTEGER),
    Column('submission_date', DATETIME),
)

caption = Table('caption', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('text', String(length=250)),
    Column('user_id', Integer),
    Column('contest_id', Integer),
    Column('timestamp', DateTime),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String(length=64)),
    Column('password', String(length=100)),
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
    pre_meta.tables['caption'].columns['submission_date'].drop()
    post_meta.tables['caption'].columns['timestamp'].create()
    post_meta.tables['user'].columns['date_joined'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['caption'].columns['submission_date'].create()
    post_meta.tables['caption'].columns['timestamp'].drop()
    post_meta.tables['user'].columns['date_joined'].drop()
