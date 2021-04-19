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

import datetime

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A, SPAN
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user_email

from py4web.utils.form import Form, FormStyleBulma
from .common import Field

url_signer = URLSigner(session)

@action('index')
@action.uses(db, auth, 'index.html')
def index():
    return dict()

@action('offerings')
@action.uses(db, auth, 'offerings.html')
def offerings():
    rows = db(
        (db.quarter.year == 2021) &
        (db.quarter.season == "Spring") &
        (db.class_offering.quarter_id == db.quarter.id) &
        (db.class_offering.catalog_class_id == db.catalog_class.id)
    ).select()
    return dict(rows=rows)

@action('register/<offering_id:int>', method=["GET", "POST"])
@action.uses(db, session, auth.user, 'register.html')
def register(offering_id=None):
    assert offering_id is not None
    offering_info = db(
        (db.class_offering.id == offering_id) &
        (db.class_offering.quarter_id == db.quarter.id) &
        (db.class_offering.catalog_class_id == db.catalog_class.id)
    ).select().first()
    assert offering_info is not None
    # At this point, I have the info to show to the user.
    form = Form([Field('note', 'text')],
                csrf_session=session, formstyle=FormStyleBulma
                )
    form.param.sidecar.append(SPAN(" ", A('Cancel', _class="button", _href=URL('offerings'))))
    if form.accepted:
        # Insert the note along with the registration.
        # Get the student id.
        student = db(db.student.email == get_user_email()).select().first()
        assert student is not None
        # Now we can insert the new registration record.
        db.registration.insert(
            student_id=student.id,
            class_offering_id=offering_id,
            is_waitlist=False,
            note=form.vars["note"],
            registration_date=datetime.datetime.utcnow(),
        )
        redirect(URL('index'))
    return dict(offering_info=offering_info,
                form=form)
