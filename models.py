"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth
from pydal.validators import *

def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()

### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later

db.define_table(
    'catalog_class', # This table, like all tables, will have an "id"
    Field('number'), # CSE 183
    Field('name'), # Web apps
    Field('description', 'text'),
)

db.define_table(
    'quarter',
    Field('year', 'integer'),
    Field('season'), # Winter
)

db.define_table(
    'class_offering',
    Field('catalog_class_id', 'reference catalog_class'),
    Field('quarter_id', 'reference quarter', ondelete="CASCADE"),
    Field('number', 'integer'),
    Field('taught_by', 'reference instructor'),
    Field('active', 'boolean') # Will this take place?
)

db.define_table(
    'student',
    Field('email'),
    Field('first_name'),
    Field('last_name'),
    Field('suid'),
)

db.define_table(
    'registration',
    Field('student_id', 'reference student'),
    Field('class_offering_id', 'reference class_offering'),
    Field('is_waitlist', 'boolean'),
    Field('waitlist_pos', 'integer'),
    Field('note', 'text'),
    Field('registration_date', 'datetime'),
)

db.define_table(
    'instructor',
    Field('email'),
    Field('first_name'),
    Field('last_name'),
)

db.commit()
