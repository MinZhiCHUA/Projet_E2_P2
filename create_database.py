# from application import create_app, models
# from application.models import *

# db.create_all(app=create_app()) # pass the create_app result so Flask-SQLAlchemy gets the configuration.

from application.extension import db
from application import create_app
from application.models import *
app = create_app()
with app.app_context():
    
    init_db()


# from werkzeug.security import generate_password_hash


# from application.models import User
# from application.models import db
# from application import create_app
# app = create_app()
# with app.app_context():
#     #user = db.engine.table_names()

#     # create a new user with the form data. Hash the password so the plaintext version isn't saved.
#     new_user = User(email="emai66", name="name23333", password=generate_password_hash("password", method='sha256'))

#     # add the new user to the database
#     db.session.add(new_user)
#     db.session.commit()
    
#     user = User.query.filter_by(name="name23333").all()
# print(user)