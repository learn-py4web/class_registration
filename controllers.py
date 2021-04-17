"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

"""
    Query examples: 
    
    # Catalog description of CSE 183?
    db(db.catalog_class.number == "CSE 183").select()

    # Offerings of CSE 183 in Spring 2021?
    db(
        (db.catalog_class.number == "CSE 183") &
        (db.quarter.year == 2021) & (db.quarter.name == "Spring") &
        # This encodes class offering ---> catalog class
        (db.class_offering.catalog_class_id == db.catalog_class.id) &
        # This encodes class offering ---> quarter
        (db.class_offering.quarter_id == db.quarter.id)
    ).select()

    # Who are the students on the waitlist for CSE 183 Spring 2021?
    rows = db(
        (db.catalog_class.number == "CSE 183") &
        (db.quarter.year == 2021) & (db.quarter.name == "Spring") &
        # This encodes class offering ---> catalog class
        (db.class_offering.catalog_class_id == db.catalog_class.id) &
        # This encodes class offering ---> quarter
        (db.class_offering.quarter_id == db.quarter.id) &
        # This encodes registration ---> offering
        (db.registration.class_offering_id == db.class_offering.id) &
        # This encodes registration ---> student
        (db.registration.student_id == db.student.id) &
        # Oh, and the registration has to be on the wait list.
        (db.registration.is_waitlist == True)
    ).select()
    for row in rows:
        print(row.student.first_name, row.student.last_name,
              "is on the waitlist")

"""


from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user_email

url_signer = URLSigner(session)

@action('index')
@action.uses(db, auth, 'index.html')
def index():

    return dict()
